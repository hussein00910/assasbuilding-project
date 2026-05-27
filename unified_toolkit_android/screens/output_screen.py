"""
OutputScreen — Runs the tool in a background thread and streams output.
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.clock import Clock
import queue
import threading


class OutputScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._output_lines = []
        self._q = queue.Queue()
        self._running = False
        self.current_opt = None
        self.current_cat = None
        self.current_params = None
        self._full_output = ""

        self._root = BoxLayout(orientation='vertical', spacing=0)
        self.add_widget(self._root)

    def execute(self, opt: dict, cat: dict, params: dict):
        self.current_opt = opt
        self.current_cat = cat
        self.current_params = params
        self._output_lines = []
        self._full_output = ""
        self._running = True
        self._q = queue.Queue()

        self._build_ui(opt, cat)
        self._start_tool(opt, params)

    def _build_ui(self, opt: dict, cat: dict):
        self._root.clear_widgets()

        with self.canvas.before:
            Color(0.03, 0.04, 0.06, 1)
            self.bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=lambda *a: setattr(self.bg, 'pos', self.pos),
                  size=lambda *a: setattr(self.bg, 'size', self.size))

        ACCENT = {
            'cyan':   '00e5ff', 'green':  '00ff80', 'purple': 'cc00ff',
            'teal':   '00e5cc', 'orange': 'ff8000', 'red':    'ff3333',
            'yellow': 'ffd700', 'blue':   '3399ff', 'lime':   '99e600',
        }
        hex_color = ACCENT.get(cat.get('color', 'cyan'), '00e5ff')

        # Header
        header = BoxLayout(size_hint_y=None, height=dp(54),
                           padding=[dp(14), dp(8)])
        with header.canvas.before:
            Color(0.0, 0.0, 0.0, 0.5)
            hr = Rectangle(pos=header.pos, size=header.size)
        header.bind(pos=lambda *a: setattr(hr, 'pos', header.pos),
                    size=lambda *a: setattr(hr, 'size', header.size))

        self.status_lbl = Label(
            text=f"[color={hex_color}][b]⚙ Running: {opt['name']}[/b][/color]",
            markup=True,
            font_size='15sp',
            halign='left',
        )
        self.status_lbl.bind(size=self.status_lbl.setter('text_size'))
        header.add_widget(self.status_lbl)
        self._root.add_widget(header)

        # Output area
        self._scroll = ScrollView(size_hint=(1, 1))
        self._out_label = Label(
            text="",
            markup=False,
            font_size='13sp',
            font_name='RobotoMono-Regular',
            halign='left',
            valign='top',
            text_size=(None, None),
            size_hint=(1, None),
            color=(0.8, 1.0, 0.8, 1),
            padding=[dp(10), dp(10)],
        )
        self._out_label.bind(texture_size=self._out_label.setter('size'))
        self._scroll.add_widget(self._out_label)
        self._root.add_widget(self._scroll)

        # Buttons
        btn_row = BoxLayout(size_hint_y=None, height=dp(54),
                            spacing=dp(8), padding=[dp(10), dp(4)])

        back_btn = Button(
            text="← Back",
            background_normal='',
            background_color=(0.12, 0.12, 0.18, 1),
            size_hint=(0.33, 1),
            font_size='14sp',
        )
        back_btn.bind(on_release=lambda b: self._go_back())

        self.save_btn = Button(
            text="💾 Save",
            background_normal='',
            background_color=(0.1, 0.3, 0.15, 1),
            size_hint=(0.33, 1),
            font_size='14sp',
        )
        self.save_btn.bind(on_release=lambda b: self._save_result())

        self.stop_btn = Button(
            text="⏹ Stop",
            background_normal='',
            background_color=(0.35, 0.1, 0.1, 1),
            size_hint=(0.34, 1),
            font_size='14sp',
        )
        self.stop_btn.bind(on_release=lambda b: self._stop())

        btn_row.add_widget(back_btn)
        btn_row.add_widget(self.save_btn)
        btn_row.add_widget(self.stop_btn)
        self._root.add_widget(btn_row)

        # Start polling the queue
        Clock.schedule_interval(self._poll_queue, 0.05)

    def _start_tool(self, opt: dict, params: dict):
        func = opt.get('func')
        if not func:
            self._q.put("[!] No function defined for this option.")
            self._q.put(None)  # sentinel
            return

        # Build kwargs from params
        kwargs = {}
        for p in opt.get('params', []):
            key = p['key']
            val = params.get(key, p.get('default', ''))
            # Convert numeric hints
            if key in ('port', 'max_hops', 'depth') and str(val).isdigit():
                val = int(val)
            kwargs[key] = val

        def _thread():
            try:
                output = func(
                    progress_cb=lambda line: self._q.put(line),
                    **kwargs
                )
                self._full_output = output or ""
            except Exception as e:
                self._q.put(f"[!] Error: {e}")
            finally:
                self._q.put(None)  # sentinel = done

        t = threading.Thread(target=_thread, daemon=True)
        t.start()

    def _poll_queue(self, dt):
        try:
            while True:
                item = self._q.get_nowait()
                if item is None:
                    # Done
                    self._running = False
                    self.status_lbl.text = "[color=00ff80][b]✔ Done[/b][/color]"
                    Clock.unschedule(self._poll_queue)
                    return
                self._output_lines.append(item)
                # Keep last 500 lines to avoid OOM
                if len(self._output_lines) > 500:
                    self._output_lines = self._output_lines[-500:]
                self._out_label.text = "\n".join(self._output_lines)
                # Auto-scroll to bottom
                self._scroll.scroll_y = 0
        except Exception:
            pass

    def _stop(self):
        self._running = False
        self._q.put(None)

    def _save_result(self):
        from utils.storage import save_result
        opt = self.current_opt or {}
        cat = self.current_cat or {}
        params = self.current_params or {}
        target = str(params.get('target') or params.get('url') or
                     params.get('host') or params.get('domain') or params.get('ip') or 'N/A')
        output = "\n".join(self._output_lines)
        save_result(
            category=cat.get('name', 'Unknown'),
            tool=opt.get('name', 'Unknown'),
            target=target,
            output=output,
        )
        self.save_btn.text = "✔ Saved!"
        Clock.schedule_once(lambda dt: setattr(self.save_btn, 'text', '💾 Save'), 2)

    def _go_back(self):
        Clock.unschedule(self._poll_queue)
        self.manager.current = 'tool'
