from decouple import config
from peewee import MySQLDatabase

def conectar_db():
    return MySQLDatabase(
        config("db", default="turnomed"),
        charset="utf8mb4",
        host=config("host", default="localhost"),
        port=config("port", default=3306, cast=int),
        user=config("user", default="root"),
        password=config("password", default=""),
    )

database = conectar_db()
