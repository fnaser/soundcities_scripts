import subprocess

dir_path = "/home/fnaser/Music/"
file_name = "test" # mp3 file

subprocess.call(['ffmpeg', '-i', dir_path + file_name + '.mp3', dir_path + file_name + '.wav'])
