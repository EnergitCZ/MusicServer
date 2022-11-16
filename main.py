"""
A simple music server written in Python
"""

import json
import os.path

settings = json.load(open("settings.json", "r")) # Load settings file
musicf = os.path.realpath(settings["music_folder"])
presets = settings["presets"]

from libs import wrappers

if settings["encoders"]["ffmpeg_location"] == "PATH": # Get wrapper of FFmpeg
	ffmpeg = wrappers.FFmpeg("ffmpeg")
else:
	relpath = os.path.join(settings["encoders"]["ffmpeg_location"], "ffmpeg")
	ffmpeg = wrappers.FFmpeg(os.realpath(relpath))

from libs.datatypes import Database

db = Database(musicf)
if os.path.exists(os.path.join(musicf, "db.musdb")): # Load database if exists else create it
	db.load()
else:
	db.update()

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import unquote
from socketserver import ThreadingMixIn
import threading
import gc
gc.collect()

class Handler(BaseHTTPRequestHandler):
	def do_GET(self):
		success = False
		if self.path.startswith("/getFile/"): # Get song from database
			urlsongpath = self.path.replace("/getFile/", "")
			songpath = unquote(urlsongpath)
			filepath = os.path.join(musicf, songpath)
			if os.path.exists(filepath):
				self.send_response(200)
				self.send_header("Content-Type", "audio/mp3")
				self.end_headers()
				with open(filepath, "rb") as f:
					while True: # Send the song
						chunk = f.read(64)
						if chunk:
							self.wfile.write(chunk)
						else:
							break
				success = True
		elif self.path.startswith("/getEncFile/"): # Get song from database and encode it
			presetsong = self.path.replace("/getEncFile/", "", 1)
			x = presetsong.find("/")
			preset = presetsong[:x]
			options = presets[preset]
			opt = "-c:a " + options["codec"]
			optformat = "-f " + options["format"]
			if options["format"] in ["ipod", "mp4"]:
				optformat = "-frag_duration 3600 " + optformat
			bitrate = options.get("bitrate")
			if bitrate:
				opt += " -b:a {}k".format(bitrate)
			prof = options.get("profile")
			if prof:
				opt += " -profile:a {}".format(prof)
			channels = options.get("channels")
			if channels:
				opt += " -ac {}".format(channels)
			songpath = unquote(presetsong[x+1:])
			filepath = os.path.join(musicf, songpath) # Get the path of the song
			if os.path.exists(filepath):
				p = ffmpeg.run_pipe(filepath, "-hide_banner -loglevel quiet " + opt + " -vn " + optformat) # Convert and put output to pipe
				self.send_response(200)
				self.send_header("Content-Type", options["contenttype"])
				self.send_header("Connection", "keep-alive")
				self.end_headers()
				while True: # Read pipe and send it in chunks of 1024 bytes
					chunk = p.stdout.read(64)
					if chunk:
						self.wfile.write(chunk)
					else:
						break
				success = True
		elif self.path.startswith("/getRandomFiles/"): # Get x of random songs from database
			songcount = int(self.path.replace("/getRandomFiles/", ""))
			self.send_response(200)
			self.send_header("Access-Control-Allow-Origin", "*")
			self.send_header("Content-Type", "text/plain; charset=utf-8")
			self.end_headers()
			lst = db.get_random(songcount)
			for song in lst:
				self.wfile.write((song[0] + "\n").encode("utf-8"))
				self.wfile.write((json.dumps(song[1]) + "\n\n").encode("utf-8"))
			success = True
		elif self.path.startswith("/getPresets"): # Get avaliable presets
			self.send_response(200)
			self.send_header("Access-Control-Allow-Origin", "*")
			self.send_header("Content-Type", "text/plain; charset=utf-8")
			self.end_headers()
			for preset in list(presets.keys()):
				self.wfile.write((preset + "\n").encode("utf-8"))
			success = True
		if not success:
			self.send_response(404)
			self.end_headers()
		self.close_connection = True
		gc.collect()

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	pass

if __name__ == '__main__':
	import subprocess
	subprocess.Popen(["python", "-m", "http.server", "--directory", "website", "80"])
	ws = ThreadedHTTPServer(("0.0.0.0", 2754), Handler)
	ws.serve_forever()