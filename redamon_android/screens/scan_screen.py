"""screens/scan_screen.py — New scan: options + live output + auto-AI."""
import threading
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.progressbar import ProgressBar
from kivy.metrics import dp
from kivy.utils import get_color_from_hex as hx
from kivy.clock import Clock

from config import C, bg, flat_btn, hdr_label
from database.db import (
    create_scan, update_scan, save_finding,
    save_raw, save_msg, get_cfg
)
from tools.recon_engine import (
    port_scan, subdomain_enum, dns_lookup, ssl_check,
    header_analysis, tech_detect, dir_bruteforce,
    whois_lookup, web_crawl
)
from ai.agent import analyze_scan, parse_findings, extract_risk, generate_report
from utils.worker import run_parallel


TOOLS = [
    ('port_scan',      '📡 Port Scanner',       True),
    ('subdomain',      '🌐 Subdomain Enum',     True),
    ('dns',            '📌 DNS Lookup',          True),
    ('ssl',            '🔒 SSL/TLS Check',      True),
    ('headers',        '📊 Header Analysis',    True),
    ('tech',           '🔎 Tech Detection',     True),
    ('dirb',           '📂 Dir Brute-Force',    False),
    ('whois',          '📗 WHOIS Lookup',       False),
    ('crawl',          '🕷️ Web Crawler',       False),
]


class ScanScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self._scan_id = None
        self._raw_buf = {}
        self._active  = False
        self._build()

    def _build(self):
        root = BoxLayout(orientation='vertical', padding=dp(12), spacing=dp(8))
        bg(root, C['bg'])

        root.add_widget(hdr_label('🔍 New Reconnaissance Scan'))

        # Target input
        input_row = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(8))
        self._target = TextInput(
            hint_text='Target: IP, domain, or URL — e.g. 192.168.1.1',
            multiline=False,
            background_color=hx(C['bg_input']),
            foreground_color=hx(C['text']),
            hint_text_color=hx(C['text_dim']),
            cursor_color=hx(C['accent_red']),
            font_size='13sp',
        )
        input_row.add_widget(self._target)
        root.add_widget(input_row)

        # Tool checkboxes
        root.add_widget(Label(
            text='Select tools:', color=hx(C['text_dim']),
            font_size='12sp', size_hint_y=None, height=dp(24),
            halign='left'))

        grid = GridLayout(cols=2, size_hint_y=None, spacing=dp(4))
        grid.bind(minimum_height=grid.setter('height'))
        self._tool_vars = {}
        for key, label, default in TOOLS:
            row = BoxLayout(size_hint_y=None, height=dp(34))
            cb = CheckBox(active=default,
                          color=hx(C['accent_red']),
                          size_hint_x=None, width=dp(34))
            lbl = Label(text=label, font_size='12sp',
                        color=hx(C['text']), halign='left')
            lbl.bind(size=lbl.setter('text_size'))
            row.add_widget(cb); row.add_widget(lbl)
            grid.add_widget(row)
            self._tool_vars[key] = cb
        root.add_widget(grid)

        # Progress bar
        self._progress = ProgressBar(max=100, value=0,
                                     size_hint_y=None, height=dp(8))
        root.add_widget(self._progress)

        # Buttons
        btn_row = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(8))
        self._run_btn = flat_btn('▶  Start Scan', C['accent_red'], font_size='13sp')
        self._clr_btn = flat_btn('🗑  Clear',      C['bg_card'],   C['text_dim'], font_size='12sp')
        self._run_btn.bind(on_press=self._start)
        self._clr_btn.bind(on_press=lambda *a: self._clear_output())
        btn_row.add_widget(self._run_btn)
        btn_row.add_widget(self._clr_btn)
        root.add_widget(btn_row)

        # Live output
        sv = ScrollView()
        self._out = TextInput(
            text='RedAmon ready. Enter a target and start scan.\n',
            readonly=True, multiline=True,
            background_color=hx(C['bg']),
            foreground_color=hx(C['accent_green']),
            font_size='11sp',
        )
        sv.add_widget(self._out)
        root.add_widget(sv)
        self.add_widget(root)

    # ── Scan Logic ─────────────────────────────────────────────────────
    def _start(self, *a):
        target = self._target.text.strip()
        if not target:
            self._write('[!] Enter a target first.\n'); return
        if self._active:
            self._write('[!] Scan already running.\n'); return

        self._active = True
        self._raw_buf.clear()
        self._clear_output()
        self._run_btn.text = '⏳ Scanning…'
        self._run_btn.disabled = True
        self._progress.value = 0

        # Determine which tools to run
        host = target.replace('https://','').replace('http://','').split('/')[0]
        url  = target if target.startswith('http') else f'http://{target}'
        port_range_end = 1024

        tasks = []
        if self._tool_vars['port_scan'].active:
            tasks.append((port_scan,     (host, 1, port_range_end, 0.4), 'Port Scanner'))
        if self._tool_vars['subdomain'].active:
            tasks.append((subdomain_enum,(host,),                        'Subdomain Enum'))
        if self._tool_vars['dns'].active:
            tasks.append((dns_lookup,    (host,),                        'DNS Lookup'))
        if self._tool_vars['ssl'].active:
            tasks.append((ssl_check,     (host,),                        'SSL Check'))
        if self._tool_vars['headers'].active:
            tasks.append((header_analysis,(url,),                        'Headers'))
        if self._tool_vars['tech'].active:
            tasks.append((tech_detect,   (url,),                         'Tech Detect'))
        if self._tool_vars['dirb'].active:
            tasks.append((dir_bruteforce,(url,),                         'Dir Brute'))
        if self._tool_vars['whois'].active:
            tasks.append((whois_lookup,  (host,),                        'WHOIS'))
        if self._tool_vars['crawl'].active:
            tasks.append((web_crawl,     (url,),                         'Crawler'))

        self._scan_id = create_scan(target)
        total = len(tasks)
        done_count = [0]

        def on_line(label, line):
            self._raw_buf.setdefault(label, [])
            self._raw_buf[label].append(line)
            self._write(f'[{label}] {line}')

        def on_all_done():
            done_count[0] += 1
            # Save raw output
            full_raw = '\n'.join(
                f'=== {lbl} ===\n' + ''.join(lines)
                for lbl, lines in self._raw_buf.items()
            )
            save_raw(self._scan_id, 'all_tools', full_raw)
            self._progress.value = 60
            self._write('\n── All tools done. Running AI analysis… ──\n')
            self._run_ai(target, full_raw)

        run_parallel(tasks, on_line=on_line, on_all_done=on_all_done)

    def _run_ai(self, target, raw):
        api_key = get_cfg('api_key', '')
        model   = get_cfg('model',   'claude-haiku-4-5-20251001')

        def _worker():
            analysis = analyze_scan(api_key, model, target, raw)
            Clock.schedule_once(lambda dt: self._on_ai_done(
                target, analysis, raw), 0)

        threading.Thread(target=_worker, daemon=True).start()

    def _on_ai_done(self, target, analysis, raw):
        self._progress.value = 85
        # Parse and save findings
        findings = parse_findings(analysis)
        risk     = extract_risk(analysis)
        for f in findings:
            save_finding(self._scan_id, 'AI Agent',
                         f['severity'], f['title'], f['detail'])
        update_scan(self._scan_id, status='done', risk=risk,
                    summary=analysis[:500])
        save_msg(self._scan_id, 'assistant',
                 f'Initial analysis complete.\n\n{analysis}')

        self._write(f'\n── AI Analysis Complete ──\n')
        self._write(f'Risk Level: {risk}\n')
        self._write(f'Findings: {len(findings)} issue(s) identified\n')
        self._write('\n▶ Go to 🤖 AI screen to view full report & chat\n')
        self._progress.value = 100
        self._run_btn.text = '▶  Start Scan'
        self._run_btn.disabled = False
        self._active = False

    def _write(self, text):
        self._out.text += text

    def _clear_output(self):
        self._out.text = ''
        self._progress.value = 0
