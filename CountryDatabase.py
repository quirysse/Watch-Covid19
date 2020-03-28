
from dbutils import create_connection
from setup_countries import InitCountryData, GetCountry
from setup_reports import  Reports

DBFILE = "database.db"

def setup_database(conn, force_update=False):
    InitCountryData(conn, force_update)
    if force_update :
        conn.commit()  


class CountryDatabase :
    
    def __init__(self, force_update=False):
        self.conn = conn = create_connection(DBFILE)
        setup_database(conn, force_update)
        self.report = Reports(conn)
        self.current = self.report.Confirmed

    def GetFromList(self, isocodelist):
        return self.__getReportFromList(isocodelist)

    def Head(self, n=10):
        return self.__head(self.current, n)

    def GetCountry(self, isocode):
        info = GetCountry(self.conn, isocode)
        timeseries = self.current[isocode]
        return {"info" : info, "timeseries" : timeseries}

    def __head(self, report, n) : 
        ret = {}
        for key, value in sorted(report.items(), key=lambda kv : kv[1][-1], reverse=True):
            ret[key] = self.GetCountry(key)
            n = n-1
            if n == 0:
                return ret

    def __getReportFromList(self, isocodelist):
        ret = {}
        for code in isocodelist:
            ret[code] = self.GetCountry(code)
        
        return ret