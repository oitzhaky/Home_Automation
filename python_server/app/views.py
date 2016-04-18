from app import app
from flask import redirect 
import os

def writeToFile(s):
	 file_path = os.path.normpath('app/static/file.txt')
	 file = open(file_path, 'w')
	 file.write(s)
	 num = file.close()
	 print(num)

@app.route('/')
@app.route('/index')
def index():
	return app.send_static_file('index.html')
@app.route('/lightsOn', methods=['POST'])
def lightsOn():
	writeToFile("1")
	return "lights-ON"
@app.route('/lightsOff', methods=['POST'])
def lightsOff():
	writeToFile("0")
	return "lights-OFF"
@app.route('/turnMusicOn')
def turnMusicOn():
	 file_path = os.path.normpath('app/static/movie.mp4')
	 os.startfile(file_path)
	