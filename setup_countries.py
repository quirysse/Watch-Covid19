
import urllib.request
import json
import os.path
import pandas as pd 
from dbutils import create_connection, create_table

DATAURL = "https://restcountries.eu/rest/v2/all"
DATAFILE = "countries.json"
COUNTRYCODE_FILE = "countrycodes.csv"
COUNTRY_TABLE = "countries"
COUNTRYCODE_TABLE = "countrycode"

def GetJsonFromInternet():
    url = DATAURL
    req = urllib.request.Request(url)
    r = urllib.request.urlopen(req).read()
    return json.loads(r.decode('utf-8'))

def GetJson():
    
    if os.path.isfile(DATAFILE):
        with open(DATAFILE) as json_file:
            data = json.load(json_file)
    else:
        data = GetJsonFromInternet()
        json_str = json.dumps(data, indent=4)
        text_file = open(DATAFILE, "w")
        text_file.write(json_str)
        text_file.close()

    return data

def CreateCountryCodeTable(conn):
    sql_create_table = """ CREATE TABLE IF NOT EXISTS """ + COUNTRYCODE_TABLE + """(
                                    name text PRIMARY KEY,
                                    isocode text NOT NULL
                                    ); """
    create_table(conn, sql_create_table)

def CreateCountryTable(conn):
    sql_create_table = """ CREATE TABLE IF NOT EXISTS """ + COUNTRY_TABLE + """(
                                    isocode text PRIMARY KEY,
                                        topLevelDomain text NOT NULL,
                                        capital text NOT NULL,
                                        latitude float,
                                        longitude float,
                                        area float,
                                        name text NOT NULL,
                                        flagurl text,
                                        population int
                                    ); """
    create_table(conn, sql_create_table)


def AddCountryCode(conn, country):
        sql = ''' INSERT OR REPLACE INTO ''' + COUNTRYCODE_TABLE + '''(name, 
                                        isocode
                                        )
                VALUES(?,?) '''
        cur = conn.cursor()
        cur.execute(sql, country)
        return cur.lastrowid


def AddCountry(conn, countrycode):
        sql = ''' INSERT OR REPLACE INTO ''' + COUNTRY_TABLE + '''(isocode, 
                                        topLevelDomain, 
                                        capital,
                                        latitude,
                                        longitude,
                                        area,
                                        name,
                                        flagurl,
                                        population)
              VALUES(?,?,?,?,?,?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, countrycode)
        return cur.lastrowid

def FillCountryCode(conn):
    data = pd.read_csv( COUNTRYCODE_FILE, header=None, sep=';', na_filter=False) 
    for index, row in data.iterrows():
        code = (row[0], row[1])
        AddCountryCode(conn, code )

def FillCountries(conn):
    data = GetJson()
    for country in data:
        if(len( country['latlng']) == 2) :
            c = (
                    country['alpha2Code'],
                    country['topLevelDomain'][0],
                    country['capital'],
                    country['latlng'][0],
                    country['latlng'][1],
                    country['area'],
                    country['name'],
                    country['flag'],
                    country['population'] )
            AddCountry(conn, c)

def GetCountry(conn, isocode):
        cur = conn.cursor()
        cur.execute("SELECT * FROM " + COUNTRY_TABLE + " WHERE isocode=?", (isocode,))
        return cur.fetchone()

def InitCountryData(conn): 
    CreateCountryTable(conn)
    CreateCountryCodeTable(conn)

    FillCountries(conn)
    FillCountryCode(conn)

    
