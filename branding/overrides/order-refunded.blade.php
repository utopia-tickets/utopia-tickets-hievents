@php /** @var \HiEvents\DomainObjects\OrderDomainObject $order */ @endphp
@php /** @var \HiEvents\DomainObjects\EventDomainObject $event */ @endphp
@php /** @var \HiEvents\DomainObjects\OrganizerDomainObject $organizer */ @endphp
@php /** @var \HiEvents\Values\MoneyValue $refundAmount */ @endphp
@php /** @var \HiEvents\DomainObjects\EventSettingDomainObject $eventSettings */ @endphp

@php /** @see \HiEvents\Mail\Order\OrderRefunded */ @endphp

@php $utopiaEs = str_starts_with(app()->getLocale(), 'es'); @endphp
@php /* Utopia Tickets (nov-2026): el importe del reembolso salía como «EUR 20.00» (MoneyValue::__toString); en español, «20,00 €». */ @endphp
@php $utopiaRefund = $utopiaEs ? \HiEvents\Helper\Currency::format($refundAmount->toFloat(), $refundAmount->getMoney()->getCurrency()->getCurrencyCode(), 'es_ES') : $refundAmount; @endphp
<x-mail::message>
{{ __('Hello') }},

{{ __('You have received a refund of :refundAmount for the following event: :eventTitle.', ['refundAmount' => $utopiaRefund, 'eventTitle' => $event->getTitle()]) }}

{{ __('Thank you') }},<br>
{{ $organizer->getName() ?: config('app.name') }}

{!! $eventSettings->getGetEmailFooterHtml() !!}
</x-mail::message>
