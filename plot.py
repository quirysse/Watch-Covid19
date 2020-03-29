import plotly.express as px
import plotly.graph_objects as go
from setup_countries import GetCountry
from scipy.signal import savgol_filter
import numpy as np

def BaseRate(x):
    return np.asarray( x[1:]/x[:len(x)-1] )

def Derive(x):
    return np.asarray( x[1:]-x[:len(x)-1] )

def DaysToMultiplyBy(x, alpha):
    y = BaseRate(x)
    return np.log(alpha) / np.log(y)


def GetLegendCummul(speed=False):
    if speed:
        return dict(
            title = '''Nouveaux cas officiels par jour''',
            xaxis_title = '''Nombre de jours''',
            yaxis_title = '''Nombre de cas par jour'''
        )
        
    else:
        return dict(
            title = '''Nombre de cas officiels cummulés''',
            xaxis_title = '''Nombre de jours''',
            yaxis_title = '''Nombre de cas'''
        )

def GetLegendDeath(speed=False):
    if speed:
        return dict(
            title = '''Nouveaux morts par jour''',
            xaxis_title = '''Nombre de jours''',
            yaxis_title = '''Nombre de morts par jour'''
        )
        
    else:
        return dict(
            title = '''Nombre de morts cummulés''',
            xaxis_title = '''Nombre de jours''',
            yaxis_title = '''Nombre de morts'''
        )

def GetFont():
    return dict(
            family="Courier New, monospace",
            size=18,
            color="#7f7f7f"
        )

def GetLegend():
    return GetLegendCummul(True)
    #return GetLegendDeath()

def plot(report, threshold=50, outputfile=None):
    
    filter_windowsize = 7
    fig = go.Figure()
    for key, val in report.items():
        isocode = key
        time_series = val["timeseries"]
        country_info = val["info"]

        country_name = country_info["name"] if country_info is not None else ""
        time_series[time_series < threshold ] = 0
        time_series = np.trim_zeros(time_series, 'f') #/ country_info["population"] * 1000000
        
        signal = time_series#savgol_filter(time_series, 5, 3)

        if len(time_series) > filter_windowsize :
            signal = savgol_filter(time_series, filter_windowsize, 3)

        signal = Derive(signal)

        fig.add_trace(go.Scatter(
            y=signal,
            mode='lines',
            name=isocode,
            hovertemplate =
            '<b>Cas</b>: %{y:.0f}'+
            '<br><b>Jour</b>: %{x}<br>'+
            '<b>' + country_name + '</b>'
        ))

    leg = GetLegend()
    fig.update_layout(
        title=leg['title'],
        xaxis_title=leg['xaxis_title'],
        yaxis_title=leg['yaxis_title'],
        font=GetFont()
    )

    if outputfile is not None:    
        fig.write_html(outputfile, auto_open=False)
    else :
        fig.show()  