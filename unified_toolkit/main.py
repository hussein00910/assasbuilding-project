#!/usr/bin/env python3
"""
██╗██╗  ██╗██╗██████╗ ██████╗██████╗ ██████╗
Unified Security Toolkit  v1.0
For authorized penetration testing only.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console
from rich.prompt import Prompt

from core.checker import check_all
from core import ui

# ── Import all modules ─────────────────────────────────────────────────
from modules.recon        import ReconModule
from modules.scanning     import ScanningModule
from modules.exploitation import ExploitationModule
from modules.passwords    import PasswordsModule
from modules.web          import WebModule
from modules.phishing     import PhishingModule
from modules.wireless     import WirelessModule
from modules.network      import NetworkModule
from modules.forensics    import ForensicsModule

console = Console()

MODULES = [
    ReconModule(),
    ScanningModule(),
    ExploitationModule(),
    PasswordsModule(),
    WebModule(),
    PhishingModule(),
    WirelessModule(),
    NetworkModule(),
    ForensicsModule(),
]

DISCLAIMER = """
┌───────────────────────────────────────────────────────────────┐
│  ⚠️  LEGAL DISCLAIMER — READ CAREFULLY                        │
│                                                              │
│  This toolkit is for AUTHORIZED security testing only.      │
│  • You must have written permission from the system owner.  │
│  • Unauthorized use is illegal in most jurisdictions.       │
│  • Suitable for: CTF, labs, your own systems only.          │
│                                                              │
│  The author accepts NO liability for misuse.                 │
└───────────────────────────────────────────────────────────────┘
"""


def show_disclaimer():
    console.print(DISCLAIMER, style='bold yellow')
    answer = input("  Do you agree? [yes/no]: ").strip().lower()
    if answer not in ('yes', 'y'):
        console.print('[red]Exiting.[/red]')
        sys.exit(0)


def main():
    show_disclaimer()

    # Check installed tools once at startup
    console.print('\n  [dim]Checking installed tools…[/dim]')
    tool_status = check_all()
    available   = sum(tool_status.values())
    total       = len(tool_status)

    # Pre-compute menu metadata for each module
    menu_items = [m.get_menu_info() for m in MODULES]

    # ------------------------------------------------------------------ #
    #  Main loop
    # ------------------------------------------------------------------ #
    while True:
        ui.show_banner(available, total)
        ui.show_main_menu(menu_items, tool_status)

        raw = input('  → ').strip().lower()

        # — Special commands —
        if raw in ('q', 'quit', 'exit'):
            console.print('\n[bold red]Goodbye.[/bold red]\n')
            sys.exit(0)

        if raw == 't':
            ui.show_tools_table(tool_status)
            continue

        if raw == 'h':
            ui.show_history()
            continue

        # — Direct tool name shortcut —
        # e.g. user types "nmap" and we find which module handles it
        if not raw.isdigit():
            matched = _find_module_by_tool(raw)
            if matched is not None:
                MODULES[matched].run(tool_status)
            else:
                console.print(f'[yellow]Unknown input: {raw!r}  (type 1-{len(MODULES)}, T, H, Q)[/yellow]')
            continue

        # — Numbered category selection —
        idx = int(raw)
        if 1 <= idx <= len(MODULES):
            MODULES[idx - 1].run(tool_status)
        else:
            console.print(f'[yellow]Enter 1–{len(MODULES)}.[/yellow]')


def _find_module_by_tool(name: str) -> int | None:
    """
    If the user types a tool name directly (e.g. 'nmap'),
    return the index of the module that owns it.
    """
    for i, m in enumerate(MODULES):
        if name in [t.lower() for t in m.TOOLS]:
            return i
        if name.lower() == m.NAME.lower():
            return i
    return None


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        console.print('\n\n[bold red]Interrupted.[/bold red]\n')
        sys.exit(0)
