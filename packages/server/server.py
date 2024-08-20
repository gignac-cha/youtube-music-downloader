import flask

import os
import sys
import pathlib

import lxml.etree
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import json
import asyncio
import concurrent.futures
import urllib.parse

import downloader.download

import requests
import lxml

server = flask.Flask(__name__, static_url_path='')

executor = concurrent.futures.ThreadPoolExecutor(max_workers=8)

@server.get("/")
@server.get("/index.html")
def index():
  return server.send_static_file('index.html')

@server.get("/static/<path:path>")
def get_static(path):
  return server.send_static_file(path)

@server.post("/api/v1/search")
async def post_search():
  search_query = flask.request.json.get("search_query", None)
  if search_query is None:
    return flask.jsonify(error=True, message="inavlid search_query"), 400
  scheme = "https"
  netloc = "www.youtube.com"
  path = "/results"
  params = None
  queries = {
    "search_query": f'{search_query} "Topic"',
  }
  query = urllib.parse.urlencode(queries)
  fragment = None
  url = urllib.parse.urlunparse((scheme, netloc, path, params, query, fragment))
  response = requests.get(url)
  root = lxml.etree.HTML(response.text)
  token = "var ytInitialData = "
  for script in root.xpath(f'//script[starts-with(text(), "{token}")]'):
    data = json.loads(script.text[len(token):-1])
    contents1 = data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"]
    data = []
    for content1 in contents1:
      if "itemSectionRenderer" in content1:
        contents2 = content1["itemSectionRenderer"]["contents"]
        for content2 in contents2:
          if "videoRenderer" in content2:
            videoRenderer = content2["videoRenderer"]
            id = videoRenderer["videoId"]
            title = next(iter(videoRenderer["title"]["runs"]))["text"]
            artist = next(iter(videoRenderer["ownerText"]["runs"]))["text"]
            thumbnail = max(videoRenderer["thumbnail"]["thumbnails"], key=lambda thumbnail: thumbnail["width"] ** 2 + thumbnail["height"])["url"]
            data.append(dict(id=id, title=title, artist=artist, thumbnail=thumbnail))
    return flask.jsonify(error=False, data=data)
  return flask.jsonify(error=True, message="unexpected error"), 500

@server.post("/api/v1/download")
async def post_download():
  url = flask.request.json.get("url", None)
  if url is None:
    return flask.jsonify(error=True, message="invalid url"), 400
  info = downloader.download.info(url)
  output_path = pathlib.Path("../../outputs").resolve()
  info_path = output_path / "info"
  os.makedirs(info_path, exist_ok=True)
  with open(info_path / f'{info["id"]}.json', 'w') as wo:
    json.dump(info, wo)
  with open(output_path / f'{info["id"]}.json', 'w') as wo:
    json.dump({}, wo)
  executor.submit(lambda id: asyncio.run(downloader.download.download(id)), info["id"])
  return flask.jsonify(error=False, data=info), 202

def get_file(id, as_attachment: bool):
  output_path = pathlib.Path("../../outputs").resolve()
  path = output_path / f'{id}.json'
  if not os.path.exists(path):
    return flask.jsonify(error=True, message="invalid id"), 404
  with open(path, 'r') as ro:
    data = json.load(ro)
    file_path = pathlib.Path(data["filename"]).resolve()
    root, ext = os.path.splitext(file_path)
    return flask.send_file(f'{root}.mp3', as_attachment=as_attachment)

@server.get("/download/<id>")
def get_download_id(id):
  return get_file(id, True)

@server.get("/play/<id>")
def get_play_id(id):
  return get_file(id, False)

@server.get("/api/v1/info/<id>")
def get_info_id(id):
  output_path = pathlib.Path("../../outputs").resolve()
  path = output_path / f'{id}.json'
  if not os.path.exists(path):
    return flask.jsonify(error=True, message="invalid id"), 404
  with open(path, 'r') as ro:
    data = json.load(ro)
    data = dict(
      info_dict=dict(id=data.get("info_dict", {}).get("id")),
      status=data.get("status", "downloading"),
      speed=data.get("speed", 0),
      downloaded_bytes=data.get("downloaded_bytes", 0),
      total_bytes=data.get("total_bytes", 1),
      elapsed=data.get("elapsed", 0),
    )
    return flask.jsonify(error=False, data=data), 200

@server.get("/api/v1/downloaded")
def get_downloaded():
  output_path = pathlib.Path("../../outputs").resolve()
  os.makedirs(output_path, exist_ok=True)
  data = []
  for path in os.listdir(output_path):
    if path.endswith(".json"):
      with open(output_path / f'{path}', 'r') as ro:
        item = json.load(ro)
        item = dict(
          info_dict=dict(
            id=item.get("info_dict", {}).get("id"),
            title=item.get("info_dict", {}).get("title"),
          ),
          total_bytes=item.get("total_bytes", 0),
        )
        data.append(item)
  return flask.jsonify(error=False, data=data)

if __name__ == "__main__":
  server.run(host="0.0.0.0", port=5000)
