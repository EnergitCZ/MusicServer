# Database

# LU - Last Update (UTC)
# SC - Song Count


"""	Database Example
  # Gzip Compressed
LU 0
SC 2

{ # Pickled Data
"/data/music/album1/song1": {"title": "Example Song", "artist": "Example Artist", "album": "Example Album"},
"/data/music/album1/song2": {"title": "Example Song", "artist": "Example Artist", "album": "Example Album"},
}
"""

import pickle, os, os.path, deflate, random
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from datetime import datetime
from io import BytesIO

class Database:
	def __init__(self, path):
		self.dbinfo = {}
		self.db = {}
		self.path = path.replace("\\", "/")
	def __loaddb(self):
		with open(os.path.join(self.path, "db.musdb"), "rb") as f:
			db = deflate.gzip_decompress(f.read())
		a = db.find(b"\n\n")
		for x in db[:a].split(b"\n"):
			data = x.split(b" ", 1)
			self.dbinfo[data[0].decode("utf-8")] = data[1].decode("utf-8")
		pickled = db[a+2:]
		self.db = pickle.loads(pickled)
		del db
	def __savedb(self):
		self.dbinfo["LU"] = datetime.utcnow()
		self.dbinfo["SC"] = len(self.db)
		mem = BytesIO()
		for key in self.dbinfo.keys():
			mem.write((key + " " + str(self.dbinfo[key]) + "\n").encode("utf-8"))
		mem.write(b"\n")
		mem.write(pickle.dumps(self.db))
		fileout = mem.getvalue()
		uncsize = len(fileout)
		compressed = deflate.gzip_compress(fileout, 12)
		comsize = len(compressed)
		with open(os.path.join(self.path, "db.musdb"), "wb") as f:
			f.write(compressed)
		del mem, compressed
	def get_random(self, amount):
		out = random.sample(list(self.db.items()), amount)
		return out
	def get(self, path):
		val = self.db.get(path.replace("\\", "/"))
		return val
	def getinfo(self, id):
		return self.dbinfo.get(id)
	def update(self):
		self.db = {}
		for root, dirs, files in os.walk(self.path):
			for f in files:
				if f.endswith(".mp3"):
					path = os.path.join(root, f)
					mp3 = MP3(path, ID3=EasyID3)
					md = dict(mp3)
					md["duration"] = mp3.info.length
					self.db[path.replace("\\", "/").replace(self.path, "")] = md
		self.__savedb()
	def load(self):
		self.__loaddb()