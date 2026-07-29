[app]
title = Notification Logger
package.name = notifapp
package.domain = com.simple
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0
requirements = python3,kivy,kivymd
orientation = portrait
osx.python_version = 3
fullscreen = 0
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.api = 31
android.minapi = 21
android.ndk = 25.2.9519653
android.sdk = 31

[buildozer]
log_level = 2
warn_on_root = 1