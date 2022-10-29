# MusicServer

A simple music server and client written in Python using FFmpeg for encoding



## Requirements

- FFmpeg with libfdk_aac in path, or a configured location

- `deflate`, `mutagen` install with `pip install -r requirements.txt`



## Usage

- Set the correct folder for music and FFmpeg in settings.json

- Run with `py main.py`



## Known issues

- Currently supports only MP3s as i didn't add support for anything else

- On worse connections might not work properly (for some reason)

- Doesn't work on Firefox as it does not support Matroska containers

- Works only on one device at a time


