# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture

YouTube Music Downloader is a web application for downloading and converting YouTube videos to MP3 files with metadata. Key components:

- `packages/server/server.py`: Flask server with REST API endpoints
  - Search YouTube videos
  - Download and convert to MP3
  - Track download progress
  - Stream/download converted files

- `packages/downloader/download.py`: Core functionality
  - YouTube video download using yt-dlp
  - Audio extraction with FFmpeg
  - Metadata embedding with eyed3

## Commands

### Setup
```bash
# Install uv (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv venv
uv pip install -r requirements.txt
```

### Development
```bash
# Run server
python packages/server/server.py

# Development server runs on:
http://localhost:5000
```

## Important Notes

- FFmpeg must be installed and available at `/usr/bin/ffmpeg`
- Downloads are processed asynchronously using ThreadPoolExecutor
- File operations use relative paths from the server.py location
- REST API endpoints:
  - POST /api/v1/search: Search YouTube videos
  - POST /api/v1/download: Download and convert video
  - GET /api/v1/info/{id}: Get download progress
  - GET /download/{id}: Download MP3 file
  - GET /play/{id}: Stream MP3 file