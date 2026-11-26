{{-- Utopia Tickets (nov-2026): copia de la v2.2.0 con la fecha en español («sábado 5 de diciembre de 2026 a las 19:30») si el idioma del correo es es. Original sha256 561333f2583dc786 --}}
@php /** @var \HiEvents\DomainObjects\EventDomainObject $event */ @endphp
@php /** @var \HiEvents\DomainObjects\EventOccurrenceDomainObject $occurrence */ @endphp
@php /** @var \HiEvents\DomainObjects\OrganizerDomainObject $organizer */ @endphp
@php /** @var \HiEvents\DomainObjects\EventSettingDomainObject $eventSettings */ @endphp
@php /** @var string $formattedDate */ @endphp
@php /** @var string $eventUrl */ @endphp
@php /** @var bool $refundOrders */ @endphp

@php /** @see \HiEvents\Mail\Occurrence\OccurrenceCancellationMail */ @endphp

@php $utopiaEs = str_starts_with(app()->getLocale(), 'es'); @endphp
@php
    // MailBuilderService la trae como 'F j, Y g:i A' (inglés fijo); se rehace desde la fecha de la sesión en la zona del evento.
    if ($utopiaEs && $occurrence?->getStartDate()) {
        $formattedDate = \Carbon\Carbon::parse($occurrence->getStartDate(), 'UTC')->setTimezone($event->getTimezone())->locale(app()->getLocale())->translatedFormat('l j \\d\\e F \\d\\e Y \\a \\l\\a\\s H:i');
    }
@endphp

<x-mail::message>
# {{ $event->getTitle() }}

{{ __('Hello') }},

{{ __('We\'re sorry to let you know that **:event** scheduled for **:date** has been cancelled.', ['event' => $event->getTitle(), 'date' => $formattedDate]) }}

@if($refundOrders)
{{ __('If your order is eligible, a refund will be processed automatically and may take a few business days to appear on your statement. If we are unable to process it automatically, our team will be in touch.') }}
@else
{{ __('If you have any questions about your order, please respond to this email.') }}
@endif

<x-mail::button :url="$eventUrl">
{{ __('View Event') }}
</x-mail::button>

{{ __('Thank you') }},<br>
{{ $organizer->getName() ?: config('app.name') }}

{!! $eventSettings->getGetEmailFooterHtml() !!}
</x-mail::message>
