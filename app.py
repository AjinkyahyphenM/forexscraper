from crypt import methods
from distutils.debug import DEBUG
from flask import Flask, jsonify
import scraper
import requests
import io
import pandas as pd
from datetime import datetime


def makeJSON(parsed_list):
    
    res = []
    for row in parsed_list:
       res_dict = {}
       res_dict["country"] = str(row[0])
       res_dict["currency_code"] = str(row[2])
       res_dict["units"] = str(row[3])
       res_dict["buying_tt"] = str(row[4])
       res_dict["buying_dd"] = str(row[5])
       res_dict["buying_notes"] = str(row[6])
       res_dict["selling_tt"] = str(row[7])
       res_dict["selling_dd"] = str(row[8])
       res_dict["selling_notes"] = str(row[9])
       res_dict["rate_date"] = str(row[10])
       res.append(res_dict)
       
    return {"data":res}


def new_scraper(date):

    returnJson = {}
    url = "https://mcb.mu/webapi/mcb/ForexDataExcel"
    page = requests.post(url=url, data={"StartDate": date, "EndDate": date, "CurrencyCode": "ALL", "BaseCurrency": "MUR"})
    df = pd.read_excel(io.BytesIO(page.content), engine='openpyxl')
    parsed_list = df.values.tolist()
    parsed_list = parsed_list[8:30]
    returnJson.update(makeJSON(parsed_list))
    input_date = datetime.strptime(date, '%Y-%m-%d')
    output_date_str = input_date.strftime('%B %d, %Y')
    returnJson["description"] = "Rates for "+output_date_str
    return returnJson



app = Flask(__name__)

@app.route('/api/<string:date>', methods = ["GET"])
def getData(date):
    print(date)
    data = new_scraper(date)
    return data

# @app.route("/", methods = ["GET"])
# def home():
#     return "Hello, world"

if __name__ == "__main__":
    app.run()
