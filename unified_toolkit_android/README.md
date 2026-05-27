# 🛡️ Security Toolkit — Android APK

A unified Android security testing toolkit built with **Kivy** and **pure Python**.
Designed for **ethical hacking, CTF competitions, and authorized penetration testing**.

---

## 📱 Features

| Category | Tools |
|----------|-------|
| 🔍 Recon & Info | Port scan, DNS lookup, WHOIS, SSL check, Subdomain enum, Banner grab, Ping sweep |
| 🌐 Web App | HTTP headers, Directory bruteforce, SQL injection test, XSS test, Tech detection, Link crawler |
| 🔑 Passwords | SSH brute force, FTP brute force, Hash identification, Hash generator |
| 🌐 Network | IP geolocation, Traceroute, Network info, TCP connect |

---

## 🏗️ Build APK

### Method 1: GitHub Actions (Recommended — no setup needed)

1. **Push** this folder to GitHub
2. GitHub Actions will **automatically build** the APK
3. Go to `Actions` → `Build Android APK` → Click the latest run
4. Download `security-toolkit-apk` from **Artifacts**
5. Install the APK on your Android device

### Method 2: Build locally (Linux/Mac)

```bash
pip install buildozer cython
cd unified_toolkit_android
buildozer android debug
ls bin/*.apk
```

---

## ⚠️ Legal Notice

This tool is for **authorized testing only**.
Only use against systems you own or have explicit written permission to test.
