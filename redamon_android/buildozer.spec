[app]
title = RedAmon Android
package.name = redamonandroid
package.domain = org.redamon
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt,db
version = 1.0
requirements = python3,kivy==2.3.0,requests,certifi,charset-normalizer,idna,urllib3
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 24
android.ndk = 25b
android.arch = arm64-v8a
android.allow_backup = True
android.logcat_filters = *:S python:D
android.release_artifact = apk

[buildozer]
log_level = 2
warn_on_root = 1
