# ⚡ Ethical Hacking Toolkit

A Python/Tkinter GUI that bundles the most common security-testing CLI tools
into one clean, dark-themed interface.

> **⚠️ Legal Notice** — This software is for **authorized security testing,
> CTF competitions, and educational use ONLY**. Running these tools against
> systems you do not own or have explicit written permission to test is
> **illegal** in most jurisdictions. The author accepts no liability for
> misuse.

---

## 📸 Features

| Panel | Underlying Tool | What it does |
|---|---|---|
| 🌐 Network Scanner | `nmap` | Port scanning, service detection, OS fingerprinting |
| 🔑 Password Brute Force | `hydra` | SSH / FTP / HTTP login brute-forcing |
| 🕸️ Web Scanner | `nikto` / `dirb` / `gobuster` / `whatweb` | Web vuln scanning, dir enumeration, fingerprinting |

**Common UI features:**
- Dark cybersecurity theme (GitHub-inspired palette)
- Sidebar navigation – switch tools in one click
- All commands run in **background threads** (GUI never freezes)
- Real-time streaming output in a scrollable text area
- Clear error messages when a required tool is not installed
- Ethical-use disclaimer dialog on every launch

---

## 🛠️ Installation

### 1. Python ≥ 3.8 with Tkinter

Tkinter is bundled with standard Python on Windows and macOS.  
On Linux you may need:

```bash
# Debian / Ubuntu
sudo apt install python3-tk

# Arch
sudo pacman -S tk
```

### 2. CLI security tools

```bash
# Debian / Ubuntu / Kali
sudo apt update
sudo apt install -y nmap hydra nikto dirb gobuster whatweb

# Arch Linux
sudo pacman -S nmap hydra nikto dirb gobuster whatweb

# macOS (Homebrew)
brew install nmap hydra nikto dirb gobuster whatweb
```

> Only tools you plan to use need to be installed.  
> The app shows a clear error if a tool is missing.

### 3. Clone the repo

```bash
git clone https://github.com/hussein00910/assasbuilding-project.git
cd assasbuilding-project/ethical_hacking_toolkit
```

---

## 🚀 Running the App

```bash
python3 main.py
# or on Windows:
python main.py
```

The ethical-use disclaimer opens first; you must agree to proceed.

---

## 📂 Project Structure

```
ethical_hacking_toolkit/
├── main.py                  # Root Tk window, sidebar, frame switcher
├── requirements.txt         # Dependency notes
├── README.md
├── tools/
│   ├── __init__.py
│   ├── network_scanner.py   # nmap GUI panel
│   ├── password_brute.py    # hydra GUI panel
│   └── web_scanner.py       # nikto/dirb/gobuster/whatweb panel
└── utils/
    ├── __init__.py
    └── command_runner.py    # Thread + Queue output streamer
```

---

## 🔧 Architecture

```
┌─────────────────────────────────────────────┐
│                  main.py                    │
│  ┌────────────┐  ┌────────────────────────┐ │
│  │  Sidebar   │  │    Content Frame       │ │
│  │            │  │  ┌──────────────────┐  │ │
│  │ [Network]  │──│─▶│ NetworkScanner   │  │ │
│  │ [Password] │  │  ├──────────────────┤  │ │
│  │ [Web]      │  │  │ PasswordBrute    │  │ │
│  │            │  │  ├──────────────────┤  │ │
│  └────────────┘  │  │ WebScanner       │  │ │
│                  │  └──────────────────┘  │ │
│                  └────────────────────────┘ │
└─────────────────────────────────────────────┘
         │                    │
         ▼                    ▼
  utils/command_runner.py  (each tool panel)
  subprocess + threading   builds CLI command
  + queue                  passes to run_command()
```

### `run_command()` flow

```
call run_command(cmd, output_widget)
  │
  ├─ check: shutil.which(cmd[0])  ── not found ──▶ show error, return
  │
  ├─ spawn daemon Thread
  │     subprocess.Popen(cmd, stdout=PIPE)
  │     for line in stdout: queue.put(line)
  │     queue.put(None)  ← sentinel
  │
  └─ schedule _poll() via widget.after(50ms)
        drain queue → widget.insert()
        reschedule until sentinel received
```

---

## 🤝 Contributing

Pull requests are welcome.  When adding a new tool panel:

1. Create `tools/your_tool.py` with a class that inherits `tk.Frame`.
2. Import and add it in `main.py` (`_build_content` and `_switch_tool`).
3. Use `run_command()` from `utils.command_runner` for all subprocesses.

---

## 📜 License

MIT — see `LICENSE`.
