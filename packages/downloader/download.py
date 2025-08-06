import os
import json
import pathlib
import yt_dlp
import eyed3
import wget

PROJECT_ROOT = pathlib.Path(__file__).parent.parent.parent.resolve()
OUTPUTS_DIR = PROJECT_ROOT / "outputs"

YDL_OPTS = {
    "format": "bestaudio/best",
    "paths": {"home": str(OUTPUTS_DIR)},
    "ffmpeg_location": "/usr/bin/ffmpeg",  # Will be overridden by server.py
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "320",
    }],
    "writethumbnail": True,
    # Anti-bot and rate limit bypass settings
    "nocheckcertificate": True,
    "http_headers": {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
    },
    # Network settings
    "socket_timeout": 30,
    "retries": 10,
    "file_access_retries": 10,
    "fragment_retries": 10,
    "skip_unavailable_fragments": True,
    "hls_prefer_native": True,
    "buffersize": 1024,
    # YouTube specific
    "youtube_include_dash_manifest": True,
    "prefer_insecure": True,
    "keepvideo": False,
    "extract_flat": False,
    "extractor_args": {
        "youtube": {
            "player_client": ["web"],
        }
    },
}

def progress_hook(data):
    info_dict = data["info_dict"]
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    with open(OUTPUTS_DIR / f'{info_dict["id"]}.json', 'w') as wo:
        json.dump(data, wo)

def postprocessor_hook(data):
    if data["status"] == "finished":
        info_dict = data["info_dict"]

        thumbnails = info_dict["thumbnails"]
        thumbnail = next(t for t in reversed(thumbnails) if t["url"].endswith(".jpg"))
        filepath = info_dict["filepath"]
        root, _ = os.path.splitext(filepath)
        thumbnail_path = f'{root}.jpg'
        if not os.path.exists(thumbnail_path):
            wget.download(thumbnail["url"], out=thumbnail_path)

        audio = eyed3.load(filepath)
        if audio is None:
            return
        audio.tag.title = info_dict["title"]
        audio.tag.artist = info_dict["artist"]
        audio.tag.album = info_dict["album"]
        with open(thumbnail_path, 'rb') as rbo:
            audio.tag.images.set(3, rbo.read(), "image/jpeg", "cover")

        audio.tag.save()

def info(url: str):
    opts = YDL_OPTS.copy()
    opts["progress_hooks"] = [progress_hook]
    opts["postprocessor_hooks"] = [postprocessor_hook]
    
    with yt_dlp.YoutubeDL(opts) as youtube:
        return youtube.extract_info(url, download=False)

async def download(id: str):
    opts = YDL_OPTS.copy()
    opts["progress_hooks"] = [progress_hook]
    opts["postprocessor_hooks"] = [postprocessor_hook]
    
    with yt_dlp.YoutubeDL(opts) as youtube:
        youtube.download_with_info_file(str(OUTPUTS_DIR / "info" / f'{id}.json'))