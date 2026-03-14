[app]

# App info
title = AtlasUploader
package.name = atlasuploader
package.domain = org.atlas

source.dir = .
source.include_exts = py,kv,png,jpg,atlas

version = 1.0

# Python requirements
requirements = python3,kivy,yt-dlp,google-api-python-client,google-auth-oauthlib

# Orientation
orientation = portrait

fullscreen = 0


# ---------- Android configuration ----------

android.api = 31
android.minapi = 21
android.sdk = 30

android.ndk = 25b
android.ndk_api = 21

android.accept_sdk_license = True

android.permissions = INTERNET

android.archs = arm64-v8a,armeabi-v7a

android.allow_backup = True
android.wakelock = False


# ---------- Python for Android ----------

p4a.branch = develop


# ---------- Build settings ----------

log_level = 2
warn_on_root = 1


# ---------- Packaging ----------

android.release_artifact = apk
