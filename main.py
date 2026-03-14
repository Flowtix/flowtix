import os
import threading
from datetime import datetime
from pathlib import Path
from queue import Queue

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

import yt_dlp

# YouTube API
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

APP_NAME = "Atlas YouTube Uploader"

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly",
]

CLIENT_SECRET_FILE = "client_secret.json"
DOWNLOADS_DIR = Path("downloads")


class VideoTask:
    def __init__(self, url, title, description, tags, schedule):
        self.url = url
        self.title = title
        self.description = description
        self.tags = tags
        self.schedule = schedule


def ensure_download_dir():
    DOWNLOADS_DIR.mkdir(exist_ok=True)


def fetch_video_info(url):
    opts = {"quiet": True, "skip_download": True}

    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)

    return info


def download_video(url):

    ensure_download_dir()

    opts = {
        "outtmpl": str(DOWNLOADS_DIR / "%(title)s.%(ext)s"),
        "format": "bv*+ba/best",
        "merge_output_format": "mp4",
        "quiet": True
    }

    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    return filename


def youtube_authorize():

    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRET_FILE, SCOPES
    )

    creds = flow.run_local_server(port=0)

    return build("youtube", "v3", credentials=creds)


def upload_video(youtube, file_path, title, description, tags):

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "22",
        },
        "status": {
            "privacyStatus": "private",
        }
    }

    media = MediaFileUpload(file_path, resumable=True)

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    response = None

    while response is None:
        status, response = request.next_chunk()

    return response["id"]


class AtlasUI(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.youtube = None
        self.queue = Queue()

        threading.Thread(target=self.worker, daemon=True).start()

    def log(self, msg):
        Clock.schedule_once(lambda dt: self.ids.log.text += msg + "\n")

    def connect_youtube(self):

        self.log("Connecting to YouTube...")

        try:
            self.youtube = youtube_authorize()
            self.log("Connected successfully")

        except Exception as e:
            self.log(f"Auth failed: {e}")

    def fetch_info(self):

        url = self.ids.url.text

        try:
            info = fetch_video_info(url)

            self.ids.title.text = info.get("title", "")
            self.ids.description.text = info.get("description", "")
            self.ids.tags.text = ",".join(info.get("tags", []))

            self.log("Video info fetched")

        except Exception as e:
            self.log(str(e))

    def add_task(self):

        url = self.ids.url.text
        title = self.ids.title.text
        description = self.ids.description.text
        tags = self.ids.tags.text.split(",")

        schedule = self.ids.schedule.text

        task = VideoTask(url, title, description, tags, schedule)

        self.queue.put(task)

        self.log("Video added to queue")

    def worker(self):

        while True:

            task = self.queue.get()

            try:

                self.log("Downloading video...")

                path = download_video(task.url)

                self.log("Uploading video...")

                vid = upload_video(
                    self.youtube,
                    path,
                    task.title,
                    task.description,
                    task.tags
                )

                self.log(f"Upload complete: {vid}")

                os.remove(path)

            except Exception as e:
                self.log(str(e))

            self.queue.task_done()


class AtlasApp(App):

    def build(self):
        return AtlasUI()


AtlasApp().run()