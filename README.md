# Flaskidian
I have a huge obsidian notes archive, and I wanted to make a web app to do some stuff with them. So this is a simple monolithic flask app for that.

# Setup
Create virtual environment and install requirements
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Make a `config.py` file in root folder, and create `Config` class inheriting from `ConfigBase` class in `config_base.py`.

# Run
```bash
python3 run.py
```