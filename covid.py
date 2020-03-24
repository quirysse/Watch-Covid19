 #Load the Pandas libraries with alias 'pd' 
from dbutils import create_connection, create_table
from setup_countries import InitCountryData, GetCountry
from setup_reports import  GetDeaths, GetConfirmed, GetRecovered
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from scipy.signal import savgol_filter


DBFILE = "database.db"

def setup_database(conn):
    InitCountryData(conn)
    conn.commit()

def plot(coutries, report, threshold=50):
    
    fig = go.Figure()
    for c in countries:
        coutry_code = c[0]
        country = GetCountry(conn, coutry_code)
        time_series = report[ coutry_code ]
        time_series[time_series < threshold ] = 0
        time_series = np.trim_zeros(time_series, 'f')# / country["population"] * 1000000
        
        print(country["name"], len(time_series), time_series )
        #p = plt.plot( time_series, c[1], label=coutry_code )

        signal = savgol_filter(time_series, 5, 3)

        fig.add_trace(go.Scatter(
            y=BaseRate(signal),
            mode='lines',
            name=coutry_code
        ))

    fig.show()
    # plt.legend(loc='upper left', borderaxespad=0.)
    # plt.show()

def BaseRate(x):
    return x[1:]/x[:len(x)-1]

if __name__ == "__main__":
    conn = create_connection(DBFILE)
    setup_database(conn)
    
    report_conf = GetConfirmed(conn)
    report_death = GetDeaths(conn)
    report_recov = GetRecovered(conn)

    countries = ( ("CA", "r"), ("US", "g"), ("IT", "b"), ("FR", "k"), ("DE", "y"), ("CN", "c"), ("ES", "m") )
    countries = ( ("CA", "r"), ("US", "g"), ("IT", "b"), ("FR", "k"), ("DE", "y"), ("ES", "m") )
    plot(countries, report_death, threshold=5)
    # df = px.data.gapminder().query("country=='Canada'")
    # fig = px.line(df, x="year", y="lifeExp", title='Life expectancy in Canada')
    # fig.show()



    
