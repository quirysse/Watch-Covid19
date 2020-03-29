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
            title = '''Nouveaux cas officiels <BR>par jour''',
            xaxis_title = '''Nombre de jours''',
            yaxis_title = '''Nombre de cas par jour'''
        )
        
    else:
        return dict(
            title = '''Nombre de cas officiels <BR>cummulés''',
            xaxis_title = '''Nombre de jours''',
            yaxis_title = '''Nombre de cas'''
        )

def GetLegendDeath(speed=False):
    if speed:
        return dict(
            title = '''Nouveaux morts <BR> par jour''',
            xaxis_title = '''Nombre de jours''',
            yaxis_title = '''Nombre de morts par jour'''
        )
        
    else:
        return dict(
            title = '''Nombre de morts <BR>cummulés''',
            xaxis_title = '''Nombre de jours''',
            yaxis_title = '''Nombre de morts'''
        )

def GetFont():
    return dict(
            family="Courier New, monospace",
            size=14,
            color="#7f7f7f"
        )

def GetLegend(rateInsteadOfSum):
    return GetLegendCummul(rateInsteadOfSum)
    #return GetLegendDeath()

def plot(report, threshold=50, derivecount = 0, bypopulation=False, outputfile=None, windowsize=5, rightbound=0):
    
    filter_windowsize = windowsize
    filter_polynomial_order = 3 if filter_windowsize > 3 else 1

    fig = go.Figure()
    for key, val in report.items():
        isocode = key
        time_series = val["timeseries"]
        country_info = val["info"]

        if country_info is not None:
            country_name = country_info["name"]  
            country_popul_str = '{:.1f} M'.format(country_info["population"]/1e6)  
        else :
            country_name = isocode  
            country_popul_str = "N/A"  
            
        time_series[time_series < threshold ] = 0
        
        time_series[time_series < threshold ] = 0
        time_series = np.trim_zeros(time_series, 'f')

        if rightbound > 0 and len(time_series) > rightbound:
            time_series[rightbound:] = 0
        
        time_series = np.trim_zeros(time_series, 'b')

        if bypopulation :
            if country_info is None:
                continue #Case of state of province without known population in dataabse
            else:
                time_series = time_series / country_info["population"] * 1000000

        signal = time_series

        if len(time_series) > filter_windowsize and filter_windowsize > 1:
            signal = savgol_filter(time_series, filter_windowsize, filter_polynomial_order)

        for i in range(derivecount):
            signal = Derive(signal)

        case_hover_string = '<b>Cas</b>: %{y:.0f}' if not bypopulation else '<b>Cas/1M hab</b>: %{y:.0f}' 
        fig.add_trace(go.Scatter(
            y=signal,
            mode='lines',
            name=isocode,
            hovertemplate =
            '<b>' + country_name + '</b><BR>' +
            '<b>Population: ' + country_popul_str + '</b><BR>' +
            case_hover_string + '<BR>' +
            '<b>Jour</b>: %{x}<br>'
        ))

    leg = GetLegend(derivecount > 0)
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