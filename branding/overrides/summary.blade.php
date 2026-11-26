{{-- Utopia Tickets (nov-2026): copia de la v2.2.0 con fechas en español si el idioma del correo es es. Original sha256 dcab578f5ca20587
     el contacto es el correo de atención del evento (support_email), no el de la cuenta del organizador, y sale el lugar --}}
@php use Carbon\Carbon; use HiEvents\Helper\Currency; use HiEvents\Helper\DateHelper; @endphp
@php /** @var \HiEvents\DomainObjects\OrderDomainObject $order */ @endphp
@php /** @var \HiEvents\DomainObjects\EventDomainObject $event */ @endphp
@php /** @var \HiEvents\DomainObjects\OrganizerDomainObject $organizer */ @endphp
@php /** @var \HiEvents\DomainObjects\EventSettingDomainObject $eventSettings */ @endphp
@php /** @var \HiEvents\DomainObjects\EventOccurrenceDomainObject|null $occurrence */ @endphp
@php /** @var string $orderUrl */ @endphp
@php /** @var \HiEvents\Services\Domain\Lineup\DTO\EmailLineupHighlightsDTO|null $lineup */ @endphp

@php /** @see \HiEvents\Mail\Order\OrderSummary */ @endphp

@php $utopiaEs = str_starts_with(app()->getLocale(), 'es'); @endphp
@php
    $displayStart = $occurrence?->getStartDate() ?? $event->getStartDate();
    $displayDate = (new Carbon(DateHelper::convertFromUTC($displayStart, $event->getTimezone())))->locale(app()->getLocale())->{$utopiaEs ? 'translatedFormat' : 'format'}($utopiaEs ? 'l, j \\d\\e F' : 'F j, Y');
    $displayTime = (new Carbon(DateHelper::convertFromUTC($displayStart, $event->getTimezone())))->format($utopiaEs ? 'H:i' : 'g:i A');
@endphp

<x-mail::message>
@if($order->isOrderAwaitingOfflinePayment())
# {{ __('Order placed: payment needed') }}
@else
# {{ __('Your Order is Confirmed! ') }} 🎉
@endif

@if($order->isOrderAwaitingOfflinePayment() === false)

<p>
{{ __('Congratulations! Your order for :eventTitle on :eventDate at :eventTime was successful. Please find your order details below.', ['eventTitle' => $event->getTitle(), 'eventDate' => $displayDate, 'eventTime' => $displayTime]) }}
</p>

@else

<div>
<p>
{{ __('Your order is pending payment. Tickets have been issued but will not be valid until payment is received.') }}
</p>

<div style="border-radius: 4px; background-color: #d7e8f8; color: #204e84; margin-bottom: 1.5rem; padding: 1rem;">
<h2>{{ __('How to pay') }}</h2>
<p>
{{ __('Amount due') }}: <b>{{ Currency::format($order->getTotalGross(), $event->getCurrency(), $utopiaEs ? 'es_ES' : 'en_US') }}</b><br>
@if($eventSettings->getOfflinePaymentOrderReferenceEnabled())
{{ __('Payment reference') }}: <b>{{ $order->getPublicId() }}</b><br>
{{ __('Include this reference with your payment so the organizer can match it to your order.') }}
@endif
</p>
{!! $eventSettings->getOfflinePaymentInstructions() !!}
</div>
</div>

@endif

<p>

## {{ __('Event Details') }}
**{{ __('Event Name:') }}** {{ $event->getTitle() }}
    <br>
**{{ __('Date & Time:') }}** {{ __(':date at :time', ['date' => $displayDate, 'time' => $displayTime]) }}
@if($occurrence?->getLabel())
    <br>
**{{ __('Session:') }}** {{ $occurrence->getLabel() }}
@endif
@php
    // el lugar (nombre y dirección) también en la confirmación, como en el correo de la entrada.
    $utopiaLoc = $occurrence?->getEventLocation() ?? $event->getEventLocation();
    $utopiaVenue = ($utopiaLoc && $utopiaLoc->getType() === \HiEvents\DomainObjects\Enums\LocationType::IN_PERSON->name) ? $utopiaLoc->getLocation() : null;
    $utopiaLugar = '';
    if ($utopiaVenue) {
        $utopiaDir = is_array($utopiaVenue->getStructuredAddress()) ? $utopiaVenue->getStructuredAddress() : [];
        $utopiaNombre = $utopiaVenue->getName() ?: ($utopiaDir['venue_name'] ?? null);
        if ($utopiaNombre) { unset($utopiaDir['venue_name']); }
        $utopiaLugar = implode(', ', array_filter([$utopiaNombre, \HiEvents\Helper\AddressHelper::formatAddress($utopiaDir)], static fn ($x) => $x !== null && $x !== ''));
    }
@endphp
@if($utopiaLugar !== '')
    <br>
**{{ __('Location:') }}** {{ $utopiaLugar }}
@endif

</p>

@include('emails.partials.lineup-highlights', ['lineup' => $lineup])

@if($eventSettings->getPostCheckoutMessage() && $order->isOrderCompleted())
<p>

## {{ __('Additional Information') }}

{!! $eventSettings->getPostCheckoutMessage() !!}

</p>
@endif

## {{ __('Order Summary') }}
- **{{ __('Order Number:') }}** {{ $order->getPublicId() }}
- **{{ __('Total Amount:') }}** {{ Currency::format($order->getTotalGross(), $event->getCurrency(), $utopiaEs ? 'es_ES' : 'en_US') }}
@if($order->getSeatLabels())
- **{{ __('Seats:') }}** {{ implode(', ', $order->getSeatLabels()) }}
@endif

<x-mail::button :url="$orderUrl">
    {{ __('View Order Summary & Tickets') }}
</x-mail::button>

@php $utopiaContacto = $eventSettings->getSupportEmail() ?: $organizer->getEmail(); @endphp
{{ __('If you have any questions or need assistance, please contact') }} <a href="mailto:{{ $utopiaContacto }}">{{ $utopiaContacto }}</a>.

{{ __('Best regards,') }}<br>
{{ $organizer->getName() ?: config('app.name') }}
</x-mail::message>
