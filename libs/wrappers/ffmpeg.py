import os.path
import subprocess

class FFmpeg:
	def __init__(self, ffmpeg_path):
		self.ffmpeg_path = ffmpeg_path
	def run(self, finput, output, options, overwrite=False):
		if overwrite:
			if os.path.isfile(output):
				os.remove(output)
			elif os.path.isdir(output):
				raise IsADirectoryError(output, "is a directory")
		if not os.path.exists(output):
			cmd = "{} -i {} {} {}".format(self.ffmpeg_path, finput, options, output)
			p = subprocess.Popen(cmd.split())
			p.communicate()
			if p.returncode != 0:
				raise Exception("There was an error while encoding using Exhale and FFmpeg")
	def run_pipe(self, finput, options):
		cmd = [
			self.ffmpeg_path,
			"-i", finput,
		]
		for x in options.split():
			cmd.append(x)
		cmd.append("-")
		p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
		return p