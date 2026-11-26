{{-- Utopia Tickets (nov-2026): copia de la v2.2.0 con la fecha de la sesión en español si el idioma del correo es es. Original sha256 ba7d76ea555f8721 --}}
@php /** @var \HiEvents\DomainObjects\WaitlistEntryDomainObject $entry */ @endphp
@php /** @var \HiEvents\DomainObjects\EventDomainObject $event */ @endphp
@php /** @var ?string $productName */ @endphp
@php /** @var ?string $occurrenceDateFormatted */ @endphp
@php /** @var \HiEvents\DomainObjects\OrganizerDomainObject $organizer */ @endphp
@php /** @var \HiEvents\DomainObjects\EventSettingDomainObject $eventSettings */ @endphp
@php /** @var string $eventUrl */ @endphp

@php /** @see \HiEvents\Mail\Waitlist\WaitlistOfferExpiredMail */ @endphp

@php $utopiaEs = str_starts_with(app()->getLocale(), 'es'); @endphp
@php
    // La sesión llega como 'dddd, MMMM D · h:mm A' («sábado, diciembre 5 · 7:30 p. m.»): pasa a «sábado 5 de diciembre a las 19:30».
    if ($utopiaEs && $occurrenceDateFormatted && preg_match('/^(\S+), (\S+) (\d{1,2}) · (\d{1,2}):(\d{2})\s*([ap])\.\s*m\.$/u', $occurrenceDateFormatted, $utopiaM)) {
        $occurrenceDateFormatted = sprintf('%s %d de %s a las %02d:%s', $utopiaM[1], $utopiaM[3], $utopiaM[2], (int) $utopiaM[4] % 12 + ($utopiaM[6] === 'p' ? 12 : 0), $utopiaM[5]);
    }
@endphp

<x-mail::message>
# {{ __('Your waitlist offer has expired') }}

{{ __('Hello') }},

@if($occurrenceDateFormatted && $productName)
{{ __('Unfortunately, your waitlist offer for **:product** on **:date** for the event **:event** has expired.', ['product' => $productName, 'date' => $occurrenceDateFormatted, 'event' => $event->getTitle()]) }}
@elseif($occurrenceDateFormatted)
{{ __('Unfortunately, your waitlist offer on **:date** for the event **:event** has expired.', ['date' => $occurrenceDateFormatted, 'event' => $event->getTitle()]) }}
@elseif($productName)
{{ __('Unfortunately, your waitlist offer for **:product** for the event **:event** has expired.', ['product' => $productName, 'event' => $event->getTitle()]) }}
@else
{{ __('Unfortunately, your waitlist offer for the event **:event** has expired.', ['event' => $event->getTitle()]) }}
@endif

{{ __('If you are still interested, you may rejoin the waitlist from the event page.') }}

<x-mail::button :url="$eventUrl">
{{ __('View Event') }}
</x-mail::button>

{{ __('If you have any questions or need assistance, please respond to this email.') }}

{{ __('Thank you') }},<br>
{{ $organizer->getName() ?: config('app.name') }}

{!! $eventSettings->getGetEmailFooterHtml() !!}
</x-mail::message>
