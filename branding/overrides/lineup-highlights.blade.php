{{-- Utopia Tickets (nov-2026): copia de la v2.2.0 con las horas del programa en 24 h si el idioma del correo es es («7:30 p. m.» → «19:30»). Original sha256 576e4ad086aa76a1 --}}
@php /** @var \HiEvents\Services\Domain\Lineup\DTO\EmailLineupHighlightsDTO|null $lineup */ @endphp
@php
    $utopiaEs = str_starts_with(app()->getLocale(), 'es');
    $utopiaHora = fn ($t) => $utopiaEs ? preg_replace_callback('/(\d{1,2}):(\d{2})\s*([ap])\.\s*m\./u', fn ($m) => sprintf('%02d:%s', (int) $m[1] % 12 + ($m[3] === 'p' ? 12 : 0), $m[2]), $t) : $t;
@endphp
@if($lineup)
<div style="border: 1px solid #e5e7eb; border-radius: 6px; padding: 16px; margin: 16px 0; line-height: 1.6;">
<strong>{{ $lineup->heading }}</strong><br>
@if($lineup->names !== [])
{{ implode(', ', $lineup->names) }}<br>
@endif
@foreach($lineup->slots as $slot)
<span style="color: #6b7280;">{{ $utopiaHora($slot['time']) }}</span> · {{ $slot['title'] }}@if($slot['stage']) · {{ $slot['stage'] }}@endif<br>
@endforeach
<a href="{{ $lineup->url }}">{{ $lineup->slots === [] ? __('See the full lineup') : __('See the full schedule') }}</a>
</div>
@endif
