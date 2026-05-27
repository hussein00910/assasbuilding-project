# 🔴 Unified Security Toolkit

> A powerful CLI interface that unifies **115+ preset commands** across 9 hacking tool categories.
> Just run it, pick a number, fill in the target — it does the rest.

⚠️ **For authorized penetration testing, CTF competitions, and security labs ONLY.**

---

## ⚡ Quick Start

```bash
# 1. Install Python dependency
pip install rich

# 2. Run
python3 main.py
```

> Kali Linux / Parrot OS already have almost all tools pre-installed.

---

## 📺 Main Menu

```
 #   Category                    Options
 ─────────────────────────────────────────────
 [1] 🔍  Information Gathering       18
 [2] 🛡️  Vulnerability Scanning      10
 [3] 💥  Exploitation                 12
 [4] 🔑  Password Attacks             15
 [5] 🌐  Web Application              14
 [6] 🎣  Phishing / Social Eng.        6
 [7] 📡  Wireless Attacks             10
 [8] 🔌  Network Tools                12
 [9] 🔬  Digital Forensics            10
 ─────────────────────────────────────────────
 [T] Show installed tools status
 [H] Command history (last 100)
 [Q] Quit
```

---

## 🔧 How It Works

```
You type: 1  (Information Gathering)
          ↓
You see:  [1] Quick Scan        nmap -F <target>
          [2] Full Port Scan    nmap -p- <target>
          [3] Service Detect    nmap -sV <target>
          ... 18 options total ...
          ↓
You type: 3
          ↓
Prompt:   Target IP / hostname: 192.168.1.1
          ↓
Executes: nmap -sV 192.168.1.1   (real-time output)
          ↓
Ask:      Save output to file? [y/N]
```

---

## 📌 Tool Shortcut

Type the tool name directly from main menu:
```
→ nmap        → jumps to Information Gathering
→ hydra       → jumps to Password Attacks
→ sqlmap      → jumps to Exploitation
```

---

## 📂 Project Structure

```
unified_toolkit/
├── main.py                   ← Entry point + main loop
├── requirements.txt
├── core/
│   ├── executor.py            ← run_command() with real-time streaming
│   ├── checker.py             ← detect installed tools via shutil.which()
│   └── ui.py                  ← all Rich display functions
├── modules/
│   ├── base.py                ← BaseModule class (inherited by all)
│   ├── recon.py               ← 18 options: nmap, whois, DNS, OSINT
│   ├── scanning.py            ← 10 options: NSE scripts, nikto, wapiti
│   ├── exploitation.py        ← 12 options: metasploit, sqlmap, payloads
│   ├── passwords.py           ← 15 options: hydra, john, hashcat
│   ├── web.py                 ← 14 options: gobuster, wfuzz, sqlmap
│   ├── phishing.py            ←  6 options: zphisher, SET
│   ├── wireless.py            ← 10 options: aircrack-ng, wifite, reaver
│   ├── network.py             ← 12 options: netcat, tcpdump, ettercap
│   └── forensics.py           ← 10 options: binwalk, steghide, volatility
└── data/
    └── history.json           ← auto-created, last 100 commands
```

---

## ➕ Adding a New Tool

1. Open any module file (e.g. `modules/web.py`)
2. Add a dict to the `OPTIONS` list:
```python
{'name':    'My New Tool',
 'tool':    'mytool',
 'cmd':     'mytool -flag {target}',
 'params':  ['target'],
 'hints':   {'target': 'Target IP or URL'},
 'description': 'What this does'},
```
3. Add the tool name to `TOOLS` list
4. Done — it appears in the menu automatically

---

## 📺 Screenshot Flow

```
╔════════════════════════════════════════════════════════════╗
║  🔴 UNIFIED SECURITY TOOLKIT   ✓ 32/45 tools installed  ║
╠════════════════════════════════════════════════════════════╣
║ [1] 🔍 Information Gathering     18 options              ║
║ [2] 🛡️ Vulnerability Scanning    10 options              ║
║ [3] 💥 Exploitation               12 options              ║
║ [4] 🔑 Password Attacks           15 options              ║
║ [5] 🌐 Web Application            14 options              ║
║ [6] 🎣 Phishing                    6 options              ║
║ [7] 📡 Wireless                   10 options              ║
║ [8] 🔌 Network Tools              12 options              ║
║ [9] 🔬 Digital Forensics          10 options              ║
╠════════════════════════════════════════════════════════════╣
║ [T] Tools Status  [H] History  [Q] Quit                   ║
╚════════════════════════════════════════════════════════════╝
  → _
```
