#!/usr/bin/env python3
"""
Ethical Hacking Toolkit - Main Application
==========================================
A GUI-based security testing toolkit built with Tkinter.

WARNING: This tool is for AUTHORIZED security testing only.
Unauthorized use is illegal and unethical.
"""

import tkinter as tk
from tkinter import messagebox, font
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tools.network_scanner import NetworkScannerFrame
from tools.password_brute import PasswordBruteFrame
from tools.web_scanner import WebScannerFrame

# ─── Colour Palette ───────────────────────────────────────────────────────────
COLORS = {
    "bg_dark":      "#0d1117",
    "bg_sidebar":   "#161b22",
    "bg_card":      "#1c2128",
    "accent":       "#58a6ff",
    "accent_red":   "#f85149",
    "accent_green": "#3fb950",
    "accent_orange":"#d29922",
    "text_primary": "#e6edf3",
    "text_secondary":"#8b949e",
    "btn_active":   "#1f6feb",
    "btn_hover":    "#388bfd",
    "border":       "#30363d",
    "output_bg":    "#0d1117",
    "output_fg":    "#3fb950",
}


class EthicalHackingToolkit(tk.Tk):
    """Root application window."""

    def __init__(self):
        super().__init__()
        self.title("⚡ Ethical Hacking Toolkit v1.0")
        self.geometry("1200x750")
        self.minsize(900, 600)
        self.configure(bg=COLORS["bg_dark"])
        self._center_window()

        # Show ethical disclaimer before loading the UI
        self._show_disclaimer()

        self._build_ui()
        self.mainloop()

    # ── Disclaimer ────────────────────────────────────────────────────────────
    def _show_disclaimer(self):
        """Force the user to accept the ethical-use disclaimer."""
        msg = (
            "⚠️  ETHICAL USE DISCLAIMER  ⚠️\n\n"
            "This toolkit is provided for EDUCATIONAL and AUTHORIZED "
            "security testing purposes ONLY.\n\n"
            "• You must have explicit written permission from the system "
            "owner before running any test.\n"
            "• Unauthorized scanning, brute-forcing, or probing of systems "
            "you do not own is ILLEGAL.\n"
            "• The developer assumes NO liability for misuse of this software.\n\n"
            "By clicking 'I Agree', you confirm that you will use this tool "
            "legally and ethically."
        )
        agreed = messagebox.askokcancel(
            title="Ethical Use Agreement",
            message=msg,
            icon=messagebox.WARNING,
        )
        if not agreed:
            self.destroy()
            sys.exit(0)

    # ── Window helpers ────────────────────────────────────────────────────────
    def _center_window(self):
        self.update_idletasks()
        w, h = 1200, 750
        x = (self.winfo_screenwidth()  // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    # ── UI Construction ───────────────────────────────────────────────────────
    def _build_ui(self):
        # ── Top bar ──
        topbar = tk.Frame(self, bg=COLORS["bg_sidebar"], height=50)
        topbar.pack(fill=tk.X, side=tk.TOP)
        topbar.pack_propagate(False)

        tk.Label(
            topbar,
            text="  ⚡ Ethical Hacking Toolkit",
            bg=COLORS["bg_sidebar"],
            fg=COLORS["accent"],
            font=("Consolas", 14, "bold"),
            anchor="w",
        ).pack(side=tk.LEFT, padx=10, pady=10)

        tk.Label(
            topbar,
            text="🔒 Authorized Use Only  ",
            bg=COLORS["bg_sidebar"],
            fg=COLORS["accent_red"],
            font=("Consolas", 10),
            anchor="e",
        ).pack(side=tk.RIGHT, padx=10, pady=10)

        # ── Main body ──
        body = tk.Frame(self, bg=COLORS["bg_dark"])
        body.pack(fill=tk.BOTH, expand=True)

        # Sidebar
        self.sidebar = tk.Frame(body, bg=COLORS["bg_sidebar"], width=220)
        self.sidebar.pack(fill=tk.Y, side=tk.LEFT)
        self.sidebar.pack_propagate(False)

        # Content area
        self.content = tk.Frame(body, bg=COLORS["bg_dark"])
        self.content.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        self._build_sidebar()
        self._build_content()

        # Show first tool by default
        self._switch_tool("network")

    def _build_sidebar(self):
        # Title
        tk.Label(
            self.sidebar,
            text="TOOLS",
            bg=COLORS["bg_sidebar"],
            fg=COLORS["text_secondary"],
            font=("Consolas", 9, "bold"),
            anchor="w",
        ).pack(fill=tk.X, padx=16, pady=(20, 6))

        # Separator
        tk.Frame(self.sidebar, bg=COLORS["border"], height=1).pack(
            fill=tk.X, padx=10, pady=(0, 10)
        )

        self._sidebar_buttons = {}
        tools = [
            ("network",  "🌐  Network Scanner",   COLORS["accent"]),
            ("password", "🔑  Password Brute",     COLORS["accent_orange"]),
            ("web",      "🕸️  Web Scanner",         COLORS["accent_green"]),
        ]
        for key, label, color in tools:
            btn = tk.Button(
                self.sidebar,
                text=label,
                bg=COLORS["bg_card"],
                fg=COLORS["text_primary"],
                activebackground=COLORS["btn_active"],
                activeforeground="white",
                relief=tk.FLAT,
                anchor="w",
                padx=16,
                pady=10,
                font=("Consolas", 11),
                cursor="hand2",
                command=lambda k=key: self._switch_tool(k),
            )
            btn.pack(fill=tk.X, padx=10, pady=3)
            self._sidebar_buttons[key] = (btn, color)

        # Bottom info
        tk.Frame(self.sidebar, bg=COLORS["border"], height=1).pack(
            fill=tk.X, padx=10, pady=(20, 10)
        )
        tk.Label(
            self.sidebar,
            text="Use responsibly \n& legally only.",
            bg=COLORS["bg_sidebar"],
            fg=COLORS["accent_red"],
            font=("Consolas", 8),
            justify="left",
        ).pack(padx=16, pady=6, anchor="w")

    def _build_content(self):
        """Create all tool frames (hidden by default)."""
        self._frames = {
            "network":  NetworkScannerFrame(self.content,  COLORS),
            "password": PasswordBruteFrame(self.content,   COLORS),
            "web":      WebScannerFrame(self.content,       COLORS),
        }
        for frame in self._frames.values():
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    def _switch_tool(self, key: str):
        """Raise the selected frame and update sidebar button styles."""
        # Reset all buttons
        for k, (btn, color) in self._sidebar_buttons.items():
            btn.configure(bg=COLORS["bg_card"], fg=COLORS["text_primary"])
        # Highlight active
        btn, color = self._sidebar_buttons[key]
        btn.configure(bg=COLORS["btn_active"], fg="white")
        # Raise frame
        self._frames[key].tkraise()


if __name__ == "__main__":
    EthicalHackingToolkit()
