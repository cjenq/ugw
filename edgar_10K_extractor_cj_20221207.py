# Extractor API info: https://sec-api.io/docs/sec-filings-item-extraction-api
# get your free API key at https://sec-api.io
    
# package installs - cmd window 
#  py -m pip install sec_api
#  py -m pip install beautifulsoup4

import requests
import json
import pandas as pd
import sec_api 
import time 
   
from sec_api import QueryApi


currapikey = "3f4acb8ac45a193f07c74e4cd2fbae64e6ab336b32997f70ab6fc6d8064cbe21"
#expired 
#currapikey = "46f91b5eec1ddba7b0a51939180b3d25f29912296aaad9b3b2d5a9c6d9b0673d"
#currapikey = "55ca5f0ee6afbd8b7bacf77596b90c58f1af91de7a6a8eacb7d0ed6ba3a6f211"
#currapikey = "2c54424ecf207f4f9ee969df13f02c5507e480c888c27814e8b3eebcfd65dbd0"
#currapikey = "f68c90e22c63c31c8b8ac24f933c1d1a3fc357b1c8a2afcf557284772901d427"


import pandas as pd
df = pd.read_csv("cik_sp500.csv")
print(df)

cik_list_int = df['cik'].tolist()


cik_list=[]
for i,a in enumerate(cik_list_int):
  cik_list.append(str(a))
print(cik_list)

#cik_list = cik_list[:331]

print("List of CIKs:",cik_list)


for cik in cik_list:
    print("cik=",cik)

    queryApi = QueryApi(api_key=currapikey)

    query = {
    "query": { "query_string": { 
        "query": "cik:" + cik + " AND filedAt:{2021-11-30 TO 2022-11-30} AND formType:\"10-K\"",
                }  
    },
    "from": "0",
    "size": "10",
    "sort": [
        { 
            "filedAt": { 
                "order": "desc" }
                }]
    }

    filings = queryApi.get_filings(query)
    #print(filings)
    #type(filings)
    #print(filings.keys())

    # loops over filings object to extract urls and create url_list_10K 

    num_filings = len((filings['filings']))
    url_list_10K = [None]*num_filings

    print("num_filings")
    print(num_filings)

    #input("Press any key to continue the program")

    for x in range(num_filings):
        url_10K = filings['filings'][x]['documentFormatFiles'][0]['documentUrl']
        #print(url_10K)
        url_list_10K[x] = url_10K

    #print("url_list_10K")
    #print(url_list_10K)

    extractor_api_endpoint = "https://api.sec-api.io/extractor"

    #  Get items 1, 1A, 7, 7A in clear text from all of company's filings.
    item_list = ["1","1A","7","7A"]

    for url in url_list_10K:
        for item in item_list: 
            #print("looping through url: ", url)
            print("looping through item: ", item)
            
            
            time.sleep(0.1)
            final_url = extractor_api_endpoint + "?url=" + url + "&item="+ item +"&type=text&token=" + currapikey 
            print("final_url",final_url)
            response = requests.get(final_url)
            
            filename = "10K_"+cik + "_item"+ item
            txt_filename = "extract_10K/txt_output/" + filename + ".txt" 

            with open(txt_filename, "w") as f:
                f.write(response.text)
            f.close()

