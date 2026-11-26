<?php

declare(strict_types=1);

namespace HiEvents\Http\Actions\Accounts;

use HiEvents\Exceptions\EmailAlreadyExists;
use HiEvents\Exceptions\UnauthorizedException;
use HiEvents\Http\Actions\Auth\BaseAuthAction;
use HiEvents\Http\Request\Account\CreateAccountRequest;
use HiEvents\Http\ResponseCodes;
use HiEvents\Resources\Account\AccountResource;
use HiEvents\Services\Application\Handlers\Account\CreateAccountHandler;
use HiEvents\Services\Application\Handlers\Account\DTO\CreateAccountDTO;
use HiEvents\Services\Application\Handlers\Account\Exceptions\AccountConfigurationDoesNotExist;
use HiEvents\Services\Application\Handlers\Account\Exceptions\AccountRegistrationDisabledException;
use HiEvents\Services\Application\Handlers\Auth\DTO\LoginCredentialsDTO;
use HiEvents\Services\Application\Handlers\Auth\LoginHandler;
use HiEvents\Services\Application\Locale\LocaleService;
use HiEvents\Services\Domain\Account\AttributionDataSanitizer;
use HiEvents\Services\Domain\Auth\PasswordLoginPolicy;
use HiEvents\Services\Infrastructure\Turnstile\TurnstileVerifier;
use Illuminate\Contracts\Encryption\DecryptException;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Mail;
use Illuminate\Http\JsonResponse;
use Illuminate\Validation\ValidationException;
use Throwable;

class CreateAccountAction extends BaseAuthAction
{
    public function __construct(
        private readonly CreateAccountHandler $createAccountHandler,
        private readonly LoginHandler $loginHandler,
        private readonly LocaleService $localeService,
        private readonly TurnstileVerifier $turnstileVerifier,
        private readonly AttributionDataSanitizer $attributionDataSanitizer,
        private readonly PasswordLoginPolicy $passwordLoginPolicy,
    ) {}

    /**
     * @throws Throwable
     * @throws ValidationException
     */
    public function __invoke(CreateAccountRequest $request): JsonResponse
    {
        if ($this->passwordLoginPolicy->isDisabled()) {
            return $this->errorResponse(
                message: __('Password sign-up is turned off. Use one of the sign-in options instead.'),
                statusCode: ResponseCodes::HTTP_FORBIDDEN,
            );
        }

        if (! $this->turnstileVerifier->verify($request->validated('turnstile_token'), $this->getClientIp($request))) {
            throw ValidationException::withMessages([
                'turnstile_token' => __('Please complete the security check and try again.'),
            ]);
        }

        try {
            $accountData = $this->createAccountHandler->handle(CreateAccountDTO::fromArray([
                'first_name' => $request->validated('first_name'),
                'last_name' => $request->validated('last_name'),
                'email' => $request->validated('email'),
                'password' => $request->validated('password'),
                'timezone' => $request->validated('timezone'),
                'currency_code' => $request->validated('currency_code'),
                'locale' => $request->has('locale')
                    ? $request->validated('locale')
                    : $this->localeService->getLocaleOrDefault($request->getPreferredLanguage()),
                'invite_token' => $request->validated('invite_token'),
                'marketing_opt_in' => (bool) $request->validated('marketing_opt_in'),
                ...$this->attributionDataSanitizer->fromValidated($request->validated()),
            ]));
        } catch (EmailAlreadyExists $e) {
            throw ValidationException::withMessages([
                'email' => $e->getMessage(),
            ]);
        } catch (DecryptException $e) {
            throw ValidationException::withMessages([
                'invite_token' => __('Invalid invite token'),
            ]);
        } catch (AccountRegistrationDisabledException) {
            return $this->errorResponse(
                message: __('Account registration is disabled'),
                statusCode: ResponseCodes::HTTP_FORBIDDEN,
            );
        } catch (AccountConfigurationDoesNotExist $e) {
            return $this->errorResponse(
                message: $e->getMessage(),
                statusCode: ResponseCodes::HTTP_INTERNAL_SERVER_ERROR,
            );
        }

        // Utopia Tickets (nov-2026): registro de la aceptación (qué versión y cuándo) y aviso a Utopia de la nueva alta.
        $this->utopiaRegistrarAlta($request, $accountData);

        try {
            $loginResponse = $this->loginHandler->handle(new LoginCredentialsDTO(
                email: $accountData->getEmail(),
                password: $request->validated('password'),
                accountId: $accountData->getId(),
            ));
        } catch (UnauthorizedException $e) {
            return $this->errorResponse(
                message: $e->getMessage(),
                statusCode: ResponseCodes::HTTP_UNAUTHORIZED,
            );
        }

        return $this->addTokenToResponse($this->resourceResponse(
            resource: AccountResource::class,
            data: $accountData,
            statusCode: ResponseCodes::HTTP_CREATED,
        ), $loginResponse->token);
    }

