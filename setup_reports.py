import os
import pandas as pd 
import numpy as np

from dbutils import create_connection, create_table, select_from_table
from setup_countries import COUNTRY_TABLE, COUNTRYCODE_TABLE

CONFIRMED="COVID-19.data\\csse_covid_19_data\\csse_covid_19_time_series\\time_series_covid19_confirmed_global.csv"
DEATH=    "COVID-19.data\\csse_covid_19_data\\csse_covid_19_time_series\\time_series_covid19_deaths_global.csv"
RECOVERD= "COVID-19.data\\csse_covid_19_data\\csse_covid_19_time_series\\time_series_covid19_recovered_global.csv"

REPORT_FOLDER="COVID-19.data\\csse_covid_19_data\\csse_covid_19_daily_reports"

STATE_TOKEN = "Province/State"
COUNTRY_TOKEN = "Country/Region"
UPDATE_TOKEN = "Last Update"
CONFIRMED_TOKEN = "Confirmed"
DEATHS_TOKEN = "Deaths"
RECOVERED_TOKEN = "Recovered"

def load_data(file):
    # Read data from file 'filename.csv' 
    # (in the same directory that your python process is based)
    # Control delimiters, rows, column names with read_csv (see later) 
    
    #return pd.read_csv( os.path.join(REPORT_FOLDER, "03-21-2020.csv") ) 
    return pd.read_csv( file ) 

def SaveCountriesCSV(countries):
    import csv
    with open('count.csv', 'w') as f:
        for key in countries.keys():
            f.write("%s;%s\n"%(key, countries[key]))


# def SortCountries(countries):


def GetReports(conn, filename):

    def GetCode(coutry_name):
        cur = conn.cursor()
        cur.execute("SELECT isocode FROM " + COUNTRYCODE_TABLE + " WHERE name=?", (coutry_name,))
        return cur.fetchone()["isocode"]

    data = load_data(filename)
    colnumber = len(data.columns)
    colstart = 4

    countries = {}
    for index, row in data.iterrows():
        try:
            code =  GetCode(row[COUNTRY_TOKEN])
        except:
            print("Missing country: " + str(row[COUNTRY_TOKEN]))
            continue

        series = np.array( row[colstart:], dtype=np.float )
        if not code in countries:
            countries[code] = series
        else:
            countries[code] = np.add(countries[code], series)

        if row[STATE_TOKEN] == "Quebec" : 
            countries["QC"] = series

    return countries

def GetDeaths(conn):
    return GetReports(conn, DEATH)
    
def GetConfirmed(conn):
    return GetReports(conn, CONFIRMED)

def GetRecovered(conn):
    return GetReports(conn, RECOVERD)
    