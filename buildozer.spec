[app]

title = AtlasUploader
package.name = atlasuploader
package.domain = org.atlas

source.dir = .
source.include_exts = py,kv,png,jpg,atlas

version = 1.0

requirements = python3,kivy,yt-dlp,google-api-python-client,google-auth-oauthlib

orientation = portrait

fullscreen = 0


# ---------- Android settings ----------

android.api = 31
android.minapi = 21
android.sdk = 31

android.ndk = 25b
android.ndk_api = 21

android.accept_sdk_license = True

android.permissions = INTERNET

android.archs = arm64-v8a,armeabi-v7a


# ---------- Build settings ----------

log_level = 2
warn_on_root = 1


# ---------- Python ----------

p4a.branch = master


# ---------- Packaging ----------

android.release_artifact = apk


# ---------- Other ----------

android.allow_backup = True
android.wakelock = False
