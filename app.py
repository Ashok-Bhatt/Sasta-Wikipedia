from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from flask import Flask, jsonify
import time

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({"message" : "Hello! Welcome to sasta wikipedia! Search anything you want to"})

@app.route("/search/<title>")
def search(title):

    driver = None
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_experimental_option("detach", True)

        web_url = f"https://en.wikipedia.org/wiki/{title}"

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(web_url)

        time.sleep(1)

        paragraphs = driver.find_elements(By.TAG_NAME, value="p")
        result = []

        for paragraph in paragraphs:
            result.append(paragraph.text)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "message" : "Couldn't search",
            "error" : str(e),
        })
    finally:
        if (driver):
            driver.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)