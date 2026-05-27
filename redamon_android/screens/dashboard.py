"""screens/dashboard.py — Main dashboard: scan list + stats."""
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp
from kivy.utils import get_color_from_hex as hx
from kivy.clock import Clock

from config import C, bg, flat_btn, hdr_label, SEVERITY_COLOR
from database.db import get_scans, get_findings, delete_scan


class ScanCard(BoxLayout):
    """One row in the scan list."""
    def __init__(self, scan, on_open, on_delete, **kw):
        super().__init__(orientation='horizontal',
                         size_hint_y=None, height=dp(72),
                         padding=dp(10), spacing=dp(8), **kw)
        bg(self, C['bg_card'])

        risk_color = {
            'CRITICAL': C['danger'],   'HIGH': C['warning'],
            'MEDIUM':   C['accent_yellow'], 'LOW': C['accent_green'],
        }.get(scan['risk'], C['text_dim'])

        info = BoxLayout(orientation='vertical')
        target_lbl = Label(
            text=f'[b]{scan["target"]}[/b]', markup=True,
            font_size='13sp', color=hx(C['text']),
            halign='left', valign='middle')
        target_lbl.bind(size=target_lbl.setter('text_size'))

        meta_lbl = Label(
            text=f'[color={risk_color[1:]}]{scan["risk"]}[/color]  •  '
                 f'[color=64748b]{scan["status"]}  •  '
                 f'{scan["created"][:16]}[/color]',
            markup=True, font_size='11sp', color=hx(C['text_dim']),
            halign='left', valign='middle')
        meta_lbl.bind(size=meta_lbl.setter('text_size'))

        info.add_widget(target_lbl)
        info.add_widget(meta_lbl)

        open_btn = flat_btn('🔍', C['btn_active'] if hasattr(C,'btn_active') else C['accent_blue'],
                            size_hint_x=None, width=dp(44))
        del_btn  = flat_btn('🗑', C['danger'],
                            size_hint_x=None, width=dp(44))
        open_btn.bind(on_press=lambda *a: on_open(scan['id']))
        del_btn.bind( on_press=lambda *a: on_delete(scan['id']))

        # fix colour ref
        open_btn.background_color = hx(C['accent_blue'])

        self.add_widget(info)
        self.add_widget(open_btn)
        self.add_widget(del_btn)


class DashboardScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self._root = BoxLayout(orientation='vertical',
                               padding=dp(12), spacing=dp(10))
        bg(self._root, C['bg'])
        self.add_widget(self._root)
        self._build()
        Clock.schedule_interval(lambda dt: self._refresh(), 5)

    def on_enter(self):
        self._refresh()

    def _build(self):
        # Stats row
        self._stats = GridLayout(cols=3, size_hint_y=None, height=dp(72),
                                 spacing=dp(8))
        self._root.add_widget(self._stats)

        self._root.add_widget(hdr_label('📁 Recent Scans'))

        sv = ScrollView()
        self._list = BoxLayout(orientation='vertical',
                               size_hint_y=None, spacing=dp(6))
        self._list.bind(minimum_height=self._list.setter('height'))
        sv.add_widget(self._list)
        self._root.add_widget(sv)

    def _stat_card(self, value, label, color):
        box = BoxLayout(orientation='vertical', padding=dp(8))
        bg(box, C['bg_card'])
        v = Label(text=f'[b]{value}[/b]', markup=True,
                  font_size='20sp', color=hx(color),
                  size_hint_y=None, height=dp(34))
        l = Label(text=label, font_size='11sp', color=hx(C['text_dim']),
                  size_hint_y=None, height=dp(22))
        box.add_widget(v); box.add_widget(l)
        return box

    def _refresh(self):
        scans = get_scans(50)
        total = len(scans)
        done  = sum(1 for s in scans if s['status'] == 'done')
        high  = sum(1 for s in scans if s['risk'] in ('CRITICAL','HIGH'))

        self._stats.clear_widgets()
        self._stats.add_widget(self._stat_card(str(total), 'Total Scans',   C['accent_blue']))
        self._stats.add_widget(self._stat_card(str(done),  'Completed',      C['accent_green']))
        self._stats.add_widget(self._stat_card(str(high),  'High Risk',      C['accent_red']))

        self._list.clear_widgets()
        if not scans:
            self._list.add_widget(
                Label(text='No scans yet. Go to 🔍 Scan to start.',
                      color=hx(C['text_dim']), font_size='13sp',
                      size_hint_y=None, height=dp(60)))
        for s in scans:
            self._list.add_widget(
                ScanCard(s, self._open_scan, self._delete_scan))

    def _open_scan(self, scan_id):
        app = self.manager.get_screen('ai')
        app.load_scan(scan_id)
        self.manager.current = 'ai'

    def _delete_scan(self, scan_id):
        delete_scan(scan_id)
        self._refresh()
