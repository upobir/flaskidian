from app import app
from app.data_store import DataStore

if __name__ == "__main__":
    if DataStore.test():
        DataStore.initialize()
        app.run()
