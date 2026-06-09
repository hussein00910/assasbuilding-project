"""
HistoryScreen — Shows scan history from SQLite.
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp


class HistoryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._root = BoxLayout(orientation='vertical')
        self.add_widget(self._root)

    def on_pre_enter(self, *args):
        self._build_ui()

    def _build_ui(self):
        self._root.clear_widgets()

        with self.canvas.before:
            Color(0.05, 0.05, 0.08, 1)
            self.bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=lambda *a: setattr(self.bg, 'pos', self.pos),
                  size=lambda *a: setattr(self.bg, 'size', self.size))

        # Header
        header = BoxLayout(size_hint_y=None, height=dp(56),
                           padding=[dp(14), dp(8)])
        with header.canvas.before:
            Color(0.0, 0.0, 0.0, 0.5)
            hr = Rectangle(pos=header.pos, size=header.size)
        header.bind(pos=lambda *a: setattr(hr, 'pos', header.pos),
                    size=lambda *a: setattr(hr, 'size', header.size))

        header.add_widget(Label(
            text="[b][color=ffd700]📜 Scan History[/color][/b]",
            markup=True, font_size='18sp',
            halign='left',
        ))
        self._root.add_widget(header)

        # Scroll list
        from utils.storage import get_history
        rows = get_history(50)

        scroll = ScrollView(size_hint=(1, 1))
        items_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(6),
            padding=[dp(10), dp(10)],
            size_hint_y=None,
        )
        items_layout.bind(minimum_height=items_layout.setter('height'))

        if not rows:
            items_layout.add_widget(Label(
                text="[color=607d8b]No history yet. Run some tools first.[/color]",
                markup=True, font_size='14sp',
                size_hint=(1, None), height=dp(50),
            ))
        else:
            for row in rows:
                btn = self._make_row_btn(row)
                items_layout.add_widget(btn)

        scroll.add_widget(items_layout)
        self._root.add_widget(scroll)

        # Buttons
        btn_row = BoxLayout(size_hint_y=None, height=dp(54),
                            spacing=dp(8), padding=[dp(10), dp(4)])

        back_btn = Button(
            text="← Back",
            background_normal='',
            background_color=(0.12, 0.12, 0.18, 1),
            size_hint=(0.5, 1),
        )
        back_btn.bind(on_release=lambda b: setattr(self.manager, 'current', 'home'))

        clear_btn = Button(
            text="🗑 Clear All",
            background_normal='',
            background_color=(0.35, 0.1, 0.1, 1),
            size_hint=(0.5, 1),
        )
        clear_btn.bind(on_release=lambda b: self._confirm_clear())

        btn_row.add_widget(back_btn)
        btn_row.add_widget(clear_btn)
        self._root.add_widget(btn_row)

    def _make_row_btn(self, row: dict) -> Button:
        text = (
            f"[b][color=00e5ff]{row['tool']}[/color][/b]  "
            f"[color=8a8a9a]{row['category']}[/color]\n"
            f"[color=b0b0c0]{row['target'][:35]}[/color]  "
            f"[color=607d8b]{row['ts']}[/color]"
        )
        btn = Button(
            text=text,
            markup=True,
            background_normal='',
            background_color=(0.08, 0.09, 0.13, 1),
            size_hint=(1, None),
            height=dp(64),
            halign='left',
            valign='middle',
            padding=[dp(12), dp(8)],
        )
        btn.bind(size=btn.setter('text_size'))
        btn.bind(on_release=lambda b, r=row: self._show_detail(r))
        return btn

    def _show_detail(self, row: dict):
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(8))

        info = Label(
            text=(f"[b]Tool:[/b] {row['tool']}\n"
                  f"[b]Target:[/b] {row['target']}\n"
                  f"[b]Time:[/b] {row['ts']}"),
            markup=True,
            font_size='13sp',
            halign='left',
            size_hint_y=None, height=dp(70),
        )
        info.bind(size=info.setter('text_size'))
        content.add_widget(info)

        scroll = ScrollView(size_hint=(1, 1))
        out_lbl = Label(
            text=row['output'][:3000],
            font_size='12sp',
            halign='left',
            valign='top',
            color=(0.7, 1.0, 0.7, 1),
            size_hint=(1, None),
        )
        out_lbl.bind(texture_size=out_lbl.setter('size'))
        out_lbl.text_size = (None, None)
        scroll.add_widget(out_lbl)
        content.add_widget(scroll)

        popup = Popup(
            title=f"Result: {row['tool']}",
            content=content,
            size_hint=(0.95, 0.85),
        )
        popup.open()

    def _confirm_clear(self):
        from utils.storage import delete_all
        content = BoxLayout(orientation='vertical', padding=dp(16), spacing=dp(12))
        content.add_widget(Label(
            text="Delete all scan history?",
            font_size='15sp',
        ))
        btns = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(8))

        popup = Popup(title='Confirm', content=content, size_hint=(0.7, 0.4))

        cancel_btn = Button(text="Cancel", background_normal='',
                            background_color=(0.2, 0.2, 0.3, 1))
        cancel_btn.bind(on_release=lambda b: popup.dismiss())

        ok_btn = Button(text="Delete", background_normal='',
                        background_color=(0.5, 0.1, 0.1, 1))
        def _do_clear(b):
            delete_all()
            popup.dismiss()
            self._build_ui()
        ok_btn.bind(on_release=_do_clear)

        btns.add_widget(cancel_btn)
        btns.add_widget(ok_btn)
        content.add_widget(btns)
        popup.open()
