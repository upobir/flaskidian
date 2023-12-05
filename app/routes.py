import threading
import time
import os

from flask import render_template
from app import app, redis_store


def long_running_task():
    redis_store.set("reading_notes", "true")  # race condition here
    try:
        notes_location = app.config["NOTES_LOCATION"]

        if not os.path.isdir(notes_location):
            print("Notes location is not a directory")
            return

        redis_store.delete("notes")

        for filename in os.listdir(notes_location):
            if os.path.isfile(os.path.join(notes_location, filename)):
                redis_store.lpush("notes", filename)

    except Exception as e:
        print(e)
    finally:
        redis_store.set("reading_notes", "false")
    return


@app.route("/")
def home():
    if redis_store.get("reading_notes") is None:
        redis_store.set("reading_notes", "false")

    if (
        redis_store.llen("notes") == 0
        and redis_store.get("reading_notes").decode("utf-8") == "false"
    ):
        print("starting task")
        task_thread = threading.Thread(target=long_running_task)
        task_thread.start()

    is_loading = redis_store.get("reading_notes").decode("utf-8") == "true"
    note_count = redis_store.llen("notes")

    return render_template("home.html", is_loading=is_loading, note_count=note_count)
