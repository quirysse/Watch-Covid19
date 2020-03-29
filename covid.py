from CountryDatabase import CountryDatabase
import numpy as np
import matplotlib.pyplot as plt

import math

from plot import plot


help="""This program parses Covid-19 data fetched from Johns Hopkins CSSE and creates some HTML plots.

Usage: covid.py [-hpuo FOLDER] [-s | -a] [-n <count>] [-b <start>]
       covid.py [-hpuo FOLDER] [-s | -a] [-c "countrylist"] [-b <start>]

Options.
-h --help    show this
-u --update  update database from online source
-o --output FOLDER    specify output folder instead of opening web browser
-n count --number count number of countries to display [default: 10]
-b start --begin start starting point (first day the number of case/death reach that level) [default: 100]
-s --speed   plot the progression rate (speed) instead of the cummulative case [default: False]
-a --acceleration   plot the variation of the progression rate (acceleration) instead of the cummulative case [default: False]
-c "list" --countries "list" space separared list of ISO 3166-1 alpha-2 country code
-p --population  plot the numbers as a ratio of the country population (by million inhabitants) [default: False]

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

    print(arguments)

    begin = int(arguments["--begin"]) if arguments["--begin"] is not None else 100
    
    db = CountryDatabase()

    derive_order = 0
    if arguments["--speed"] :
        derive_order = 1
    elif arguments["--acceleration"]:
        derive_order = 2

    if arguments["--countries"] is not None:
        countries = db.GetFromList( arguments["--countries"].upper().split() )
    else:
        countries = db.Head()
    
    plotlist = countries

    plotlist[ "QC" ] = db.GetCountry("QC")
    plotlist[ "CA" ] = db.GetCountry("CA")
    plot(plotlist, threshold=begin, derivecount=derive_order, bypopulation=arguments["--population"], outputfile=arguments["--output"])



    
