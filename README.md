# MusicServer

A simple music server and client written in Python using FFmpeg for encoding

## Requirements

- FFmpeg in path, or a configured location

- `deflate`, `mutagen` install with `pip install -r requirements.txt`

## Usage

- Set the correct folder for music and FFmpeg in settings.json

- Run with `py main.py`

## Notes

- For better AAC quality use a build of ffmpeg with `libfdk_aac` and its presets (`libfdk_...`)
