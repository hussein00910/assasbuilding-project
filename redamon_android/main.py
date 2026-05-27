#!/usr/bin/env python3
"""
🔴 RedAmon Android v1.0
========================
AI-Powered Penetration Testing Platform for Android

Features:
  • 9 Pure-Python recon tools running in parallel
  • Claude AI Agent (multi-step ReAct analysis)
  • Interactive AI chat per scan
  • SQLite scan storage & findings database
  • Full pentest report generation

WARNING: For AUTHORIZED security testing only.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.utils import get_color_from_hex as hx
from kivy.metrics import dp
from kivy.clock import Clock

from config import C, bg, flat_btn
from database.db import init_db
from screens.dashboard    import DashboardScreen
from screens.scan_screen  import ScanScreen
from screens.ai_screen    import AIScreen
from screens.settings_screen import SettingsScreen

Window.clearcolor = hx('#0a0a0fff')


# ── Disclaimer ────────────────────────────────────────────────────────────────
class DisclaimerPopup(Popup):
    def __init__(self, **kw):
        super().__init__(
            title='🔴 RedAmon — Legal Notice',
            size_hint=(.93, .70),
            auto_dismiss=False, **kw)

        root = BoxLayout(orientation='vertical',
                         padding=dp(16), spacing=dp(14))
        bg(root, C['bg_card'])

        msg = Label(
            text=(
                '[b][color=e63946]⚠ AUTHORIZED USE ONLY ⚠[/color][/b]\n\n'
                'RedAmon is an [b]AI-powered penetration testing[/b]\n'
                'platform for [b]authorized security testing[/b] ONLY.\n\n'
                '• You must have [b]written permission[/b] from\n'
                '  the system owner before scanning.\n\n'
                '• Unauthorized use is a [b]criminal offence[/b]\n'
                '  in most jurisdictions.\n\n'
                '• Designed for: CTF, labs, your own systems.\n\n'
                '[i][color=64748b]Tap I Agree to continue[/color][/i]'
            ),
            markup=True, halign='center', valign='middle',
            color=hx(C['text']), font_size='13sp',
        )
        msg.bind(size=msg.setter('text_size'))

        btn_row = BoxLayout(size_hint_y=None, height=dp(52), spacing=dp(10))
        agree = flat_btn('✅  I Agree — Continue', C['accent_red'], font_size='13sp')
        leave = flat_btn('❌  Exit',                C['bg_input'],  C['text_dim'], font_size='13sp')
        agree.bind(on_press=lambda *a: self.dismiss())
        leave.bind(on_press=lambda *a: App.get_running_app().stop())
        btn_row.add_widget(agree)
        btn_row.add_widget(leave)

        root.add_widget(msg)
        root.add_widget(btn_row)
        self.content = root


# ── Top bar ───────────────────────────────────────────────────────────────────
class TopBar(BoxLayout):
    def __init__(self, **kw):
        super().__init__(
            size_hint_y=None, height=dp(48),
            padding=[dp(14), dp(6)], **kw)
        bg(self, C['bg_card'])
        l = Label(
            text='[b][color=e63946]🔴 RedAmon[/color]  '
                 '[color=64748b]Android AI PenTest[/color][/b]',
            markup=True, font_size='14sp', halign='left',
            color=hx(C['text']))
        l.bind(size=l.setter('text_size'))
        r = Label(
            text='[color=e63946]Auth Only[/color]',
            markup=True, font_size='11sp', halign='right')
        self.add_widget(l)
        self.add_widget(r)


# ── Bottom nav ───────────────────────────────────────────────────────────────
class NavBar(BoxLayout):
    TABS = [
        ('🏠\nDashboard', 'dashboard', '#4cc9f0'),
        ('🔍\nScan',      'scan',      '#e63946'),
        ('🤖\nAI Agent',  'ai',        '#a78bfa'),
        ('⚙️\nSettings',  'settings',  '#64748b'),
    ]

    def __init__(self, sm, **kw):
        super().__init__(size_hint_y=None, height=dp(58), spacing=dp(2), **kw)
        bg(self, C['bg_card'])
        self.sm = sm
        self._btns = {}
        for label, name, color in self.TABS:
            btn = flat_btn(label, C['bg_input'], C['text_dim'],
                           font_size='10sp')
            btn.bind(on_press=lambda b, n=name, c=color: self._go(n, c))
            self.add_widget(btn)
            self._btns[name] = (btn, color)
        self._go('dashboard', '#4cc9f0')

    def _go(self, name, color):
        for n, (b, c) in self._btns.items():
            b.background_color = hx(C['bg_input'])
            b.color = hx(C['text_dim'])
        btn, clr = self._btns[name]
        btn.background_color = hx(clr + '33')   # tinted
        btn.color = hx(clr)
        self.sm.current = name


# ── App ───────────────────────────────────────────────────────────────────────
class RedAmonApp(App):
    def build(self):
        self.title = '🔴 RedAmon Android'
        init_db()

        sm = ScreenManager(transition=FadeTransition(duration=0.12))
        sm.add_widget(DashboardScreen(name='dashboard'))
        sm.add_widget(ScanScreen(     name='scan'))
        sm.add_widget(AIScreen(       name='ai'))
        sm.add_widget(SettingsScreen( name='settings'))

        root = BoxLayout(orientation='vertical')
        root.add_widget(TopBar())
        root.add_widget(sm)
        root.add_widget(NavBar(sm))

        Clock.schedule_once(lambda dt: DisclaimerPopup().open(), 0.6)
        return root


if __name__ == '__main__':
    RedAmonApp().run()
