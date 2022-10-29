import os.path
import subprocess

class Exhale:
	def __init__(self, exhale_path, ffmpeg_path):
		self.exhale_path = exhale_path
		self.ffmpeg_path = ffmpeg_path
	def encode(self, preset, finput, output, overwrite=False):
		if overwrite:
			if os.path.isfile(output):
				os.remove(output)
			elif os.path.isdir(output):
				raise IsADirectoryError(output, "is a directory")
		if not os.path.exists(output):
			cmd = "{} {} {} {}".format(self.exhale_path, preset, finput, output)
			p = subprocess.Popen(cmd.split())
			p.communicate()
			if p.returncode != 0:
				raise Exception("There was an error while encoding using Exhale")
	def ffmpeginput_encode(self, preset, finput, output, overwrite=False, channels=2):
		if overwrite:
			if os.path.isfile(output):
				os.remove(output)
			elif os.path.isdir(output):
				raise IsADirectoryError(output, "is a directory")
		if not os.path.exists(output):
			cmd = "{} -i {} -ac {} -f wav - | {} {} {}".format(self.ffmpeg_path, finput, channels, self.exhale_path, preset, output)
			p = subprocess.Popen(cmd.split(), shell=True)
			p.communicate()
			if p.returncode != 0:
				raise Exception("There was an error while encoding using Exhale and FFmpeg")