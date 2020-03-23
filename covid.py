 #Load the Pandas libraries with alias 'pd' 
from dbutils import create_connection, create_table
from setup_countries import InitCountryData, GetCountry
from setup_reports import  GetReports
import numpy as np
import matplotlib.pyplot as plt


DBFILE = "database.db"

def setup_database(conn):
    InitCountryData(conn)
    conn.commit()

if __name__ == "__main__":
    conn = create_connection(DBFILE)
    setup_database(conn)
    report = GetReports(conn)

    countries = ( ("CA", "r"), ("US", "g"), ("IT", "b"), ("FR", "k"), ("DE", "y"), ("CN", "c") )
    for c in countries:
        country = GetCountry(conn, c[0])
        print(country["name"], country["population"])
        time_series = report[ c[0] ] / country["population"]
        # print(c[0], report[ c[0] ] )
        #print(c[0], np.diff(report[ c[0] ]) )
        #plt.plot( report[ c[0] ])
        #leg.append(c[0])
        p = plt.plot( time_series, c[1], label=c[0] )
        #graph.append(p)
        #plt.plot( np.diff(report[ c[0] ]), c[1] )

    plt.legend(loc='upper left', borderaxespad=0.)
    #plt.legend(graph, leg)
    plt.show()



    
