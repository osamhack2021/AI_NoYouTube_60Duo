# python -m pip install flask-ngrok
from flask import Flask
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
run_with_ngrok(app)

@app.route("/")
def home():
    return "<h1>This is your Flask server.</h1>"
app.run()

