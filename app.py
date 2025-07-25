from flask import Flask, jsonify
import os
from dotenv import load_dotenv
import requests

load_dotenv()

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({"message" : "Hello! Welcome to sasta wikipedia! Search anything you want to"})

@app.route("/search/<title>")
def search(title):

    TOKEN = os.getenv("BROWSERLESS_API_KEY")
    url = f"https://production-sfo.browserless.io/scrape?token={TOKEN}"
    headers = {
        "Cache-Control": "no-cache",
        "Content-Type": "application/json"
    }

    data = {
        "url": f"https://en.wikipedia.org/wiki/{title}",
        "elements": [
            { "selector": "p" }
        ],
        "waitForSelector": {
            "selector": "h1",
            "timeout": 1000
        }
    }

    api_response = requests.post(url, headers=headers, json=data)
    result = api_response.json()
    
    response = []

    for index, data in enumerate(result["data"][0]["results"]):
        response.append(data["text"])

    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)