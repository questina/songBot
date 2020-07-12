from peewee import *

database = SqliteDatabase('users.db')


class BaseModel(Model):
    class Meta:
        database = database


class User(BaseModel):
    username = CharField(unique=True)
    join_date = DateField()
    score = IntegerField()


class Point(BaseModel):
    score = IntegerField()
    question = TextField()
    wrong_answer = TextField()
    right_answer = TextField()
    reaction = TextField()

