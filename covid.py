 #Load the Pandas libraries with alias 'pd' 
from dbutils import create_connection, create_table
from setup_countries import InitCountryData, GetCountry
from setup_reports import  GetDeaths, GetConfirmed, GetRecovered
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import math
from scipy.signal import savgol_filter


DBFILE = "database.db"

def setup_database(conn):
    InitCountryData(conn)
    conn.commit()

def plot(report, threshold=50):
    
    filter_windowsize = 5000000000000
    fig = go.Figure()
    for country_code,  time_series in report.items():

        time_series[time_series < threshold ] = 0
        time_series = np.trim_zeros(time_series, 'f') # / country["population"] * 1000000
        
        #print(country["name"], len(time_series), time_series )
        #p = plt.plot( time_series, c[1], label=country_code )

        signal = time_series#savgol_filter(time_series, 5, 3)

        if len(time_series) > filter_windowsize :
            signal = savgol_filter(time_series, filter_windowsize, 3)
#        signal = savgol_filter( DaysToMultiplyBy(time_series, 2.), 9, 3)

#        signal = Derive(signal)

        fig.add_trace(go.Scatter(
            y=signal,
            mode='lines',
            name=country_code
        ))

    fig.show()
    # plt.legend(loc='upper left', borderaxespad=0.)
    # plt.show()

def BaseRate(x):
    return np.asarray( x[1:]/x[:len(x)-1] )

def Derive(x):
    return np.asarray( x[1:]-x[:len(x)-1] )

def DaysToMultiplyBy(x, alpha):
    y = BaseRate(x)
    return np.log(alpha) / np.log(y)

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
    conn = create_connection(DBFILE)
    setup_database(conn)
    
    report_conf = GetConfirmed(conn)
    report_death = GetDeaths(conn)
    report_recov = GetRecovered(conn)

    plot_report = report_conf

    countries = ( ("CA", "r"), ("US", "g"), ("IT", "b"), ("FR", "k"), ("DE", "y"), ("CN", "c"), ("ES", "m") )
    countries = ( ("CA", "r"), ("US", "g"), ("IT", "b"), ("FR", "k"), ("DE", "y"), ("ES", "m") )
    #countries = ( "US", "IT", "FR", "DE", "ES", "CN" )
    countries = ( "QC", "FR", "CA", "IT" )

    customlist = GetReportFromList(plot_report, countries)
    toplist = Head(plot_report, 5)
    
    plotlist = toplist

    plotlist[ "QC" ] = plot_report["QC"]
    plot(plotlist, threshold=100)

    #plot(countries, report_conf, threshold=50)
    # df = px.data.gapminder().query("country=='Canada'")
    # fig = px.line(df, x="year", y="lifeExp", title='Life expectancy in Canada')
    # fig.show()



    
