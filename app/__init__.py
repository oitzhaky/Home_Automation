from flask import Flask, request, send_from_directory
from peewee import *
from datetime import datetime

DATABASE = 'homeapp.db'

db = SqliteDatabase(DATABASE)

class BaseModel(Model): 
    class Meta: 
        database = db 

class Timer(BaseModel): 
    set_time = DateTimeField() 
    end_time = DateTimeField()
 
    class Meta: 
        order_by = ('end_time',)

def create_tables():
    db.connect()
    db.create_tables([Timer])

app = Flask(__name__, static_url_path='')
from app import views
