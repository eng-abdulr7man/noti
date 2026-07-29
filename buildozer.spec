[app]
title = Notification Logger

package.name = notifapp
package.domain = com.simple

source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,atlas,json,ttf

version = 1.0

requirements = python3==3.11,kivy==2.3.1,kivymd

orientation = portrait
fullscreen = 0

android.api = 34
android.minapi = 24

android.permissions = INTERNET

# اترك Buildozer يختار الـ NDK المناسب
# android.ndk =
# android.sdk =

[buildozer]
log_level = 2
warn_on_root = 0
