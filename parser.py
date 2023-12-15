import os
import pandas as pd
import os
import glob
import json
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

    

def parse(date):
    returnJson = {}
    returnJson["error"] = ""
    returnJson["success"] = True
    try:        
        download_directory = os.getcwd()+"/downloads"
        list_of_files = glob.glob(os.path.join(download_directory, '*'))
        latest_file = max(list_of_files, key=os.path.getctime)
        current_file_name = os.path.basename(latest_file)
        new_file_name = "downloaded_spreadsheet.xlsx"
        new_file_path = os.path.join(download_directory, new_file_name)
        os.rename(latest_file, new_file_path)
    except:
        print("Error in renaming the file")
        returnJson["error"] = "Error in renaming the file"
        returnJson["success"] = False

    try:
        excel_file_path = os.getcwd() + "/downloads/downloaded_spreadsheet.xlsx"
        df = pd.read_excel(excel_file_path, engine="openpyxl")
        parsed_list = df.values.tolist()
        parsed_list = parsed_list[8:30]
        returnJson.update(makeJSON(parsed_list))
        input_date = datetime.strptime(date, '%Y-%m-%d')
        output_date_str = input_date.strftime('%B %d, %Y')
        returnJson["description"] = "Rates for "+output_date_str
        os.remove(os.getcwd()+"/downloads/downloaded_spreadsheet.xlsx")
        
    except:
        print("Some error in reading the file and converting it to json")
        returnJson["error"] = "Error in reading the file"
        returnJson["success"] = False
        os.remove(os.getcwd()+"/downloads/downloaded_spreadsheet.xlsx")
    
    return json.dumps(returnJson)



if __name__ == "__main__":
    print(parse("2023-12-11"))