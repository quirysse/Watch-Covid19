 #Load the Pandas libraries with alias 'pd' 

from CountryDatabase import CountryDatabase
import numpy as np
import matplotlib.pyplot as plt

import math

from plot import plot


help="""This program parses Covid-19 data fetched from Johns Hopkins CSSE and creates some HTML plots.

Usage: covid.py [-huo FOLDER] [-n <count>]
       covid.py [-huo FOLDER] [-c "countrylist"]

Options.
-h --help    show this
-u --update  update database from online source
-o --output FOLDER    specify output folder instead of opening web browser
-n count --number count number of countries to display [default: 10]
-c "list" --countries "list" space separared list of ISO 3166-1 alpha-2 country code

This depends 2019 Novel Coronavirus COVID-19 (2019-nCoV) Data Repository by Johns Hopkins CSSE available at https://github.com/CSSEGISandData/COVID-19.git
"""
from docopt import docopt








def GetCountriesFromArguments(plot_report, parselist):
    countries = parselist.upper().split()
    return GetReportFromList(plot_report, countries)


if __name__ == "__main__":

    arguments = docopt(help)
    country_number = 10
    if arguments["--number"] is not None :
        country_number = int(arguments["--number"])

    # print(arguments)

    
    db = CountryDatabase()
    
    report_conf = db.report.Confirmed
    report_death = db.report.Deaths
    report_recov = db.report.Recovered

    plot_report = report_conf


    if arguments["--countries"] is not None:
        countries = db.GetFromList( arguments["--countries"].upper().split() )
    else:
        countries = db.Head()
    
    plotlist = countries

    plotlist[ "QC" ] = db.GetCountry("QC")
    plot(plotlist, threshold=100, outputfile=arguments["--output"])



    
