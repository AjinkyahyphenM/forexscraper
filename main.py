from crypt import methods
from distutils.debug import DEBUG
from flask import Flask, jsonify
import scraper

app = Flask(__name__)

@app.route('/api/<string:date>', methods = ["GET"])
def getData(date):
    data = scraper.scrape(date)
    return data

if __name__ == "__main__":
    app.run()
