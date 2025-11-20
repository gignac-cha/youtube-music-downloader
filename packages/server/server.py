import asyncio
import concurrent.futures
import json
import os
import pathlib
import sys
import urllib.parse

import flask
import lxml
import lxml.etree
import requests
import typer

PROJECT_ROOT = pathlib.Path(__file__).parent.parent.parent.resolve()
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
sys.path.append(str(PROJECT_ROOT / "packages"))

from downloader import YDL_OPTS, download, info

app = typer.Typer()
server = flask.Flask(__name__, static_url_path="")
executor = concurrent.futures.ThreadPoolExecutor(max_workers=8)


@server.get("/")
@server.get("/index.html")
def index():
    return server.send_static_file("index.html")


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
        data = json.loads(script.text[len(token) : -1])
        contents1 = data["contents"]["twoColumnSearchResultsRenderer"][
            "primaryContents"
        ]["sectionListRenderer"]["contents"]
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
                        thumbnail = max(
                            videoRenderer["thumbnail"]["thumbnails"],
                            key=lambda thumbnail: thumbnail["width"] ** 2
                            + thumbnail["height"],
                        )["url"]

                        # Extract view count
                        view_count = None
                        if "viewCountText" in videoRenderer:
                            view_count_text = videoRenderer["viewCountText"].get(
                                "simpleText", ""
                            )
                            view_count = view_count_text

                        # Extract duration
                        duration = None
                        if "lengthText" in videoRenderer:
                            duration = videoRenderer["lengthText"].get("simpleText", "")

                        data.append(
                            dict(
                                id=id,
                                title=title,
                                artist=artist,
                                thumbnail=thumbnail,
                                view_count=view_count,
                                duration=duration,
                            )
                        )
        return flask.jsonify(error=False, data=data)
    return flask.jsonify(error=True, message="unexpected error"), 500


def is_already_downloaded(video_id):
    """Check if a video is already downloaded by looking for MP3 files with the video ID"""
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    for filename in os.listdir(OUTPUTS_DIR):
        if filename.endswith(".mp3") and f"[{video_id}]" in filename:
            return True, filename
    return False, None


@server.post("/api/v1/download")
async def post_download():
    url = flask.request.json.get("url", None)
    if url is None:
        return flask.jsonify(error=True, message="invalid url"), 400

    try:
        info_data = info(url)
        video_id = info_data["id"]

        # Check if already downloaded
        already_downloaded, existing_file = is_already_downloaded(video_id)
        if already_downloaded:
            # Create progress file showing completion
            os.makedirs(OUTPUTS_DIR / "info", exist_ok=True)
            with open(OUTPUTS_DIR / "info" / f"{video_id}.json", "w") as wo:
                json.dump(info_data, wo)

            # Create completion status immediately
            file_size = os.path.getsize(OUTPUTS_DIR / existing_file)
            completion_data = {
                "info_dict": {"id": video_id},
                "status": "finished",
                "speed": 0,
                "downloaded_bytes": file_size,
                "total_bytes": file_size,
                "elapsed": 0,
            }
            with open(OUTPUTS_DIR / f"{video_id}.json", "w") as wo:
                json.dump(completion_data, wo)

            return flask.jsonify(error=False, data=info_data), 202

        # Not downloaded yet, proceed with normal download
        os.makedirs(OUTPUTS_DIR / "info", exist_ok=True)

        with open(OUTPUTS_DIR / "info" / f"{info_data['id']}.json", "w") as wo:
            json.dump(info_data, wo)
        with open(OUTPUTS_DIR / f"{info_data['id']}.json", "w") as wo:
            json.dump({}, wo)

        executor.submit(
            lambda id: asyncio.run(download(id)), info_data["id"]
        )
        return flask.jsonify(error=False, data=info_data), 202

    except Exception as e:
        error_msg = str(e)

        if "bot" in error_msg.lower() or "sign in" in error_msg.lower():
            return flask.jsonify(
                error=True, message="YouTube bot detection triggered", details=error_msg
            ), 403

        elif "403" in error_msg or "forbidden" in error_msg.lower():
            return flask.jsonify(
                error=True, message="Access denied by YouTube", details=error_msg
            ), 403

        else:
            return flask.jsonify(
                error=True, message="Unexpected error occurred", details=error_msg
            ), 500


def get_file(id, as_attachment: bool):
    path = OUTPUTS_DIR / f"{id}.json"
    if not os.path.exists(path):
        return flask.jsonify(error=True, message="invalid id"), 404

    # Try to find the MP3 file in outputs directory
    for filename in os.listdir(OUTPUTS_DIR):
        if filename.endswith(".mp3") and f"[{id}]" in filename:
            return flask.send_file(OUTPUTS_DIR / filename, as_attachment=as_attachment)

    return flask.jsonify(error=True, message="file not found"), 404


@server.get("/download/<id>")
def get_download_id(id):
    return get_file(id, True)


@server.get("/play/<id>")
def get_play_id(id):
    return get_file(id, False)


@server.get("/api/v1/info/<id>")
def get_info_id(id):
    path = OUTPUTS_DIR / f"{id}.json"
    if not os.path.exists(path):
        return flask.jsonify(error=True, message="invalid id"), 404

    try:
        with open(path) as ro:
            data = json.load(ro)
            response_data = dict(
                info_dict=dict(id=data.get("info_dict", {}).get("id")),
                status=data.get("status", "downloading"),
                speed=data.get("speed", 0),
                downloaded_bytes=data.get("downloaded_bytes", 0),
                total_bytes=data.get("total_bytes", 1),
                elapsed=data.get("elapsed", 0),
            )
            return flask.jsonify(error=False, data=response_data), 200
    except json.JSONDecodeError:
        # Return default downloading state for corrupted progress files
        response_data = dict(
            info_dict=dict(id=id),
            status="downloading",
            speed=0,
            downloaded_bytes=0,
            total_bytes=1,
            elapsed=0,
        )
        return flask.jsonify(error=False, data=response_data), 200
    except Exception:
        return flask.jsonify(error=True, message="failed to read progress"), 500


@server.get("/api/v1/downloaded")
def get_downloaded():
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    data = []

    # MP3 파일을 기준으로 목록 생성
    for path in os.listdir(OUTPUTS_DIR):
        if path.endswith(".mp3"):
            # [id].mp3 형식에서 ID 추출
            video_id = path.split("[")[-1].split("]")[0]
            title = path.split("[")[0].strip()
            data.append(
                dict(
                    info_dict=dict(
                        id=video_id,
                        title=title,
                    ),
                    total_bytes=os.path.getsize(OUTPUTS_DIR / path),
                    status="completed",
                )
            )
    return flask.jsonify(error=False, data=data)


@app.command()
def serve(
    host: str = typer.Option("0.0.0.0", help="Host to bind to"),
    port: int = typer.Option(5000, help="Port to listen on"),
    ffmpeg_path: str = typer.Option("/usr/bin/ffmpeg", help="Path to ffmpeg binary"),
):
    """Run the Flask server"""
    YDL_OPTS["ffmpeg_location"] = ffmpeg_path
    debug_mode = os.environ.get("FLASK_DEBUG") == "True"
    server.run(host=host, port=port, debug=debug_mode)


if __name__ == "__main__":
    app()
