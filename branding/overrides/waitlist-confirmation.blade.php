{{-- Utopia Tickets (nov-2026): copia de la v2.2.0 con la fecha de la sesión en español si el idioma del correo es es. Original sha256 f01c1a30bdbb2f85 --}}
@php /** @var \HiEvents\DomainObjects\WaitlistEntryDomainObject $entry */ @endphp
@php /** @var \HiEvents\DomainObjects\EventDomainObject $event */ @endphp
@php /** @var ?string $productName */ @endphp
@php /** @var ?string $occurrenceDateFormatted */ @endphp
@php /** @var \HiEvents\DomainObjects\OrganizerDomainObject $organizer */ @endphp
@php /** @var \HiEvents\DomainObjects\EventSettingDomainObject $eventSettings */ @endphp
@php /** @var string $eventUrl */ @endphp

@php /** @see \HiEvents\Mail\Waitlist\WaitlistConfirmationMail */ @endphp

@php $utopiaEs = str_starts_with(app()->getLocale(), 'es'); @endphp
@php
    // La sesión llega como 'dddd, MMMM D · h:mm A' («sábado, diciembre 5 · 7:30 p. m.»): pasa a «sábado 5 de diciembre a las 19:30».
    if ($utopiaEs && $occurrenceDateFormatted && preg_match('/^(\S+), (\S+) (\d{1,2}) · (\d{1,2}):(\d{2})\s*([ap])\.\s*m\.$/u', $occurrenceDateFormatted, $utopiaM)) {
        $occurrenceDateFormatted = sprintf('%s %d de %s a las %02d:%s', $utopiaM[1], $utopiaM[3], $utopiaM[2], (int) $utopiaM[4] % 12 + ($utopiaM[6] === 'p' ? 12 : 0), $utopiaM[5]);
    }
@endphp

<x-mail::message>
# {{ __("You're on the waitlist!") }}

{{ __('Hello') }},

@if($occurrenceDateFormatted && $productName)
{{ __("You have been added to the waitlist for **:product** on **:date** for the event **:event**.", ['product' => $productName, 'date' => $occurrenceDateFormatted, 'event' => $event->getTitle()]) }}
@elseif($occurrenceDateFormatted)
{{ __("You have been added to the waitlist on **:date** for the event **:event**.", ['date' => $occurrenceDateFormatted, 'event' => $event->getTitle()]) }}
@elseif($productName)
{{ __("You have been added to the waitlist for **:product** for the event **:event**.", ['product' => $productName, 'event' => $event->getTitle()]) }}
@else
{{ __("You have been added to the waitlist for the event **:event**.", ['event' => $event->getTitle()]) }}
@endif

{{ __("We'll notify you as soon as a spot becomes available.") }}

<x-mail::button :url="$eventUrl">
{{ __('View Event') }}
</x-mail::button>

{{ __('If you have any questions or need assistance, please respond to this email.') }}

{{ __('Thank you') }},<br>
{{ $organizer->getName() ?: config('app.name') }}

{!! $eventSettings->getGetEmailFooterHtml() !!}
</x-mail::message>
