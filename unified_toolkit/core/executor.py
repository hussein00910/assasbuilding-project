"""core/executor.py — Real-time command runner with history."""
import subprocess
import json
import os
from datetime import datetime
from rich.console import Console

console = Console()

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HISTORY_FILE = os.path.join(_BASE, 'data', 'history.json')


def _ensure():
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'w') as f:
            json.dump([], f)


def _save_history(cmd: str, output: str):
    _ensure()
    try:
        with open(HISTORY_FILE, 'r') as f:
            history = json.load(f)
        history.append({
            'time':    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'command': cmd,
            'preview': output[:300].strip(),
        })
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history[-100:], f, indent=2, ensure_ascii=False)
    except Exception:
        pass


def run_command(cmd: str, save_output: bool = False) -> str:
    """
    Execute *cmd* in a shell with real-time stdout streaming.
    Saves the run to history.json automatically.
    Returns the full output string.
    """
    console.print(f"\n[dim]─── [bold cyan]{cmd}[/bold cyan] ───[/dim]\n")
    lines = []
    try:
        proc = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        for line in proc.stdout:        # type: ignore[union-attr]
            print(line, end='', flush=True)
            lines.append(line)
        proc.wait()
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠  Interrupted[/yellow]")
    except FileNotFoundError:
        console.print(f"[red][!] Command not found: {cmd.split()[0]}[/red]")
    except Exception as exc:
        console.print(f"[red][!] {exc}[/red]")

    output = ''.join(lines)
    _save_history(cmd, output)

    if save_output and output:
        fname = f"output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(fname, 'w') as f:
            f.write(f"Command : {cmd}\n")
            f.write(f"Time    : {datetime.now()}\n")
            f.write('=' * 60 + '\n')
            f.write(output)
        console.print(f"\n[green]✓ Saved → {fname}[/green]")

    return output
