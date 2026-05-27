"""config.py — RedAmon Android: colors, constants, widget helpers."""
from kivy.utils import get_color_from_hex as hx
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle

C = {
    'bg':            '#0a0a0f',
    'bg_card':       '#12121a',
    'bg_input':      '#1a1a26',
    'accent_red':    '#e63946',
    'accent_blue':   '#4cc9f0',
    'accent_green':  '#4ade80',
    'accent_yellow': '#fbbf24',
    'accent_purple': '#a78bfa',
    'text':          '#e2e8f0',
    'text_dim':      '#64748b',
    'border':        '#1e293b',
    'success':       '#22c55e',
    'warning':       '#f59e0b',
    'danger':        '#ef4444',
}

MODELS = [
    'claude-haiku-4-5-20251001',
    'claude-sonnet-4-6',
]

APP_VERSION = '1.0.0'


def bg(widget, color_hex):
    """Paint a solid background on any Kivy widget."""
    with widget.canvas.before:
        Color(*hx(color_hex))
        rect = Rectangle(pos=widget.pos, size=widget.size)
    widget.bind(
        pos=lambda *a: setattr(rect, 'pos', widget.pos),
        size=lambda *a: setattr(rect, 'size', widget.size),
    )


def flat_btn(text, bg_hex, fg_hex='#ffffff', **kw):
    """Flat button with custom colours."""
    return Button(
        text=text, markup=True,
        color=hx(fg_hex),
        background_color=hx(bg_hex),
        background_normal='',
        background_down='',
        **kw,
    )


def card(padding=12, spacing=8, **kw):
    """Return a BoxLayout styled as a card."""
    from kivy.uix.boxlayout import BoxLayout
    box = BoxLayout(padding=dp(padding), spacing=dp(spacing), **kw)
    bg(box, C['bg_card'])
    return box


def hdr_label(text, color_key='accent_red'):
    lbl = Label(
        text=f'[b]{text}[/b]', markup=True,
        font_size='14sp', color=hx(C[color_key]),
        size_hint_y=None, height=dp(32),
        halign='left', valign='middle',
    )
    lbl.bind(size=lbl.setter('text_size'))
    return lbl


SEVERITY_COLOR = {
    'CRITICAL': '#e63946',
    'HIGH':     '#f97316',
    'MEDIUM':   '#fbbf24',
    'LOW':      '#4ade80',
    'INFO':     '#4cc9f0',
}
