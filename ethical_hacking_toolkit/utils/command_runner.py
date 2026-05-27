#!/usr/bin/env python3
"""
utils/command_runner.py
========================
Provides `run_command()` – runs an OS command in a background thread and
streams stdout/stderr line-by-line into a tkinter ScrolledText widget via
a thread-safe queue.
"""

import subprocess
import threading
import shutil
import queue
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from typing import List, Optional, Callable


def _tool_available(name: str) -> bool:
    """Return True if `name` is on the system PATH."""
    return shutil.which(name) is not None


def run_command(
    cmd: List[str],
    output_widget: ScrolledText,
    on_finish: Optional[Callable[[int], None]] = None,
    env: Optional[dict] = None,
) -> None:
    """
    Execute *cmd* in a daemon thread.  Output is streamed to *output_widget*
    (a ScrolledText) safely across threads via a Queue.

    Parameters
    ----------
    cmd           : Command list, e.g. ['nmap', '-F', '192.168.1.1']
    output_widget : The ScrolledText where output will appear.
    on_finish     : Optional callback called with the return-code when done.
    env           : Optional environment variables dict.
    """
    # Basic check: is the executable available?
    executable = cmd[0]
    if not _tool_available(executable):
        _write(output_widget, (
            f"[ERROR] '{executable}' was not found on this system.\n\n"
            f"  Install it and make sure it is in your PATH:\n"
            f"    Linux : sudo apt install {executable}\n"
            f"    macOS : brew install {executable}\n\n"
            "Aborting.\n"
        ), tag="error")
        return

    q: "queue.Queue[Optional[str]]" = queue.Queue()

    def _worker():
        try:
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                env=env,
            )
            for line in proc.stdout:          # type: ignore[union-attr]
                q.put(line)
            proc.wait()
            q.put(None)                        # sentinel
            if on_finish:
                on_finish(proc.returncode)
        except Exception as exc:
            q.put(f"[EXCEPTION] {exc}\n")
            q.put(None)

    def _poll():
        try:
            while True:
                line = q.get_nowait()
                if line is None:
                    _write(output_widget, "\n── Finished ──\n", tag="info")
                    return
                _write(output_widget, line)
        except queue.Empty:
            pass
        output_widget.after(50, _poll)         # check again in 50 ms

    thread = threading.Thread(target=_worker, daemon=True)
    thread.start()
    output_widget.after(50, _poll)


def _write(widget: ScrolledText, text: str, tag: str = "normal") -> None:
    """Append *text* to *widget* in a thread-safe manner."""
    widget.configure(state=tk.NORMAL)
    widget.insert(tk.END, text, tag)
    widget.see(tk.END)
    widget.configure(state=tk.DISABLED)
