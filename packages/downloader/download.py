import os
import json
import yt_dlp
import eyed3
import wget

def progress_hook(data):
  info_dict = data["info_dict"]
  os.makedirs("../../outputs", exist_ok=True)
  with open(f'../../outputs/{info_dict["id"]}.json', 'w') as wo:
    json.dump(data, wo)

def postprocessor_hook(data):
  if data["status"] == "finished":
    info_dict = data["info_dict"]

    thumbnails = info_dict["thumbnails"]
    thumbnail = next(t for t in reversed(thumbnails) if t["url"].endswith(".jpg"))
    filepath = info_dict["filepath"]
    root, ext = os.path.splitext(filepath)
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
  with yt_dlp.YoutubeDL({}) as youtube:
    return youtube.extract_info(url, download=False)

async def download(id: str):
  params = dict(
    format="bestaudio/best",
    paths=dict(home="../../outputs"),
    progress_hooks=[ progress_hook ],
    ffmpeg_location="/usr/bin/ffmpeg",
    postprocessors=[dict(
      key="FFmpegExtractAudio",
      preferredcodec="mp3",
      preferredquality="320",
    )],
    writethumbnail=True,
    postprocessor_hooks=[ postprocessor_hook ],
  )
  with yt_dlp.YoutubeDL(params) as youtube:
    youtube.download_with_info_file(f'../../outputs/info/{id}.json')
