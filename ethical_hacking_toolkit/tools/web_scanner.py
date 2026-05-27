#!/usr/bin/env python3
"""
tools/web_scanner.py
=====================
Web Vulnerability Scanner panel.

Supported scanners
-------------------
  nikto  : Web server vulnerability scanner.
  dirb   : Directory / file brute-forcer.
  gobuster: Fast directory/DNS brute-forcer (Go-based).
  whatweb: Web technology fingerprinting.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from utils.command_runner import run_command


class WebScannerFrame(tk.Frame):
    """Web scanner panel supporting multiple tools."""

    SCANNERS = {
        "Nikto  (vuln scan)": {
            "binary": "nikto",
            "build":  lambda url, extra: ["nikto", "-h", url] + extra,
        },
        "Dirb  (dir bruteforce)": {
            "binary": "dirb",
            "build":  lambda url, extra: ["dirb", url] + extra,
        },
        "Gobuster  (fast dir/dns)": {
            "binary": "gobuster",
            "build":  lambda url, extra: [
                "gobuster", "dir",
                "-u", url,
                "-w", "/usr/share/wordlists/dirb/common.txt",
            ] + extra,
        },
        "WhatWeb  (fingerprint)": {
            "binary": "whatweb",
            "build":  lambda url, extra: ["whatweb", "-v", url] + extra,
        },
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
            text="🕸️  Web Scanner",
            bg=self.C["bg_card"],
            fg=self.C["accent_green"],
            font=("Consolas", 16, "bold"),
        ).pack(side=tk.LEFT, padx=20)

        tk.Label(
            hdr,
            text="nikto | dirb | gobuster | whatweb",
            bg=self.C["bg_card"],
            fg=self.C["text_secondary"],
            font=("Consolas", 10),
        ).pack(side=tk.RIGHT, padx=20)

        # ── Input card ──
        card = tk.Frame(self, bg=self.C["bg_card"], padx=20, pady=16)
        card.pack(fill=tk.X, padx=20, pady=10)

        # Row 0 – URL
        tk.Label(
            card, text="Target URL:",
            bg=self.C["bg_card"], fg=self.C["text_secondary"],
            font=("Consolas", 10),
        ).grid(row=0, column=0, sticky="w", pady=4)

        self.url_var = tk.StringVar(value="http://example.com")
        tk.Entry(
            card, textvariable=self.url_var,
            bg=self.C["bg_dark"], fg=self.C["text_primary"],
            insertbackground=self.C["accent"],
            relief=tk.FLAT, font=("Consolas", 11), width=44,
        ).grid(row=0, column=1, sticky="ew", padx=(12, 0), pady=4)

        # Row 1 – Scanner
        tk.Label(
            card, text="Scanner:",
            bg=self.C["bg_card"], fg=self.C["text_secondary"],
            font=("Consolas", 10),
        ).grid(row=1, column=0, sticky="w", pady=4)

        self.scanner_var = tk.StringVar()
        scanner_cb = ttk.Combobox(
            card,
            textvariable=self.scanner_var,
            values=list(self.SCANNERS.keys()),
            state="readonly",
            font=("Consolas", 10),
            width=42,
        )
        scanner_cb.current(0)
        scanner_cb.grid(row=1, column=1, sticky="ew", padx=(12, 0), pady=4)

        # Row 2 – Extra flags
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
            relief=tk.FLAT, font=("Consolas", 11), width=44,
        ).grid(row=2, column=1, sticky="ew", padx=(12, 0), pady=4)

        # Row 3 – SSL toggle
        tk.Label(
            card, text="Options:",
            bg=self.C["bg_card"], fg=self.C["text_secondary"],
            font=("Consolas", 10),
        ).grid(row=3, column=0, sticky="w", pady=4)

        opt_frame = tk.Frame(card, bg=self.C["bg_card"])
        opt_frame.grid(row=3, column=1, sticky="w", padx=(12, 0), pady=4)

        self.ssl_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            opt_frame, text="Force SSL (-ssl)",
            variable=self.ssl_var,
            bg=self.C["bg_card"], fg=self.C["text_primary"],
            selectcolor=self.C["bg_dark"],
            activebackground=self.C["bg_card"],
            font=("Consolas", 10),
        ).pack(side=tk.LEFT)

        self.timeout_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            opt_frame, text="Set timeout 10 s",
            variable=self.timeout_var,
            bg=self.C["bg_card"], fg=self.C["text_primary"],
            selectcolor=self.C["bg_dark"],
            activebackground=self.C["bg_card"],
            font=("Consolas", 10),
        ).pack(side=tk.LEFT, padx=(16, 0))

        card.columnconfigure(1, weight=1)

        # ── Buttons ──
        btn_frame = tk.Frame(self, bg=self.C["bg_dark"])
        btn_frame.pack(fill=tk.X, padx=20, pady=(0, 10))

        self.run_btn = tk.Button(
            btn_frame,
            text="▶  Start Scan",
            bg="#1a5c2a",
            fg="white",
            activebackground="#27843d",
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
            fg=self.C["accent_green"],
            insertbackground=self.C["accent"],
            font=("Consolas", 10),
            relief=tk.FLAT,
            state=tk.DISABLED,
            wrap=tk.WORD,
        )
        self.output.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        self._configure_tags()
        self._append("Web Scanner ready.\nEnter a URL and choose a scanner.\n")

    def _configure_tags(self):
        self.output.tag_configure("error",  foreground=self.C["accent_red"])
        self.output.tag_configure("info",   foreground=self.C["accent"])
        self.output.tag_configure("normal", foreground=self.C["accent_green"])

    # ── Logic ─────────────────────────────────────────────────────────────────
    def _run(self):
        url = self.url_var.get().strip()
        if not url:
            self._append("[ERROR] Please enter a target URL.\n", tag="error")
            return
        if not url.startswith(("http://", "https://")):
            url = "http://" + url
            self.url_var.set(url)

        scanner_key = self.scanner_var.get()
        scanner = self.SCANNERS[scanner_key]

        extra: list = self.extra_var.get().split()
        if self.ssl_var.get():
            extra = ["-ssl"] + extra
        if self.timeout_var.get():
            extra = ["-timeout", "10"] + extra

        cmd = scanner["build"](url, extra)

        self._clear()
        self._append(f"$ {' '.join(cmd)}\n\n", tag="info")
        self.run_btn.configure(state=tk.DISABLED, text="⏳ Scanning...")

        def on_done(rc):
            self.run_btn.configure(state=tk.NORMAL, text="▶  Start Scan")

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
