{{-- Utopia Tickets (nov-2026): copia de la v2.2.0 con fechas en español si el idioma del correo es es. Original sha256 0183f37b707debbf --}}
@php /** @var \HiEvents\DomainObjects\WaitlistEntryDomainObject $entry */ @endphp
@php /** @var \HiEvents\DomainObjects\EventDomainObject $event */ @endphp
@php /** @var ?string $productName */ @endphp
@php /** @var ?string $occurrenceDateFormatted */ @endphp
@php /** @var \HiEvents\DomainObjects\OrganizerDomainObject $organizer */ @endphp
@php /** @var \HiEvents\DomainObjects\EventSettingDomainObject $eventSettings */ @endphp
@php /** @var string $checkoutUrl */ @endphp

@php /** @see \HiEvents\Mail\Waitlist\WaitlistOfferMail */ @endphp

@php $utopiaEs = str_starts_with(app()->getLocale(), 'es'); @endphp
@php
    // WaitlistOfferMail da la sesión como 'dddd, MMMM D · h:mm A' («sábado, diciembre 5 · 7:30 p. m.») y la caducidad como
    // 'MMMM D, YYYY [at] h:mm A (z)' en UTC. Se rehacen: «sábado 5 de diciembre a las 19:30», la caducidad en la zona del evento.
    if ($utopiaEs && $occurrenceDateFormatted && preg_match('/^(\S+), (\S+) (\d{1,2}) · (\d{1,2}):(\d{2})\s*([ap])\.\s*m\.$/u', $occurrenceDateFormatted, $utopiaM)) {
        $occurrenceDateFormatted = sprintf('%s %d de %s a las %02d:%s', $utopiaM[1], $utopiaM[3], $utopiaM[2], (int) $utopiaM[4] % 12 + ($utopiaM[6] === 'p' ? 12 : 0), $utopiaM[5]);
    }
    if ($utopiaEs && $entry->getOfferExpiresAt()) {
        $offerExpiresAtFormatted = \Carbon\Carbon::parse($entry->getOfferExpiresAt(), 'UTC')->setTimezone($event->getTimezone())->locale(app()->getLocale())->translatedFormat('l j \\d\\e F \\a \\l\\a\\s H:i');
    }
@endphp

<x-mail::message>
# {{ __('A spot has opened up!') }}

{{ __('Hello') }},

@if($occurrenceDateFormatted && $productName)
{{ __('Great news! A spot has become available for **:product** on **:date** for the event **:event**.', ['product' => $productName, 'date' => $occurrenceDateFormatted, 'event' => $event->getTitle()]) }}
@elseif($occurrenceDateFormatted)
{{ __('Great news! A spot has become available on **:date** for the event **:event**.', ['date' => $occurrenceDateFormatted, 'event' => $event->getTitle()]) }}
@elseif($productName)
{{ __('Great news! A spot has become available for **:product** for the event **:event**.', ['product' => $productName, 'event' => $event->getTitle()]) }}
@else
{{ __('Great news! A spot has become available for the event **:event**.', ['event' => $event->getTitle()]) }}
@endif

{{ __('An order has been reserved for you. Click the button below to complete your purchase.') }}

@if($offerExpiresAtFormatted)
{{ __('This offer expires on :date. Please complete your order before it expires.', ['date' => $offerExpiresAtFormatted]) }}
@endif

<x-mail::button :url="$checkoutUrl">
{{ __('Complete Your Order') }}
</x-mail::button>

{{ __('If you have any questions or need assistance, please respond to this email.') }}

{{ __('Thank you') }},<br>
{{ $organizer->getName() ?: config('app.name') }}

{!! $eventSettings->getGetEmailFooterHtml() !!}
</x-mail::message>
