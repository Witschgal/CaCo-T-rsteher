from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "✅ Der Bot läuft!"

def run():
    app.run(host='0.0.0.0', port=8080)  # Port 8080 unbedingt angeben!

def keep_alive():
    t = Thread(target=run)
    t.start()
