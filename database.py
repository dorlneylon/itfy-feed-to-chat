from peewee import SqliteDatabase, Model
from peewee import IntegerField, CharField, PrimaryKeyField, TimestampField
from pathlib import Path
from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini", encoding="utf-8")

db = SqliteDatabase(Path.cwd() / config.get('main', 'database_file'))


class BaseModel(Model):
    class Meta:
        database = db


class Topic(BaseModel):
    id = PrimaryKeyField(null=False)
    title = CharField()
    link = CharField()
    ext_id = IntegerField()
    saved_on = TimestampField()
    announced_on = TimestampField()

    class Meta:
        db_table = 'topics'


db.connect()
if not Topic.table_exists():
    Topic.create_table()