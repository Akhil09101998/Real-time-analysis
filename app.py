import requests
from bs4 import BeautifulSoup
import pandas as pd
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





def get_data(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text,"html.parser")

    # HTML of table
    get_full_table = soup.find('table', class_ = 'tableStyle')
    

    # Getting the header of LZ_NORTH
    header_outer = get_full_table.find("tr")
    header_inner = header_outer.find_all('th',class_ = "headerValueClass")
    region = header_inner[-4].text

    # Getting the values of LZ_NORTH from table
    values = get_full_table.find_all("tr")
    values = values[1:]

    d = {
        "Date": [],
        "Price": []
        }

    for i in values:
        for j  in i.find_all('td',class_ = "labelClassCenter")[-4]:
            date = values[0].find_all('td',class_ = "labelClassCenter")[0].text
            d['Date'].append(date)
            d['Price'].append(j)

    #Creating a DataFrame      
    df = pd.DataFrame(d)
    #df.to_csv("ak.csv")
    return {
        "final_data" : d
    }

url = 'https://www.ercot.com/content/cdr/html/real_time_spp.html'

@app.get('/')
def index():
    return get_data(url)
    
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)