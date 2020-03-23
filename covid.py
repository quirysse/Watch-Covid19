 #Load the Pandas libraries with alias 'pd' 
from dbutils import create_connection, create_table
from setup_countries import InitCountryData, GetCountry
from setup_reports import  GetDeaths, GetConfirmed, GetRecovered
import numpy as np
import matplotlib.pyplot as plt


DBFILE = "database.db"

def setup_database(conn):
    InitCountryData(conn)
    conn.commit()

def plot(coutries, report):
    for c in countries:
        coutry_code = c[0]
        country = GetCountry(conn, coutry_code)
        time_series = report[ coutry_code ]
        time_series[time_series < 50 ] = 0
        time_series = np.trim_zeros(time_series, 'f') / country["population"] * 1000000
        
        print(country["name"], len(time_series), time_series )
        p = plt.plot( time_series, c[1], label=coutry_code )

    plt.legend(loc='upper left', borderaxespad=0.)
    plt.show()

if __name__ == "__main__":
    conn = create_connection(DBFILE)
    setup_database(conn)
    
    
    report_conf = GetConfirmed(conn)
    report_death = GetDeaths(conn)
    report_recov = GetRecovered(conn)

    countries = ( ("CA", "r"), ("US", "g"), ("IT", "b"), ("FR", "k"), ("DE", "y"), ("CN", "c"), ("ES", "m") )
    countries = ( ("CA", "r"), ("US", "g"), ("IT", "b"), ("FR", "k"), ("DE", "y"), ("ES", "m") )
    plot(countries, report_death)




    
