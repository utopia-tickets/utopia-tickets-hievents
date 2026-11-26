{{-- Utopia Tickets (nov-2026): copia de la v2.2.0 con el plazo de pago en español si el idioma del correo es es. Original sha256 79443f6572211a4a --}}
@php /** @var \HiEvents\DomainObjects\OrderDomainObject $order */ @endphp
@php /** @var \HiEvents\DomainObjects\EventDomainObject $event */ @endphp
@php /** @var \HiEvents\DomainObjects\OrganizerDomainObject $organizer */ @endphp
@php /** @var \HiEvents\DomainObjects\EventSettingDomainObject $eventSettings */ @endphp
@php /** @var string $paymentLinkUrl */ @endphp
@php /** @var string $amountDue */ @endphp
@php /** @var string $payByFormatted */ @endphp

@php /** @see \HiEvents\Mail\Order\OrderPaymentLinkMail */ @endphp

@php $utopiaEs = str_starts_with(app()->getLocale(), 'es'); @endphp
@php
    // OrderPaymentLinkMail lo da como 'dddd, MMMM D · h:mm A z' («sábado, diciembre 5 · 7:30 p. m. CET»): pasa a «sábado 5 de diciembre a las 19:30».
    if ($utopiaEs && $order->getReservedUntil()) {
        $payByFormatted = \Carbon\Carbon::parse($order->getReservedUntil(), 'UTC')->setTimezone($event->getTimezone())->locale(app()->getLocale())->translatedFormat('l j \\d\\e F \\a \\l\\a\\s H:i');
    }
@endphp

<x-mail::message>
# {{ __('Your payment link is ready') }}

{{ __('Hello') }},

{{ __('Your registration for :event is saved and your places are held. Forward this email, or the link below, to whoever is paying. They will see your order and can pay for it.', ['event' => $event->getTitle()]) }}

{{ __('Amount due') }}: <b>{{ $amountDue }}</b><br>
{{ __('Order reference') }}: <b>{{ $order->getPublicId() }}</b><br>
{{ __('Pay by') }}: <b>{{ $payByFormatted }}</b>

<x-mail::button :url="$paymentLinkUrl">
{{ __('Open payment page') }}
</x-mail::button>

{{ __('If the order is not paid by then, the places are released and the link stops working. You will receive your order confirmation by email as soon as they complete checkout.') }}

{{ __('Anyone with this link can view and pay for this order, so only share it with the person paying.') }}

{{ __('Thank you') }},<br>
{{ $organizer->getName() ?: config('app.name') }}

{!! $eventSettings->getGetEmailFooterHtml() !!}
</x-mail::message>
