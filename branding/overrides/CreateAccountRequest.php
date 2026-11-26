<?php

declare(strict_types=1);

namespace HiEvents\Http\Request\Account;

use HiEvents\Http\Request\BaseRequest;
use HiEvents\Locale;
use HiEvents\Validators\Rules\PersonNameRule;
use HiEvents\Validators\Rules\RulesHelper;
use Illuminate\Validation\Rule;
use Illuminate\Validation\Rules\Password;

class CreateAccountRequest extends BaseRequest
{
    use ValidatesAttribution;

    public function rules(): array
    {
        $currencies = include __DIR__.'/../../../../data/currencies.php';

        return [
            'first_name' => PersonNameRule::rules(),
            'last_name' => PersonNameRule::rules(required: false),
            'email' => RulesHelper::REQUIRED_EMAIL,
            'password' => ['required', 'confirmed', Password::min(8)],
            'timezone' => ['timezone:all'],
            'currency_code' => [Rule::in(array_values($currencies))],
            'locale' => ['nullable', Rule::in(Locale::getSupportedLocales())],
            'invite_token' => ['nullable', 'string'],
            'marketing_opt_in' => 'boolean|nullable',
            ...$this->attributionRules(),
            'turnstile_token' => ['nullable', 'string', 'max:2048'],
            // Utopia Tickets (nov-2026): alta libre de promotores con aceptación expresa de las condiciones para
            // promotores y de la política de privacidad. Sin la casilla marcada no se crea la cuenta.
            'utopia_acepta_condiciones' => ['accepted'],
        ];
    }

    public function messages(): array
    {
        return [
            'utopia_acepta_condiciones.accepted' => 'Para crear la cuenta tienes que aceptar las condiciones para promotores y la política de privacidad.',
        ];
    }
}
