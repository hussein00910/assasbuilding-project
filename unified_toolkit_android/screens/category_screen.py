"""
CategoryScreen — Shows all options/tools within a selected category.
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp


class CategoryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_cat = None
        self._root = BoxLayout(orientation='vertical', spacing=0)
        self.add_widget(self._root)

    def load_category(self, cat: dict):
        self.current_cat = cat
        self._root.clear_widgets()

        with self.canvas.before:
            Color(0.05, 0.05, 0.08, 1)
            self.bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=lambda *a: setattr(self.bg, 'pos', self.pos),
                  size=lambda *a: setattr(self.bg, 'size', self.size))

        # ── Header ────────────────────────────────────
        ACCENT = {
            'cyan':   '00e5ff', 'green':  '00ff80', 'purple': 'cc00ff',
            'teal':   '00e5cc', 'orange': 'ff8000', 'red':    'ff3333',
            'yellow': 'ffd700', 'blue':   '3399ff', 'lime':   '99e600',
        }
        hex_color = ACCENT.get(cat.get('color', 'cyan'), '00e5ff')

        header = BoxLayout(orientation='vertical',
                           size_hint_y=None, height=dp(90),
                           padding=[dp(16), dp(12)])
        with header.canvas.before:
            Color(0.0, 0.0, 0.0, 0.5)
            hdr_rect = Rectangle(pos=header.pos, size=header.size)
        header.bind(pos=lambda *a: setattr(hdr_rect, 'pos', header.pos),
                    size=lambda *a: setattr(hdr_rect, 'size', header.size))

        title_lbl = Label(
            text=f"[color={hex_color}][b]{cat['icon']} {cat['name']}[/b][/color]",
            markup=True,
            font_size='20sp',
            halign='left',
            size_hint_y=None, height=dp(35),
        )
        title_lbl.bind(size=title_lbl.setter('text_size'))

        desc_lbl = Label(
            text=f"[color=607d8b]{cat['desc']}[/color]",
            markup=True,
            font_size='13sp',
            halign='left',
            size_hint_y=None, height=dp(22),
        )
        desc_lbl.bind(size=desc_lbl.setter('text_size'))

        header.add_widget(title_lbl)
        header.add_widget(desc_lbl)
        self._root.add_widget(header)

        # ── Option list ───────────────────────────────────
        scroll = ScrollView(size_hint=(1, 1))
        options_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(8),
            padding=[dp(12), dp(12)],
            size_hint_y=None,
        )
        options_layout.bind(minimum_height=options_layout.setter('height'))

        for i, opt in enumerate(cat.get('options', [])):
            btn = self._make_option_btn(opt, i, hex_color)
            options_layout.add_widget(btn)

        scroll.add_widget(options_layout)
        self._root.add_widget(scroll)

        # ── Back button ───────────────────────────────────
        back_btn = Button(
            text="[b]← Back[/b]",
            markup=True,
            background_normal='',
            background_color=(0.1, 0.1, 0.15, 1),
            size_hint=(1, None),
            height=dp(50),
        )
        back_btn.bind(on_release=lambda b: self._go_back())
        self._root.add_widget(back_btn)

    def _make_option_btn(self, opt: dict, idx: int, hex_color: str) -> Button:
        text = (
            f"[b][color={hex_color}]{opt['icon']}  {opt['name']}[/color][/b]\n"
            f"[color=8a8a9a][size=13]{opt['description']}[/size][/color]"
        )
        btn = Button(
            text=text,
            markup=True,
            background_normal='',
            background_color=(0.08, 0.09, 0.13, 1),
            size_hint=(1, None),
            height=dp(70),
            halign='left',
            valign='middle',
            padding=[dp(16), dp(8)],
        )
        btn.bind(size=btn.setter('text_size'))
        btn.bind(on_release=lambda b, o=opt: self._open_tool(o))
        return btn

    def _open_tool(self, opt: dict):
        screen = self.manager.get_screen('tool')
        screen.load_option(opt, self.current_cat)
        self.manager.current = 'tool'

    def _go_back(self):
        self.manager.current = 'home'
