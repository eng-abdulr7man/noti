[app]

title = Notification Logger

package.name = notifapp
package.domain = com.simple

source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,json,ttf,atlas

version = 1.0

requirements = python3,kivy==2.3.1,kivymd

orientation = portrait

fullscreen = 0

android.permissions = INTERNET

android.api = 34
android.minapi = 21

# اترك Buildozer يختار إصدار الـ NDK المناسب
# android.ndk =

# لا تستخدم android.sdk
# android.sdk =

osx.python_version = 3

[buildozer]

log_level = 2
warn_on_root = 1
