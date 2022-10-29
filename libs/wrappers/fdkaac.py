import os.path
import subprocess

class FdkAAC:
	def __init__(self, fdkaac_path, ffmpeg_path):
		self.fdkaac_path = fdkaac_path
		self.ffmpeg_path = ffmpeg_path
	def encode(self, bitrate, profile, finput, output, overwrite=False):
		if overwrite:
			if os.path.isfile(output):
				os.remove(output)
			elif os.path.isdir(output):
				raise IsADirectoryError(output, "is a directory")
		if not os.path.exists(output):
			cmd = "{} {} -p {} -b {} -o {}".format(self.fdkaac_path, finput, profile, bitrate, output)
			p = subprocess.Popen(cmd.split())
			p.communicate()
			if p.returncode != 0:
				raise Exception("There was an error while encoding using Exhale")
	def ffmpeginput_encode(self, bitrate, profile, finput, output, overwrite=False, channels=2):
		if overwrite:
			if os.path.isfile(output):
				os.remove(output)
			elif os.path.isdir(output):
				raise IsADirectoryError(output, "is a directory")
		if not os.path.exists(output):
			cmd = "{} -i {} -ac {} -f wav - | {} - -p {} -b {} -o {}".format(self.ffmpeg_path, finput, channels, self.fdkaac_path, profile, bitrate, output)
			p = subprocess.Popen(cmd.split(), shell=True)
			p.communicate()
			if p.returncode != 0:
				raise Exception("There was an error while encoding using Exhale")