#!/usr/bin/env python3
"""
tools/password_brute.py
========================
Password Brute-Force panel – front-end for THC-Hydra.

Supported protocols: SSH, FTP, HTTP-Form-GET, HTTP-Form-POST, Telnet, SMB.

WARNING: Use only on systems you own or have written authorisation to test.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
from utils.command_runner import run_command


class PasswordBruteFrame(tk.Frame):
    """Hydra-based password brute-force panel."""

    PROTOCOLS = ["ssh", "ftp", "telnet", "smb", "http-get", "http-post-form"]

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
            text="🔑  Password Brute Force",
            bg=self.C["bg_card"],
            fg=self.C["accent_orange"],
            font=("Consolas", 16, "bold"),
        ).pack(side=tk.LEFT, padx=20)

        tk.Label(
            hdr,
            text="powered by hydra",
            bg=self.C["bg_card"],
            fg=self.C["text_secondary"],
            font=("Consolas", 10),
        ).pack(side=tk.RIGHT, padx=20)

        # ── Warning banner ──
        warn = tk.Frame(self, bg="#3d1a1a", pady=6)
        warn.pack(fill=tk.X, padx=20, pady=(6, 0))
        tk.Label(
            warn,
            text=("⚠️  AUTHORIZED USE ONLY — "
                  "Running brute-force attacks without permission is a criminal offence."),
            bg="#3d1a1a",
            fg=self.C["accent_red"],
            font=("Consolas", 9, "bold"),
        ).pack(padx=14)

        # ── Input card ──
        card = tk.Frame(self, bg=self.C["bg_card"], padx=20, pady=16)
        card.pack(fill=tk.X, padx=20, pady=10)

        fields = [
            ("Target IP / Host:",   "target_var",  "192.168.1.100"),
            ("Port:",               "port_var",    "22"),
            ("Username:",           "user_var",    "root"),
        ]
        for row, (lbl, attr, default) in enumerate(fields):
            tk.Label(
                card, text=lbl,
                bg=self.C["bg_card"], fg=self.C["text_secondary"],
                font=("Consolas", 10),
            ).grid(row=row, column=0, sticky="w", pady=4)
            var = tk.StringVar(value=default)
            setattr(self, attr, var)
            tk.Entry(
                card, textvariable=var,
                bg=self.C["bg_dark"], fg=self.C["text_primary"],
                insertbackground=self.C["accent"],
                relief=tk.FLAT, font=("Consolas", 11), width=36,
            ).grid(row=row, column=1, sticky="ew", padx=(12, 0), pady=4)

        # Protocol
        tk.Label(
            card, text="Protocol:",
            bg=self.C["bg_card"], fg=self.C["text_secondary"],
            font=("Consolas", 10),
        ).grid(row=3, column=0, sticky="w", pady=4)
        self.proto_var = tk.StringVar()
        proto_cb = ttk.Combobox(
            card, textvariable=self.proto_var,
            values=self.PROTOCOLS, state="readonly",
            font=("Consolas", 10), width=34,
        )
        proto_cb.current(0)
        proto_cb.grid(row=3, column=1, sticky="ew", padx=(12, 0), pady=4)
        proto_cb.bind("<<ComboboxSelected>>", self._on_proto_change)

        # Wordlist (password list)
        tk.Label(
            card, text="Password Wordlist:",
            bg=self.C["bg_card"], fg=self.C["text_secondary"],
            font=("Consolas", 10),
        ).grid(row=4, column=0, sticky="w", pady=4)

        wl_frame = tk.Frame(card, bg=self.C["bg_card"])
        wl_frame.grid(row=4, column=1, sticky="ew", padx=(12, 0), pady=4)

        self.wordlist_var = tk.StringVar(value="/usr/share/wordlists/rockyou.txt")
        tk.Entry(
            wl_frame, textvariable=self.wordlist_var,
            bg=self.C["bg_dark"], fg=self.C["text_primary"],
            insertbackground=self.C["accent"],
            relief=tk.FLAT, font=("Consolas", 11), width=27,
        ).pack(side=tk.LEFT)
        tk.Button(
            wl_frame, text="Browse",
            bg=self.C["btn_active"], fg="white",
            relief=tk.FLAT, font=("Consolas", 9),
            padx=8, cursor="hand2",
            command=self._browse_wordlist,
        ).pack(side=tk.LEFT, padx=(6, 0))

        # HTTP form path (shown only for http protocols)
        tk.Label(
            card, text="HTTP Path (if HTTP):",
            bg=self.C["bg_card"], fg=self.C["text_secondary"],
            font=("Consolas", 10),
        ).grid(row=5, column=0, sticky="w", pady=4)
        self.http_path_var = tk.StringVar(value="/login.php:user=^USER^&pass=^PASS^:F=incorrect")
        self.http_entry = tk.Entry(
            card, textvariable=self.http_path_var,
            bg=self.C["bg_dark"], fg=self.C["text_secondary"],
            insertbackground=self.C["accent"],
            relief=tk.FLAT, font=("Consolas", 10), width=36,
            state=tk.DISABLED,
        )
        self.http_entry.grid(row=5, column=1, sticky="ew", padx=(12, 0), pady=4)

        card.columnconfigure(1, weight=1)

        # ── Buttons ──
        btn_frame = tk.Frame(self, bg=self.C["bg_dark"])
        btn_frame.pack(fill=tk.X, padx=20, pady=(0, 10))

        self.run_btn = tk.Button(
            btn_frame,
            text="▶  Start Attack",
            bg="#b84a00",
            fg="white",
            activebackground="#e05a00",
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
            fg=self.C["accent_orange"],
            insertbackground=self.C["accent"],
            font=("Consolas", 10),
            relief=tk.FLAT,
            state=tk.DISABLED,
            wrap=tk.WORD,
        )
        self.output.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        self._configure_tags()
        self._append("Hydra Password Brute-Force ready.\nFill in the fields and click Start Attack.\n")

    def _configure_tags(self):
        self.output.tag_configure("error",  foreground=self.C["accent_red"])
        self.output.tag_configure("info",   foreground=self.C["accent"])
        self.output.tag_configure("normal", foreground=self.C["accent_orange"])

    # ── Logic ─────────────────────────────────────────────────────────────────
    def _on_proto_change(self, _event=None):
        proto = self.proto_var.get()
        if "http" in proto:
            self.http_entry.configure(state=tk.NORMAL,
                                      fg=self.C["text_primary"])
        else:
            self.http_entry.configure(state=tk.DISABLED,
                                      fg=self.C["text_secondary"])

    def _browse_wordlist(self):
        path = filedialog.askopenfilename(
            title="Select Wordlist File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if path:
            self.wordlist_var.set(path)

    def _run(self):
        target   = self.target_var.get().strip()
        port     = self.port_var.get().strip()
        username = self.user_var.get().strip()
        wordlist = self.wordlist_var.get().strip()
        proto    = self.proto_var.get()

        if not all([target, port, username, wordlist]):
            self._append("[ERROR] Please fill in all required fields.\n", tag="error")
            return

        cmd = ["hydra",
               "-l", username,
               "-P", wordlist,
               "-s", port,
               "-t", "4",         # 4 parallel tasks (safe default)
               "-V",              # verbose – show each attempt
               target,
               proto]

        # For HTTP form protocols, append the form path
        if "http" in proto:
            http_path = self.http_path_var.get().strip()
            if http_path:
                cmd.append(http_path)

        self._clear()
        self._append(f"$ {' '.join(cmd)}\n\n", tag="info")
        self.run_btn.configure(state=tk.DISABLED, text="⏳ Running...")

        def on_done(rc):
            self.run_btn.configure(state=tk.NORMAL, text="▶  Start Attack")

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
