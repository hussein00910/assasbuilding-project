"""screens/settings_screen.py — API key, model, scan config."""
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.metrics import dp
from kivy.utils import get_color_from_hex as hx

from config import C, bg, flat_btn, hdr_label, MODELS
from database.db import set_cfg, get_cfg


class SettingsScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self._build()

    def on_enter(self):
        self._load()

    def _build(self):
        sv = ScrollView()
        root = BoxLayout(orientation='vertical',
                         padding=dp(16), spacing=dp(14),
                         size_hint_y=None)
        root.bind(minimum_height=root.setter('height'))
        bg_widget = BoxLayout()
        bg(bg_widget, C['bg'])
        bg_widget.add_widget(sv)
        sv.add_widget(root)
        self.add_widget(bg_widget)

        root.add_widget(hdr_label('⚙️ Settings'))

        # ── Claude API ──
        root.add_widget(self._section('Claude AI Configuration'))

        root.add_widget(Label(
            text='Anthropic API Key:', color=hx(C['text_dim']),
            font_size='12sp', size_hint_y=None, height=dp(26), halign='left'))
        self._api_key = TextInput(
            hint_text='sk-ant-api03-…',
            password=True, multiline=False,
            background_color=hx(C['bg_input']),
            foreground_color=hx(C['text']),
            hint_text_color=hx(C['text_dim']),
            font_size='12sp', size_hint_y=None, height=dp(44),
        )
        root.add_widget(self._api_key)

        root.add_widget(Label(
            text='Model:', color=hx(C['text_dim']),
            font_size='12sp', size_hint_y=None, height=dp(26), halign='left'))
        self._model = Spinner(
            text='claude-haiku-4-5-20251001',
            values=MODELS,
            background_color=hx(C['bg_input']),
            color=hx(C['text']), font_size='12sp',
            size_hint_y=None, height=dp(44),
        )
        root.add_widget(self._model)

        # ── Save button ──
        save_btn = flat_btn('💾  Save Settings', C['accent_red'],
                            size_hint_y=None, height=dp(50), font_size='13sp')
        save_btn.bind(on_press=self._save)
        root.add_widget(save_btn)

        # ── Status ──
        self._status = Label(
            text='', color=hx(C['accent_green']),
            font_size='12sp', size_hint_y=None, height=dp(32))
        root.add_widget(self._status)

        # ── About ──
        root.add_widget(self._section('About'))
        about_text = (
            'RedAmon Android v1.0\n'
            'AI-Powered Penetration Testing Platform\n\n'
            'Tools: Port Scanner, Subdomain Enum, DNS,\n'
            'SSL Check, Headers, Tech Detection,\n'
            'Dir Brute-Force, WHOIS, Web Crawler\n\n'
            'AI: Claude (Anthropic) via API\n'
            'Storage: SQLite (local)\n\n'
            '⚠️  For authorized testing only.'
        )
        root.add_widget(Label(
            text=about_text, color=hx(C['text_dim']),
            font_size='11sp', size_hint_y=None, height=dp(180),
            halign='left', valign='top'))

    def _section(self, title):
        lbl = Label(
            text=f'[b][color=e63946]{title}[/color][/b]',
            markup=True, font_size='12sp',
            color=hx(C['accent_red']),
            size_hint_y=None, height=dp(30),
            halign='left')
        lbl.bind(size=lbl.setter('text_size'))
        return lbl

    def _load(self):
        self._api_key.text = get_cfg('api_key', '')
        m = get_cfg('model', 'claude-haiku-4-5-20251001')
        if m in MODELS:
            self._model.text = m

    def _save(self, *a):
        set_cfg('api_key', self._api_key.text.strip())
        set_cfg('model',   self._model.text)
        self._status.text = '✓ Saved!'
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: setattr(self._status, 'text', ''), 2)
