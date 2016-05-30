from flask import Flask, request, send_from_directory
from peewee import *
from datetime import datetime
import serial

DATABASE = 'homeapp.db'

db = SqliteDatabase(DATABASE)


class BaseModel(Model):
    class Meta:
        database = db


class Timer(BaseModel):
    id
    set_time = DateTimeField()
    end_time = DateTimeField()

    class Meta:
        order_by = ('end_time',)


class Command(BaseModel):
    id
    name = CharField()

    class Meta:
        order_by = ('name',)


def create_tables():
    db.connect()  # close?
    db.create_tables([Timer])
    db.create_tables([Command])


app = Flask(__name__, static_url_path='')
from app import views
