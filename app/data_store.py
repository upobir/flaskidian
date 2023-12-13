from flask_redis import FlaskRedis

from app import app


class DataStore:
    redis_store = FlaskRedis(app)

    @classmethod
    def test(cls):
        try:
            cls.redis_store.ping()
            return True
        except Exception:
            print()
            print("!!! Could not connect to Redis")
            print()
            return False

    @classmethod
    def initialize(cls):
        if cls.redis_store.exists("flaskidian_initialized"):
            return
        cls.redis_store.set("reading_notes", "false")
        cls.redis_store.delete("notes")
        cls.redis_store.set("flaskidian_initialized", "true")
        print("Initialized Flaskidian data store in Redis")

    @classmethod
    def get_reading_notes(cls):
        return cls.redis_store.get("reading_notes").decode("utf-8") == "true"

    @classmethod
    def set_reading_notes(cls, value):
        string_value = "true" if value else "false"
        cls.redis_store.set("reading_notes", string_value)

    @classmethod
    def get_notes_count(cls):
        return cls.redis_store.llen("notes")

    @classmethod
    def add_notes(cls, value):
        cls.redis_store.rpush("notes", value)

    @classmethod
    def delete_notes(cls):
        cls.redis_store.delete("notes")
