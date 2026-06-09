[app]

# App metadata
title = Security Toolkit
package.name = securitytoolkit
package.domain = org.securitytoolkit

# Source
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
source.include_patterns = assets/*,tools/*,screens/*,utils/*

# Version
version = 1.0

# Entry point
entrypoint = main.py

# Requirements (pure Python — no native extensions that would fail)
requirements = python3==3.11,kivy==2.3.0,requests,pillow

# Android
android.api = 34
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

# Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Orientation
orientation = portrait

# Fullscreen (0 = show status bar)
fullscreen = 0

# Icon (optional — create a 512x512 PNG)
# icon.filename = %(source.dir)s/assets/icon.png

# Log level (debug/info/warning/error/critical)
log_level = 2

# Kivy-related
android.logcat_filters = *:S python:D

# p4a branch
p4a.branch = master


[buildozer]

# Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# Warn on root
warn_on_root = 1
