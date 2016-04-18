from flask import Flask, request, send_from_directory

app = Flask(__name__, static_url_path='')
from app import views