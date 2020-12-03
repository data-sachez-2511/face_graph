from peewee import *

from .config import cfg


class Face(Model):
    id = BigIntegerField(unique=True)
    face_blob = BlobField()
    meta = TextField()
    neighbors = TextField()


class ResultStorage:
    db: SqliteDatabase

    def __init__(self):
        self.db = SqliteDatabase(cfg.db_path)
        # self.db = SqliteDatabase(cfg.db_path, pragmas={
        #     'journal_mode': 'wal',
        #     'synchronous': '0',
        #     'locking_mode': 'EXCLUSIVE'
        # })
        self.db.connect()
        self.db.bind([Face])
        self.db.create_tables([Face])
