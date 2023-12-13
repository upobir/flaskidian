import threading
import time
import os

from flask import render_template
from flask_restful import Resource

from app import app, api
from app.data_store import DataStore


def long_running_task():
    DataStore.set_reading_notes(True)  # race condition here

    try:
        notes_location = app.config["NOTES_LOCATION"]

        if not os.path.isdir(notes_location):
            print("Notes location is not a directory")
            return

        DataStore.delete_notes()

        for filename in os.listdir(notes_location):
            if os.path.isfile(os.path.join(notes_location, filename)):
                DataStore.add_notes(filename)

    except Exception as e:
        print(e)
    finally:
        DataStore.set_reading_notes(False)
    return


@app.route("/")
def home():
    if DataStore.get_notes_count() == 0 and DataStore.get_reading_notes() == False:
        print("starting task")
        task_thread = threading.Thread(target=long_running_task)
        task_thread.start()

    is_loading = DataStore.get_reading_notes()
    note_count = DataStore.get_notes_count()

    return render_template("home.html", is_loading=is_loading, note_count=note_count)


class Notes(Resource):
    def get(self):
        return [], 200


api.add_resource(Notes, "/api/notes")
