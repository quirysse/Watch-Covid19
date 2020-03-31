import os
from os import path
import pandas as pd 
import numpy as np
import urllib.request
from git import Repo

from dbutils import create_connection, create_table, select_from_table
from setup_countries import COUNTRY_TABLE, COUNTRYCODE_TABLE

SOURCEURL="https://github.com/CSSEGISandData/COVID-19.git"

BASEDIR="COVID-19.data-git"
CONFIRMED=path.join(BASEDIR, "csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
DEATH=    path.join(BASEDIR, "csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
RECOVERD= path.join(BASEDIR, "csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv")

REPORT_FOLDER=path.join(BASEDIR, "csse_covid_19_data/csse_covid_19_daily_reports")

STATE_TOKEN = "Province/State"
COUNTRY_TOKEN = "Country/Region"
UPDATE_TOKEN = "Last Update"
CONFIRMED_TOKEN = "Confirmed"
DEATHS_TOKEN = "Deaths"
RECOVERED_TOKEN = "Recovered"

def load_data(file):
    return pd.read_csv( file ) 

def SaveCountriesCSV(countries):
    import csv
    with open('count.csv', 'w') as f:
        for key in countries.keys():
            f.write("%s;%s\n"%(key, countries[key]))


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

        #Special case to get some territories/pronvinces separately
        if row[STATE_TOKEN] == "Quebec" : 
            countries["QC"] = series

    return countries

def GetDeaths(conn):
    return GetReports(conn, DEATH)
    
def GetConfirmed(conn):
    return GetReports(conn, CONFIRMED)

def GetRecovered(conn):
    return GetReports(conn, RECOVERD)
    
def GetDataFromInternet():
    from git import RemoteProgress
    class MyProgressPrinter(RemoteProgress):
        def update(self, op_code, cur_count, max_count=None, message='---'):
            print(message)

    if not path.exists(BASEDIR) : 
        print('Cloning', SOURCEURL)
        Repo.clone_from(SOURCEURL, BASEDIR)
    else :
        print('Updating', SOURCEURL)
        Repo(BASEDIR).remotes.origin.pull()


def SetupData(forceupdate=False):
    if forceupdate or not path.exists(DEATH) or not path.exists(CONFIRMED) or not path.exists(RECOVERD) :
        GetDataFromInternet()

class Reports:

    def __init__(self, conn, forceupdate=False):
        SetupData(forceupdate)

        self.Deaths = GetDeaths(conn)
        self.Confirmed = GetConfirmed(conn)
        self.Recovered = GetRecovered(conn)

    def GetLastUpdateTime(self):
        import os.path, time
        return time.ctime( os.path.getmtime(CONFIRMED) )