import os
import pandas as pd 
import numpy as np

from dbutils import create_connection, create_table, select_from_table
from setup_countries import COUNTRY_TABLE, COUNTRYCODE_TABLE

CONFIRMED="COVID-19\\csse_covid_19_data\\csse_covid_19_time_series\\time_series_19-covid-Confirmed.csv"
DEATH="COVID-19\\csse_covid_19_data\\csse_covid_19_time_series\\time_series_19-covid-Death.csv"
RECOVERD="COVID-19\\csse_covid_19_data\\csse_covid_19_time_series\\time_series_19-covid-Recovered.csv"

REPORT_FOLDER="COVID-19\\csse_covid_19_data\\csse_covid_19_daily_reports"

STATE_TOKEN = "Province/State"
COUNTRY_TOKEN = "Country/Region"
UPDATE_TOKEN = "Last Update"
CONFIRMED_TOKEN = "Confirmed"
DEATHS_TOKEN = "Deaths"
RECOVERED_TOKEN = "Recovered"

def load_data():
    # Read data from file 'filename.csv' 
    # (in the same directory that your python process is based)
    # Control delimiters, rows, column names with read_csv (see later) 
    
    #return pd.read_csv( os.path.join(REPORT_FOLDER, "03-21-2020.csv") ) 
    return pd.read_csv( CONFIRMED ) 

def SaveCountriesCSV(countries):
    import csv
    with open('count.csv', 'w') as f:
        for key in countries.keys():
            f.write("%s;%s\n"%(key, countries[key]))

def GetReports(conn):

    def GetCode(coutry_name):
        cur = conn.cursor()
        cur.execute("SELECT isocode FROM " + COUNTRYCODE_TABLE + " WHERE name=?", (coutry_name,))
        return cur.fetchall()[0][0]

    data = load_data()
    colnumber = len(data.columns)
    colstart = 4

    countries = {}
    for index, row in data.iterrows():
        code =  GetCode(row[COUNTRY_TOKEN])
        series = np.array( row[colstart:] )
        if not code in countries:
            countries[code] = series
        else:
            countries[code] = np.add(countries[code], series)

    return countries

    # # print(countries["CA"])
    # print(countries)
    # print(countries["CA"].shape)