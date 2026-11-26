@php /** @var string $scheduledDeletionDate */ @endphp
@php /** @var string $cancelLink */ @endphp
{{-- Utopia Tickets (nov-2026): copia de la v2.2.0 con la fecha en español si el idioma del correo es es. Original sha256 47ac057d002474c7 --}}
@php
    // ProcessScheduledAccountDeletionsJob la da con toFormattedDateString() ('M j, Y', «Dec 5, 2026», siempre en inglés): pasa a «5 de diciembre de 2026».
    if (str_starts_with(app()->getLocale(), 'es')) {
        try { $scheduledDeletionDate = \Carbon\Carbon::createFromFormat('!M j, Y', $scheduledDeletionDate)->locale(app()->getLocale())->translatedFormat('j \\d\\e F \\d\\e Y'); } catch (\Throwable $e) {}
    }
@endphp

<x-mail::message>
{{ __('Hi') }},

{{ __('This is a reminder that your :appName account is scheduled for permanent deletion on :date.', ['appName' => config('app.name'), 'date' => $scheduledDeletionDate]) }}

{{ __('If you want to keep your account, cancel the deletion before this date:') }}

<x-mail::button :url="$cancelLink">
    {{ __('Cancel Account Deletion') }}
</x-mail::button>

{{ __('If you take no action, the deletion will proceed automatically and cannot be undone.') }}

{{ __('Best Regards,') }}<br>
{{ __('The :appName Team', ['appName' => config('app.name')]) }}
</x-mail::message>
