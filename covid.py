 #Load the Pandas libraries with alias 'pd' 
from dbutils import create_connection, create_table
from setup_countries import InitCountryData
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

    countries = ( ("CA", "r"), ("US", "g"), ("IT", "b"), ("FR", "k"), ("DE", "y") )
    for c in countries:
        # print(c[0], report[ c[0] ] )
        print(c[0], np.diff(report[ c[0] ]) )
        #plt.plot( report[ c[0] ])
        plt.plot( report[ c[0] ], c[1] )
        #plt.plot( np.diff(report[ c[0] ]), c[1] )

    plt.show()



    
