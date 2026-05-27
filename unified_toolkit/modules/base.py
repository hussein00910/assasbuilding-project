"""modules/base.py — Abstract base class for every tool module."""
import os
from rich.console import Console
from core.executor import run_command
from core import ui

console = Console()


class BaseModule:
    """
    Every tool module inherits this class and only needs to define:
      NAME, ICON, COLOR, DESCRIPTION, TOOLS, OPTIONS
    """
    NAME: str         = ''
    ICON: str         = ''
    COLOR: str        = 'white'
    DESCRIPTION: str  = ''
    TOOLS: list       = []    # system tool names needed
    OPTIONS: list     = []    # list of option dicts (see below)
    """
    Option dict schema:
    {
        'name':          str,           # display name
        'tool':          str,           # system binary used
        'description':   str,           # one-line description
        'cmd':           str,           # command template, {param} placeholders
        'params':        list[str],     # ordered list of placeholder names
        'hints':         dict[str,str], # human-friendly prompt per param
        'requires_root': bool,          # warn if not root
        'interactive':   bool,          # launches interactive session
        'custom':        bool,          # user types entire command
    }
    """

    # ------------------------------------------------------------------ #
    def get_menu_info(self) -> dict:
        return {
            'name':         self.NAME,
            'icon':         self.ICON,
            'color':        self.COLOR,
            'description':  self.DESCRIPTION,
            'tools':        self.TOOLS,
            'option_count': len(self.OPTIONS),
        }

    def run(self, tool_status: dict):
        """Interactive option loop for this module."""
        while True:
            options = self._annotate(tool_status)
            ui.show_module_menu(self.NAME, self.ICON, self.COLOR, options)

            raw = input(f'  [{self.NAME}] → ').strip()
            if raw in ('0', 'b', 'back', 'q'):
                break

            if not raw.isdigit():
                console.print('[yellow]Enter a number.[/yellow]')
                continue

            idx = int(raw)
            if not (1 <= idx <= len(self.OPTIONS)):
                console.print('[yellow]Out of range.[/yellow]')
                continue

            opt = self.OPTIONS[idx - 1]

            # Check tool availability
            tool = opt.get('tool', '')
            if tool and not tool_status.get(tool, False):
                console.print(
                    f'[red]❌ Tool [bold]{tool}[/bold] is not installed.\n'
                    f'   Install with: [cyan]sudo apt install {tool}[/cyan][/red]'
                )
                input('\n  [Press ENTER]')
                continue

            self._execute(opt)

    # ------------------------------------------------------------------ #
    def _annotate(self, tool_status: dict) -> list:
        result = []
        for i, opt in enumerate(self.OPTIONS, 1):
            tool  = opt.get('tool', '')
            avail = tool_status.get(tool, True) if tool else True
            result.append({**opt, 'available': avail, 'index': i})
        return result

    def _execute(self, opt: dict):
        console.print(f"\n  [bold cyan]{opt['name']}[/bold cyan]")
        if opt.get('description'):
            console.print(f"  [dim]{opt['description']}[/dim]\n")

        # Custom: user types the full command
        if opt.get('custom'):
            cmd = input('  Command: ').strip()
            if not cmd:
                console.print('[yellow]Cancelled.[/yellow]')
                return

        # Interactive: just launch the binary
        elif opt.get('interactive'):
            cmd = opt.get('cmd', opt.get('tool', ''))

        # Template: fill in {params}
        else:
            params = {}
            for key in opt.get('params', []):
                hint = opt.get('hints', {}).get(key, key)
                val  = input(f'  {hint}: ').strip()
                if not val:
                    console.print('[yellow]Cancelled.[/yellow]')
                    return
                params[key] = val
            try:
                cmd = opt['cmd'].format(**params)
            except KeyError as e:
                console.print(f'[red]Missing param: {e}[/red]')
                return

        # Root warning
        if opt.get('requires_root') and os.geteuid() != 0:
            console.print('[yellow]⚠  This command typically needs root/sudo.[/yellow]')
            if input('  Add sudo? [Y/n]: ').strip().lower() not in ('n', 'no'):
                cmd = 'sudo ' + cmd

        save = input('  Save output to file? [y/N]: ').strip().lower() == 'y'
        run_command(cmd, save_output=save)
        input('\n  [Press ENTER to continue]')
