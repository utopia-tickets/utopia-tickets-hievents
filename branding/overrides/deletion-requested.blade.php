@php /** @var \HiEvents\DomainObjects\AccountDomainObject $account */ @endphp
@php /** @var string $scheduledDeletionDate */ @endphp
@php /** @var bool $willBeAnonymized */ @endphp
@php /** @var string $cancelLink */ @endphp
{{-- Utopia Tickets (nov-2026): copia de la v2.2.0 con la fecha en español si el idioma del correo es es. Original sha256 c1b5c53ed5c54f20 --}}
@php
    // AccountDeletionRequestedEmail la da con toFormattedDateString() ('M j, Y', «Dec 5, 2026», siempre en inglés): pasa a «5 de diciembre de 2026».
    if (str_starts_with(app()->getLocale(), 'es')) {
        try { $scheduledDeletionDate = \Carbon\Carbon::createFromFormat('!M j, Y', $scheduledDeletionDate)->locale(app()->getLocale())->translatedFormat('j \\d\\e F \\d\\e Y'); } catch (\Throwable $e) {}
    }
@endphp

<x-mail::message>
{{ __('Hi') }},

{{ __('We have received a request to delete your :appName account. Your account has been deactivated and is scheduled for permanent deletion on :date.', ['appName' => config('app.name'), 'date' => $scheduledDeletionDate]) }}

{{ __('All of your published events have been unpublished. If you cancel the deletion, you will need to republish them manually.') }}

@if ($willBeAnonymized)
{{ __('Because your account has completed orders, transaction records (amounts, dates, and invoice details) will be retained in an anonymized form for legal and tax purposes. All personal information will be permanently removed.') }}
@else
{{ __('Your account and all of its data will be permanently deleted.') }}
@endif

{{ __('If you did not request this, or you change your mind, you can cancel the deletion at any time before :date:', ['date' => $scheduledDeletionDate]) }}

<x-mail::button :url="$cancelLink">
    {{ __('Cancel Account Deletion') }}
</x-mail::button>

{{ __('Best Regards,') }}<br>
{{ __('The :appName Team', ['appName' => config('app.name')]) }}
</x-mail::message>
