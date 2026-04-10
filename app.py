from flask import Flask
from main import CONFIG
import subprocess

app = Flask(__name__)
sqlite_path = CONFIG["STORE_PATH"]

@app.route(f"/")
def greet():
    subprocess.run(["/home/luc/Programs/Python/icewatch/dockerRun.sh"], shell=False)
    return