"""
ToolScreen — Input form for a selected tool option.
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp


class ToolScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_opt = None
        self.current_cat = None
        self.param_inputs = {}
        self._root = BoxLayout(orientation='vertical', spacing=0)
        self.add_widget(self._root)

    def load_option(self, opt: dict, cat: dict):
        self.current_opt = opt
        self.current_cat = cat
        self.param_inputs = {}
        self._root.clear_widgets()

        with self.canvas.before:
            Color(0.05, 0.05, 0.08, 1)
            self.bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=lambda *a: setattr(self.bg, 'pos', self.pos),
                  size=lambda *a: setattr(self.bg, 'size', self.size))

        ACCENT = {
            'cyan':   '00e5ff', 'green':  '00ff80', 'purple': 'cc00ff',
            'teal':   '00e5cc', 'orange': 'ff8000', 'red':    'ff3333',
            'yellow': 'ffd700', 'blue':   '3399ff', 'lime':   '99e600',
        }
        hex_color = ACCENT.get(cat.get('color', 'cyan'), '00e5ff')

        # ── Header ────────────────────────────────────
        header = BoxLayout(orientation='vertical',
                           size_hint_y=None, height=dp(85),
                           padding=[dp(16), dp(10)])
        with header.canvas.before:
            Color(0.0, 0.0, 0.0, 0.5)
            hdr_rect = Rectangle(pos=header.pos, size=header.size)
        header.bind(pos=lambda *a: setattr(hdr_rect, 'pos', header.pos),
                    size=lambda *a: setattr(hdr_rect, 'size', header.size))

        header.add_widget(Label(
            text=f"[b][color={hex_color}]{opt['icon']} {opt['name']}[/color][/b]",
            markup=True, font_size='18sp',
            halign='left', size_hint_y=None, height=dp(32),
        ))
        desc = Label(
            text=f"[color=607d8b]{opt['description']}[/color]",
            markup=True, font_size='13sp',
            halign='left', size_hint_y=None, height=dp(22),
        )
        desc.bind(size=desc.setter('text_size'))
        header.add_widget(desc)
        self._root.add_widget(header)

        # ── Parameter form ─────────────────────────────────
        scroll = ScrollView(size_hint=(1, 1))
        form = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            padding=[dp(14), dp(14)],
            size_hint_y=None,
        )
        form.bind(minimum_height=form.setter('height'))

        params = opt.get('params', [])

        if params:
            for param in params:
                key     = param['key']
                label   = param['label']
                hint    = param.get('hint', '')
                default = param.get('default', '')

                lbl = Label(
                    text=f"[color=b0b0c0]{label}[/color]",
                    markup=True,
                    font_size='14sp',
                    halign='left',
                    size_hint=(1, None),
                    height=dp(22),
                )
                lbl.bind(size=lbl.setter('text_size'))
                form.add_widget(lbl)

                inp = TextInput(
                    hint_text=hint,
                    text=default,
                    multiline=False,
                    background_color=(0.1, 0.1, 0.16, 1),
                    foreground_color=(0.9, 0.9, 0.9, 1),
                    hint_text_color=(0.45, 0.45, 0.5, 1),
                    cursor_color=(0.0, 0.9, 1.0, 1),
                    size_hint=(1, None),
                    height=dp(44),
                    padding=[dp(10), dp(10)],
                    font_size='15sp',
                )
                self.param_inputs[key] = inp
                form.add_widget(inp)
        else:
            # No params — just show a note
            form.add_widget(Label(
                text="[color=8a8a9a]This tool requires no input. Press RUN to execute.[/color]",
                markup=True, font_size='14sp',
                halign='center', size_hint=(1, None), height=dp(50),
            ))

        scroll.add_widget(form)
        self._root.add_widget(scroll)

        # ── Action buttons ─────────────────────────────────
        btn_row = BoxLayout(size_hint_y=None, height=dp(56),
                            spacing=dp(8), padding=[dp(10), dp(4)])

        back_btn = Button(
            text="← Back",
            background_normal='',
            background_color=(0.12, 0.12, 0.18, 1),
            size_hint=(0.35, 1),
            font_size='15sp',
        )
        back_btn.bind(on_release=lambda b: self._go_back())

        run_btn = Button(
            text=f"[b]▶  RUN[/b]",
            markup=True,
            background_normal='',
            background_color=(0.0, 0.55, 0.65, 1),
            size_hint=(0.65, 1),
            font_size='16sp',
        )
        run_btn.bind(on_release=lambda b: self._run_tool())

        btn_row.add_widget(back_btn)
        btn_row.add_widget(run_btn)
        self._root.add_widget(btn_row)

    def _run_tool(self):
        """Collect params and navigate to OutputScreen."""
        params = {k: inp.text.strip() for k, inp in self.param_inputs.items()}
        screen = self.manager.get_screen('output')
        screen.execute(self.current_opt, self.current_cat, params)
        self.manager.current = 'output'

    def _go_back(self):
        self.manager.current = 'category'
