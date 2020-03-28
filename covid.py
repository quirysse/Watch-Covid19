 #Load the Pandas libraries with alias 'pd' 
from dbutils import create_connection, create_table
from setup_countries import InitCountryData, GetCountry
from setup_reports import  Reports
import numpy as np
import matplotlib.pyplot as plt

import math

from plot import plot


help="""This program parses Covid-19 data fetched from Johns Hopkins CSSE and creates some HTML plots.

Usage: covid.py [-huo FOLDER]

Options.
-h --help    show this
-u --update  update database from online source
-o --output FOLDER    specify output folder instead of opening web browser

This depends 2019 Novel Coronavirus COVID-19 (2019-nCoV) Data Repository by Johns Hopkins CSSE available at https://github.com/CSSEGISandData/COVID-19.git
"""
from docopt import docopt

DBFILE = "database.db"

def setup_database(conn, force_update=False):
    InitCountryData(conn, force_update)
    if force_update :
        conn.commit()  

def Head(countries, n=10) : 
    ret = {}

    for key, value in sorted(countries.items(), key=lambda kv : kv[1][-1], reverse=True):
        ret[key] = value
        n = n-1
        if n == 0:
            return ret

def GetReportFromList(report, isocodelist):
    ret = {}
    for code in isocodelist:
        ret[code] = report[code]
    
    return ret

if __name__ == "__main__":

    arguments = docopt(help)
    print(arguments)

    conn = create_connection(DBFILE)
    setup_database(conn, arguments['--update'])
    
    rep = Reports(conn)
    
    report_conf = rep.Confirmed
    report_death = rep.Deaths
    report_recov = rep.Recovered

    plot_report = report_conf

    countries = ( ("CA", "r"), ("US", "g"), ("IT", "b"), ("FR", "k"), ("DE", "y"), ("CN", "c"), ("ES", "m") )
    countries = ( ("CA", "r"), ("US", "g"), ("IT", "b"), ("FR", "k"), ("DE", "y"), ("ES", "m") )
    #countries = ( "US", "IT", "FR", "DE", "ES", "CN" )
    countries = ( "QC", "FR", "CA", "IT" )

    customlist = GetReportFromList(plot_report, countries)
    toplist = Head(plot_report, 10)
    
    plotlist = toplist

    plotlist[ "QC" ] = plot_report["QC"]
    plot(plotlist, threshold=100, outputfile=arguments["--output"])



    