    /**
     * Utopia Tickets (nov-2026). Guarda en `utopia_aceptaciones` una fila por documento aceptado (condiciones para
     * promotores y privacidad) con su versión y su huella sha256, la fecha, la IP y el navegador, y avisa por
     * correo a la dirección de `UTOPIA_AVISO_ALTAS`. Nunca impide el alta: si algo falla queda en el log y el
     * aviso dice «NO REGISTRADAS: revisar».
     */
    private function utopiaRegistrarAlta(CreateAccountRequest $request, $account): void
    {
        $versiones = [];
        try {
            $ruta = (string) env('UTOPIA_LEGAL_VERSIONES', '/branding/public/legal/versiones.json');
            $leido = is_readable($ruta) ? json_decode((string) file_get_contents($ruta), true) : null;
            $versiones = is_array($leido) ? ($leido['documentos'] ?? []) : [];
        } catch (Throwable $e) {
            Log::error('utopia: no se pudieron leer las versiones legales', ['error' => $e->getMessage()]);
        }

        $userId = null;
        $aceptados = [];
        try {
            $userId = DB::table('account_users')
                ->where('account_id', $account->getId())
                ->where('is_account_owner', true)
                ->value('user_id');
            $ahora = now()->toDateTimeString();
            foreach (['condiciones-promotores', 'privacidad'] as $doc) {
                $v = $versiones[$doc] ?? [];
                $fila = [
                    'account_id' => $account->getId(),
                    'user_id' => $userId,
                    'email' => strtolower((string) $account->getEmail()),
                    'documento' => $doc,
                    'version' => (string) ($v['version'] ?? 'desconocida'),
                    'sha256' => (string) ($v['sha256'] ?? ''),
                    'url' => (string) ($v['url'] ?? ''),
                    'origen' => 'registro',
                    'ip' => $this->getClientIp($request),
                    'user_agent' => mb_substr((string) $request->userAgent(), 0, 500),
                    'aceptado_en' => $ahora,
                    'created_at' => $ahora,
                ];
                DB::table('utopia_aceptaciones')->insert($fila);
                $aceptados[] = $doc.' '.$fila['version'].' ('.substr($fila['sha256'], 0, 12).')';
            }
        } catch (Throwable $e) {
            Log::error('utopia: no se pudo registrar la aceptación de condiciones', [
                'account_id' => $account->getId(),
                'error' => $e->getMessage(),
            ]);
        }

        $destino = trim((string) env('UTOPIA_AVISO_ALTAS', ''));
        if ($destino === '') {
            return;
        }
        try {
            $base = rtrim((string) config('app.frontend_url'), '/');
            $texto = implode("\n", [
                'Nueva alta de promotor en Utopia Tickets.',
                '',
                'Cuenta: '.$account->getName().' (id '.$account->getId().')',
                'Correo: '.$account->getEmail(),
                'Fecha: '.now()->toDateTimeString().' UTC',
                'Condiciones aceptadas: '.($aceptados ? implode('; ', $aceptados) : 'NO REGISTRADAS: revisar'),
                '',
                'Revisar: '.$base.'/admin/accounts/'.$account->getId(),
                'Herramienta: altas_promotores.py revisar '.$account->getId(),
                'Para suspender: altas_promotores.py suspender '.$account->getId().' --motivo "..."',
            ]);
            $para = array_values(array_filter(array_map('trim', explode(',', $destino))));
            Mail::raw($texto, function ($m) use ($para, $account) {
                $m->to($para)->subject('[Utopia Tickets] Nueva alta de promotor: '.$account->getName());
            });
        } catch (Throwable $e) {
            Log::error('utopia: no se pudo avisar de la nueva alta', [
                'account_id' => $account->getId(),
                'error' => $e->getMessage(),
            ]);
        }
    }
}
