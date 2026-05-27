#!/usr/bin/env python3
"""
tools/network_scanner.py
========================
Network Scanner panel – wraps nmap with a friendly GUI.

Supported scan types
---------------------
  Quick (-F)         : Top 100 ports, fast.
  Full (-p-)         : All 65 535 ports.
  Service (-sV)      : Version/service detection.
  OS Detection (-O)  : OS fingerprinting (requires root).
  Aggressive (-A)    : OS + version + scripts + traceroute.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from utils.command_runner import run_command


class NetworkScannerFrame(tk.Frame):
    """Full-featured nmap front-end panel."""

    SCAN_TYPES = {
        "Quick Scan  (-F)":        ["-F"],
        "Full Port Scan  (-p-)": ["-p-"],
        "Service Detection  (-sV)": ["-sV"],
        "OS Detection  (-O)": ["-O"],
        "Aggressive  (-A)": ["-A"],
    }

    def __init__(self, parent, colors: dict):
        self.C = colors
        super().__init__(parent, bg=self.C["bg_dark"])
        self._build()

    # ── UI ────────────────────────────────────────────────────────────────────
    def _build(self):
        # ── Header ──
        hdr = tk.Frame(self, bg=self.C["bg_card"], pady=14)
        hdr.pack(fill=tk.X, padx=20, pady=(20, 0))

        tk.Label(
            hdr,
            text="🌐  Network Scanner",
            bg=self.C["bg_card"],
            fg=self.C["accent"],
            font=("Consolas", 16, "bold"),
        ).pack(side=tk.LEFT, padx=20)

        tk.Label(
            hdr,
            text="powered by nmap",
            bg=self.C["bg_card"],
            fg=self.C["text_secondary"],
            font=("Consolas", 10),
        ).pack(side=tk.RIGHT, padx=20)

        # ── Input card ──
        card = tk.Frame(self, bg=self.C["bg_card"], padx=20, pady=16)
        card.pack(fill=tk.X, padx=20, pady=10)

        # Row 1 – Target
        tk.Label(
            card, text="Target (IP / Hostname / CIDR):",
            bg=self.C["bg_card"], fg=self.C["text_secondary"],
            font=("Consolas", 10),
        ).grid(row=0, column=0, sticky="w", pady=4)

        self.target_var = tk.StringVar(value="192.168.1.1")
        tk.Entry(
            card, textvariable=self.target_var,
            bg=self.C["bg_dark"], fg=self.C["text_primary"],
            insertbackground=self.C["accent"],
            relief=tk.FLAT, font=("Consolas", 11), width=40,
        ).grid(row=0, column=1, sticky="ew", padx=(12, 0), pady=4)

        # Row 2 – Scan type
        tk.Label(
            card, text="Scan Type:",
            bg=self.C["bg_card"], fg=self.C["text_secondary"],
            font=("Consolas", 10),
        ).grid(row=1, column=0, sticky="w", pady=4)

        self.scan_type_var = tk.StringVar()
        scan_menu = ttk.Combobox(
            card,
            textvariable=self.scan_type_var,
            values=list(self.SCAN_TYPES.keys()),
            state="readonly",
            font=("Consolas", 10),
            width=38,
        )
        scan_menu.current(0)
        scan_menu.grid(row=1, column=1, sticky="ew", padx=(12, 0), pady=4)

        # Row 3 – Extra flags
        tk.Label(
            card, text="Extra Flags:",
            bg=self.C["bg_card"], fg=self.C["text_secondary"],
            font=("Consolas", 10),
        ).grid(row=2, column=0, sticky="w", pady=4)

        self.extra_var = tk.StringVar(value="")
        tk.Entry(
            card, textvariable=self.extra_var,
            bg=self.C["bg_dark"], fg=self.C["text_primary"],
            insertbackground=self.C["accent"],
            relief=tk.FLAT, font=("Consolas", 11), width=40,
        ).grid(row=2, column=1, sticky="ew", padx=(12, 0), pady=4)

        card.columnconfigure(1, weight=1)

        # ── Buttons ──
        btn_frame = tk.Frame(self, bg=self.C["bg_dark"])
        btn_frame.pack(fill=tk.X, padx=20, pady=(0, 10))

        self.run_btn = tk.Button(
            btn_frame,
            text="▶  Run Scan",
            bg=self.C["btn_active"],
            fg="white",
            activebackground=self.C["btn_hover"],
            relief=tk.FLAT,
            font=("Consolas", 11, "bold"),
            padx=20, pady=8,
            cursor="hand2",
            command=self._run,
        )
        self.run_btn.pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(
            btn_frame,
            text="🗑  Clear",
            bg=self.C["bg_card"],
            fg=self.C["text_secondary"],
            activebackground=self.C["border"],
            relief=tk.FLAT,
            font=("Consolas", 11),
            padx=20, pady=8,
            cursor="hand2",
            command=self._clear,
        ).pack(side=tk.LEFT)

        # ── Output ──
        self.output = scrolledtext.ScrolledText(
            self,
            bg=self.C["output_bg"],
            fg=self.C["output_fg"],
            insertbackground=self.C["accent"],
            font=("Consolas", 10),
            relief=tk.FLAT,
            state=tk.DISABLED,
            wrap=tk.WORD,
        )
        self.output.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        self._configure_tags()
        self._append("Nmap Network Scanner ready.\nEnter a target and click Run Scan.\n")

    def _configure_tags(self):
        self.output.tag_configure("error", foreground=self.C["accent_red"])
        self.output.tag_configure("info",  foreground=self.C["accent"])
        self.output.tag_configure("normal",foreground=self.C["output_fg"])

    # ── Logic ─────────────────────────────────────────────────────────────────
    def _run(self):
        target = self.target_var.get().strip()
        if not target:
            self._append("[ERROR] Please enter a target.\n", tag="error")
            return

        flags = self.SCAN_TYPES[self.scan_type_var.get()]
        extra = self.extra_var.get().split()
        cmd = ["nmap"] + flags + extra + [target]

        self._clear()
        self._append(f"$ {' '.join(cmd)}\n\n", tag="info")
        self.run_btn.configure(state=tk.DISABLED, text="⏳ Scanning...")

        def on_done(rc):
            self.run_btn.configure(state=tk.NORMAL, text="▶  Run Scan")

        run_command(cmd, self.output, on_finish=on_done)

    def _clear(self):
        self.output.configure(state=tk.NORMAL)
        self.output.delete("1.0", tk.END)
        self.output.configure(state=tk.DISABLED)

    def _append(self, text: str, tag: str = "normal"):
        self.output.configure(state=tk.NORMAL)
        self.output.insert(tk.END, text, tag)
        self.output.see(tk.END)
        self.output.configure(state=tk.DISABLED)
