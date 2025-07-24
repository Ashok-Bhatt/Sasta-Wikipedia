from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({"message" : "Hello! Welcome to sasta wikipedia! Search anything you want to"})

@app.route("/search/<title>")
def search(title):

    driver = None
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        web_url = f"https://en.wikipedia.org/wiki/{title}"

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(web_url)

        paragraphs = driver.find_elements(By.TAG_NAME, value="p")
        result = []

        for paragraph in paragraphs:
            result.append(paragraph.text)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "message" : "Couldn't search",
            "error" : e,
        })
    finally:
        driver.close()

if __name__ == "__main__":
    app.run(debug=True)