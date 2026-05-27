"""core/ui.py — All display functions (Rich-based)."""
import json
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.columns import Columns
from rich import box

console = Console()

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HISTORY_FILE = os.path.join(_BASE, 'data', 'history.json')

BANNER = r"""
  ┌────────────────────────────────────────────────────────────┐
  │  ██╗██╗  ██╗██╗██████╗██████╗ ██████╗ ██████╗  │
  │  ║ ██╔╝║  ██║║ █████╔╝║ ██╔═══██╗║ ╔════╝║ ╔════╝  │
  │  ║ ║  ║║  ██║║ ██╔══╝ ║ ██║  ██║║ ║     ║ ║███╗   │
  │  ║ ║  ║╚██╔██║║ ██╗   ║ ██║  ██║║ ║     ║ ╚══██╗  │
  │  ║██╗  ║ ╚═╝ ██║║ ██████╗╔██╝  ██╔╝╚██████╗╚██████╔╝  │
  │  ╚═╝  ═╝    ╚═╝╚═╝╚═════╝╚═╝  ╚═╝  ╚═════╝ ╚═════╝   │
  └────────────────────────────────────────────────────────────┘
      Unified Security Toolkit  —  For Authorized Use Only
"""

CATEGORY_COLORS = {
    'recon':       'cyan',
    'scanning':    'yellow',
    'exploitation':'red',
    'passwords':   'magenta',
    'web':         'blue',
    'phishing':    'orange3',
    'wireless':    'green',
    'network':     'white',
    'forensics':   'purple',
}


def clear():
    os.system('clear' if os.name != 'nt' else 'cls')


def show_banner(available: int, total: int):
    clear()
    console.print(BANNER, style='bold red')
    status_color = 'green' if available > total // 2 else 'yellow'
    console.print(
        f"  [{status_color}]✓ {available}/{total} tools installed[/{status_color}]  "
        f"[dim]| For authorized penetration testing only |[/dim]\n"
    )


def show_main_menu(modules: list, tool_status: dict):
    table = Table(
        title='[bold red]🔴 Main Menu[/bold red]',
        box=box.ROUNDED,
        border_style='red',
        show_header=True,
        header_style='bold white',
    )
    table.add_column('#',     style='bold yellow', width=4, justify='center')
    table.add_column('Category',  style='bold white',  width=28)
    table.add_column('Description',  style='dim white',  width=35)
    table.add_column('Options',  style='cyan',  width=8, justify='center')

    for i, m in enumerate(modules, 1):
        avail = sum(1 for t in m.get('tools', []) if tool_status.get(t))
        total = len(m.get('tools', []))
        stat  = f'[green]{avail}[/green]/[dim]{total}[/dim]'
        table.add_row(
            str(i),
            f"{m['icon']} {m['name']}",
            m['description'],
            f"[cyan]{m['option_count']}[/cyan]",
        )

    console.print(table)
    console.print(
        "\n  [bold yellow][T][/bold yellow] Show tools status   "
        "[bold yellow][H][/bold yellow] History   "
        "[bold yellow][Q][/bold yellow] Quit\n"
    )


def show_module_menu(name: str, icon: str, color: str, options: list):
    clear()
    console.print(Panel(
        f"[bold {color}]{icon} {name}[/bold {color}]",
        border_style=color, expand=False
    ))

    table = Table(box=box.SIMPLE, show_header=True,
                  header_style=f'bold {color}')
    table.add_column('#',      width=4,  justify='center')
    table.add_column('Option', width=30)
    table.add_column('Tool',   width=16, style='cyan')
    table.add_column('Command Preview', width=40, style='dim')
    table.add_column('',       width=3,  justify='center')

    for opt in options:
        avail_icon = '[green]✅[/green]' if opt['available'] else '[red]❌[/red]'
        cmd_prev   = opt.get('cmd', 'interactive')[:38]
        table.add_row(
            f"[bold yellow]{opt['index']}[/bold yellow]",
            opt['name'],
            opt.get('tool', '—'),
            cmd_prev,
            avail_icon,
        )

    console.print(table)
    console.print("  [bold yellow][0][/bold yellow] ← Back to main menu\n")


def show_tools_table(tool_status: dict):
    from core.checker import get_description
    clear()
    table = Table(
        title='[bold cyan]🔧 Installed Tools Status[/bold cyan]',
        box=box.ROUNDED, border_style='cyan',
        show_header=True, header_style='bold white',
    )
    table.add_column('Tool',        style='bold white', width=20)
    table.add_column('Status',      width=6,  justify='center')
    table.add_column('Description', style='dim', width=45)

    for tool, installed in sorted(tool_status.items()):
        icon = '[green]✅[/green]' if installed else '[red]❌[/red]'
        table.add_row(tool, icon, get_description(tool))

    console.print(table)
    input("\n  [Press ENTER to return]")


def show_history():
    clear()
    if not os.path.exists(HISTORY_FILE):
        console.print('[yellow]No history yet.[/yellow]')
        input("\n  [Press ENTER to return]")
        return

    with open(HISTORY_FILE) as f:
        history = json.load(f)

    if not history:
        console.print('[yellow]History is empty.[/yellow]')
        input("\n  [Press ENTER to return]")
        return

    table = Table(
        title='[bold cyan]📜 Command History[/bold cyan]',
        box=box.ROUNDED, border_style='cyan',
        show_header=True, header_style='bold white',
    )
    table.add_column('#',        width=5,  justify='right', style='dim')
    table.add_column('Time',     width=20, style='dim')
    table.add_column('Command',  width=50, style='cyan')
    table.add_column('Preview',  width=35, style='dim')

    for i, entry in enumerate(reversed(history[-50:]), 1):
        prev = entry.get('preview', '')[:33].replace('\n', ' ')
        table.add_row(str(i), entry['time'], entry['command'], prev)

    console.print(table)
    input("\n  [Press ENTER to return]")
