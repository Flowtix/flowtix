[app]

title = Atlas YouTube Uploader
package.name = atlasuploader
package.domain = org.atlas

source.dir = .
source.include_exts = py,kv

version = 1.0

requirements = python3,kivy,yt-dlp,google-api-python-client,google-auth-oauthlib,requests

orientation = portrait

fullscreen = 0

# Permissions required
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# Android API versions
android.api = 33
android.minapi = 21

# Android architecture
android.archs = arm64-v8a,armeabi-v7a

# Log level
log_level = 2

# Python for Android branch
p4a.branch = master

# Entry point
entrypoint = main.py

# Include additional files
source.include_patterns = assets/*

# Icon (optional)
# icon.filename = icon.png


[buildozer]

log_level = 2

warn_on_root = 1