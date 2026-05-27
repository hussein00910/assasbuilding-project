# 🔴 RedAmon Android

> **AI-Powered Penetration Testing Platform for Android**  
> Inspired by [RedAmon](https://github.com/samugit83/redamon) — rebuilt for mobile with pure Python + Claude AI.

⚠️ **For authorized security testing, CTF labs, and educational use ONLY.**

---

## 🤖 Features vs Original RedAmon

| Feature | RedAmon (Desktop) | RedAmon Android |
|---------|-------------------|------------------|
| UI | Next.js browser | Kivy native APK |
| Recon Tools | 40+ Linux CLI tools | 9 Pure Python tools |
| AI Agent | LangGraph + ReAct | Claude API (multi-step) |
| Database | Neo4j + PostgreSQL | SQLite (local) |
| Report | HTML export | In-app + chat |
| Install | Docker + 8GB RAM | APK — install & run |

---

## 🔧 9 Built-in Recon Tools

| Tool | What it does |
|------|--------------|
| 📡 Port Scanner | TCP scan ports 1–1024 with banner grab |
| 🌐 Subdomain Enum | DNS-based subdomain discovery |
| 📌 DNS Lookup | A, AAAA, PTR, MX records |
| 🔒 SSL/TLS Check | Certificate analysis + weak protocol detection |
| 📊 Header Analysis | Security header audit (CSP, HSTS, X-Frame…) |
| 🔎 Tech Detection | CMS, framework, server fingerprinting |
| 📂 Dir Brute-Force | Common path enumeration (requests-based) |
| 📗 WHOIS Lookup | Domain registration info |
| 🕷️ Web Crawler | Link, form, and parameter discovery |

---

## 🤖 AI Agent Flow

```
Target entered
      ↓
[9 tools run in parallel]
      ↓
Raw output → Claude API
      ↓
Step 1: Analyze → extract CRITICAL/HIGH/MEDIUM/LOW findings
      ↓
Step 2: Generate full pentest report
      ↓
Interactive chat — ask follow-up questions
```

---

## 🚀 Build APK via GitHub Actions

1. Push to `main` branch
2. GitHub Actions auto-builds (~15 min)
3. Download from **Actions → RedAmon-Android-APK**
4. Install on Android (enable unknown sources)

---

## ⚡ Run Locally (Linux / macOS / Termux with X11)

```bash
git clone https://github.com/hussein00910/assasbuilding-project
cd assasbuilding-project/redamon_android
pip install kivy requests
python3 main.py
```

---

## ⚙️ Setup: Claude API Key

1. Get API key: [console.anthropic.com](https://console.anthropic.com)
2. Open app → **⚙️ Settings**
3. Paste your `sk-ant-api03-…` key
4. Choose model: **Haiku** (fast/cheap) or **Sonnet** (smarter)

---

## 📂 Project Structure

```
redamon_android/
├── main.py                    # App entry, TopBar, NavBar, Disclaimer
├── config.py                  # Colors, helpers
├── buildozer.spec             # APK build config
├── .github/workflows/
│   └── build.yml               # Auto-build APK on push
├── database/
│   └── db.py                   # SQLite: scans, findings, chat, settings
├── screens/
│   ├── dashboard.py            # Scan list + stats
│   ├── scan_screen.py          # New scan + live output + auto-AI
│   ├── ai_screen.py            # Report viewer + AI chat
│   └── settings_screen.py      # API key + model config
├── tools/
│   └── recon_engine.py         # 9 pure-Python recon generators
├── ai/
│   └── agent.py                # Claude API: analyze + report + chat
└── utils/
    └── worker.py               # Thread-safe parallel task runner
```
