"""screens/ai_screen.py — AI Agent: report viewer + interactive chat."""
import threading
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.metrics import dp
from kivy.utils import get_color_from_hex as hx
from kivy.clock import Clock

from config import C, bg, flat_btn, hdr_label, SEVERITY_COLOR
from database.db import (
    get_scans, get_scan, get_findings, get_raw,
    get_conv, save_msg, get_cfg
)
from ai.agent import generate_report, chat


class AIScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self._scan_id  = None
        self._history  = []   # Claude conversation history
        self._context  = ''
        self._build()

    def _build(self):
        root = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(8))
        bg(root, C['bg'])

        # Scan selector
        top = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(8))
        top.add_widget(Label(text='Scan:', color=hx(C['text_dim']),
                             font_size='12sp', size_hint_x=None, width=dp(48)))
        self._picker = Spinner(
            text='Select a scan…',
            values=[],
            background_color=hx(C['bg_input']),
            color=hx(C['text']), font_size='12sp',
        )
        self._picker.bind(text=self._on_pick)
        self._report_btn = flat_btn('📊 Report', C['accent_purple'],
                                    font_size='12sp',
                                    size_hint_x=None, width=dp(90))
        self._report_btn.bind(on_press=self._gen_report)
        top.add_widget(self._picker)
        top.add_widget(self._report_btn)
        root.add_widget(top)

        # Findings badges row
        self._badges = BoxLayout(size_hint_y=None, height=dp(32), spacing=dp(6))
        root.add_widget(self._badges)

        # Chat area
        sv = ScrollView(size_hint_y=1)
        self._chat_out = TextInput(
            text='Select a scan above to load AI analysis and chat.\n',
            readonly=True, multiline=True,
            background_color=hx(C['bg']),
            foreground_color=hx(C['text']),
            font_size='12sp',
        )
        sv.add_widget(self._chat_out)
        root.add_widget(sv)

        # Input row
        inp_row = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(6))
        self._inp = TextInput(
            hint_text='Ask the AI about this scan…',
            multiline=False,
            background_color=hx(C['bg_input']),
            foreground_color=hx(C['text']),
            hint_text_color=hx(C['text_dim']),
            font_size='12sp',
        )
        send_btn = flat_btn('▶', C['accent_red'],
                            size_hint_x=None, width=dp(52))
        send_btn.bind(on_press=self._send)
        inp_row.add_widget(self._inp)
        inp_row.add_widget(send_btn)
        root.add_widget(inp_row)
        self.add_widget(root)

    def on_enter(self):
        self._refresh_picker()

    def _refresh_picker(self):
        scans = get_scans(30)
        self._picker.values = [
            f'{s["id"]} | {s["target"]} [{s["risk"]}]' for s in scans
        ]
        if not self._picker.values:
            self._picker.text = 'No scans yet'

    def load_scan(self, scan_id):
        """Called from Dashboard to open a specific scan."""
        self._scan_id = scan_id
        scans = get_scans(30)
        for s in scans:
            if s['id'] == scan_id:
                self._picker.text = f'{s["id"]} | {s["target"]} [{s["risk"]}]'
                break
        self._load_scan_data(scan_id)

    def _on_pick(self, spinner, text):
        try:
            scan_id = int(text.split('|')[0].strip())
            self._scan_id = scan_id
            self._load_scan_data(scan_id)
        except:
            pass

    def _load_scan_data(self, scan_id):
        scan     = get_scan(scan_id)
        findings = get_findings(scan_id)
        conv     = get_conv(scan_id)
        raw_rows = get_raw(scan_id)

        # Build context string for AI
        raw_text = '\n'.join(r['output'] for r in raw_rows)
        self._context = raw_text[:6000]

        # Rebuild history from DB
        self._history = [
            {'role': r['role'], 'content': r['content']} for r in conv
        ]

        # Update badges
        counts = {}
        for f in findings:
            counts[f['severity']] = counts.get(f['severity'], 0) + 1
        self._badges.clear_widgets()
        for sev, cnt in sorted(counts.items()):
            color = SEVERITY_COLOR.get(sev, C['text_dim'])
            lbl = Label(
                text=f'[b][color={color[1:]}]{sev} ({cnt})[/color][/b]',
                markup=True, font_size='11sp',
                size_hint_x=None, width=dp(110))
            self._badges.add_widget(lbl)

        # Display in chat
        self._chat_out.text = ''
        target = scan['target'] if scan else ''
        self._append(f'🔴 Target: {target}  |  Risk: {scan["risk"]}\n\n')

        if findings:
            self._append('📋 FINDINGS:\n')
            for f in findings:
                color = SEVERITY_COLOR.get(f['severity'], C['text_dim'])
                self._append(f'[{f["severity"]}] {f["title"]}\n')
                self._append(f'     {f["detail"]}\n\n')

        # Replay prior conversation
        for msg in conv:
            prefix = '👤 You' if msg['role'] == 'user' else '🤖 RedAmon AI'
            self._append(f'\n{prefix}:\n{msg["content"]}\n')

        if not findings and not conv:
            self._append('No AI analysis yet.\nRun a scan first, or press Report.\n')

    def _send(self, *a):
        if not self._scan_id:
            self._append('[!] Select a scan first.\n'); return
        msg = self._inp.text.strip()
        if not msg: return
        self._inp.text = ''

        self._append(f'\n👤 You:\n{msg}\n')
        self._append('🤖 RedAmon AI: thinking…\n')
        save_msg(self._scan_id, 'user', msg)

        api_key = get_cfg('api_key', '')
        model   = get_cfg('model',   'claude-haiku-4-5-20251001')
        scan    = get_scan(self._scan_id)
        target  = scan['target'] if scan else ''
        history = list(self._history)

        def _worker():
            reply = chat(api_key, model, history, msg, target, self._context)
            self._history.append({'role': 'user',      'content': msg})
            self._history.append({'role': 'assistant', 'content': reply})
            save_msg(self._scan_id, 'assistant', reply)
            Clock.schedule_once(
                lambda dt: self._append(f'\n🤖 RedAmon AI:\n{reply}\n'), 0)

        threading.Thread(target=_worker, daemon=True).start()

    def _gen_report(self, *a):
        if not self._scan_id:
            self._append('[!] Select a scan first.\n'); return
        self._append('\n📊 Generating full pentest report…\n')
        api_key = get_cfg('api_key', '')
        model   = get_cfg('model',   'claude-haiku-4-5-20251001')
        scan    = get_scan(self._scan_id)
        target  = scan['target'] if scan else ''
        findings = get_findings(self._scan_id)
        findings_txt = '\n'.join(
            f'[{f["severity"]}] {f["title"]}: {f["detail"]}' for f in findings
        )

        def _worker():
            report = generate_report(api_key, model, target,
                                     findings_txt, self._context)
            save_msg(self._scan_id, 'assistant', report)
            Clock.schedule_once(
                lambda dt: self._append(f'\n📊 PENTEST REPORT:\n{report}\n'), 0)

        threading.Thread(target=_worker, daemon=True).start()

    def _append(self, text):
        self._chat_out.text += text
