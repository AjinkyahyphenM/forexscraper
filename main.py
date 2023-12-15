from crypt import methods
from distutils.debug import DEBUG
from flask import Flask, jsonify
import scraper

app = Flask(__name__)

# @app.route('/api/<string:date>', methods = ["GET"])
# def getData(date):
#     data = scraper.scrape(date)
#     return data

@app.route("", methods = ["GET"])
def home():
    return "Hello, world"

if __name__ == "__main__":
    app.run()
