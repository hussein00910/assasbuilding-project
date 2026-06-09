"""
HomeScreen — Main menu with 4 category buttons + History button.
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.metrics import dp

from tools.categories import CATEGORIES
from utils.theme import (BG_DARK, BG_CARD, TEXT_PRIMARY, TEXT_SECONDARY,
                          FONT_TITLE, FONT_BODY, BTN_HEIGHT)


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()

    def _build_ui(self):
        with self.canvas.before:
            Color(*BG_DARK)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)

        root = BoxLayout(orientation='vertical', spacing=0)

        # ── Header ────────────────────────────────────
        header = BoxLayout(orientation='vertical',
                           size_hint_y=None, height=dp(100),
                           padding=[dp(20), dp(15)])
        with header.canvas.before:
            Color(0.0, 0.0, 0.0, 0.4)
            self.hdr_rect = Rectangle(pos=header.pos, size=header.size)
        header.bind(pos=lambda *a: setattr(self.hdr_rect, 'pos', header.pos),
                    size=lambda *a: setattr(self.hdr_rect, 'size', header.size))

        title = Label(
            text="[color=00e5ff][b]🛡 SECURITY TOOLKIT[/b][/color]",
            markup=True,
            font_size='24sp',
            halign='center',
            size_hint_y=None, height=dp(40),
        )
        subtitle = Label(
            text="[color=607d8b]Ethical Hacking · Authorized Testing Only[/color]",
            markup=True,
            font_size='13sp',
            halign='center',
            size_hint_y=None, height=dp(25),
        )
        header.add_widget(title)
        header.add_widget(subtitle)
        root.add_widget(header)

        # ── Scrollable grid of category cards ───────────────────
        scroll = ScrollView(size_hint=(1, 1))
        grid = GridLayout(
            cols=2,
            spacing=dp(12),
            padding=[dp(14), dp(14)],
            size_hint_y=None,
        )
        grid.bind(minimum_height=grid.setter('height'))

        for cat in CATEGORIES:
            btn = self._make_cat_btn(cat)
            grid.add_widget(btn)

        # History & About buttons
        hist_btn = self._make_action_btn(
            "📜  History", (0.2, 0.2, 0.3, 1), self._go_history)
        grid.add_widget(hist_btn)

        info_btn = self._make_action_btn(
            "ℹ️  About", (0.15, 0.2, 0.2, 1), self._show_about)
        grid.add_widget(info_btn)

        scroll.add_widget(grid)
        root.add_widget(scroll)
        self.add_widget(root)

    def _make_cat_btn(self, cat: dict) -> Button:
        ACCENT = {
            'cyan':   (0.0, 0.9, 1.0, 1),
            'green':  (0.0, 1.0, 0.5, 1),
            'purple': (0.8, 0.0, 1.0, 1),
            'teal':   (0.0, 0.9, 0.8, 1),
            'orange': (1.0, 0.5, 0.0, 1),
            'red':    (1.0, 0.2, 0.2, 1),
            'yellow': (1.0, 0.85, 0.0, 1),
            'blue':   (0.2, 0.6, 1.0, 1),
            'lime':   (0.6, 0.9, 0.0, 1),
        }
        color = ACCENT.get(cat.get('color', 'cyan'), (0.0, 0.9, 1.0, 1))
        r, g, b, _ = color
        bg = (r * 0.15, g * 0.15, b * 0.15, 1)

        text = (f"[color={self._rgba_hex(color)}][b]{cat['icon']} {cat['name']}[/b][/color]\n"
                f"[color=8a8a9a][size=12]{cat['desc']}[/size][/color]")

        btn = Button(
            text=text,
            markup=True,
            background_normal='',
            background_color=bg,
            size_hint=(1, None),
            height=dp(88),
            halign='center',
            valign='middle',
            padding=[dp(10), dp(10)],
        )
        btn.bind(size=btn.setter('text_size'))
        btn.bind(on_release=lambda b, c=cat: self._open_category(c))
        return btn

    def _make_action_btn(self, text: str, bg_color: tuple, callback) -> Button:
        btn = Button(
            text=f"[b]{text}[/b]",
            markup=True,
            background_normal='',
            background_color=bg_color,
            size_hint=(1, None),
            height=dp(60),
            halign='center',
            valign='middle',
        )
        btn.bind(on_release=lambda b: callback())
        return btn

    def _open_category(self, cat: dict):
        screen = self.manager.get_screen('category')
        screen.load_category(cat)
        self.manager.current = 'category'

    def _go_history(self):
        self.manager.current = 'history'

    def _show_about(self):
        from kivy.uix.popup import Popup
        from kivy.uix.label import Label
        content = Label(
            text=(
                "[b][color=00e5ff]Security Toolkit[/color][/b]\n\n"
                "[color=b0b0c0]A unified Android security testing toolkit.\n"
                "For authorized ethical hacking and CTF use only.\n\n"
                "Built with Kivy + pure Python\n"
                "Pure Python tools: socket, requests, paramiko[/color]"
            ),
            markup=True,
            halign='center',
            valign='middle',
        )
        content.bind(size=content.setter('text_size'))
        popup = Popup(title='About', content=content,
                      size_hint=(0.85, 0.5))
        popup.open()

    def _update_bg(self, *_):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    @staticmethod
    def _rgba_hex(rgba):
        r, g, b, _ = rgba
        return '{:02x}{:02x}{:02x}'.format(int(r*255), int(g*255), int(b*255))
