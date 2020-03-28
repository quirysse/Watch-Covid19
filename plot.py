import plotly.express as px
import plotly.graph_objects as go
from scipy.signal import savgol_filter
import numpy as np

def BaseRate(x):
    return np.asarray( x[1:]/x[:len(x)-1] )

def Derive(x):
    return np.asarray( x[1:]-x[:len(x)-1] )

def DaysToMultiplyBy(x, alpha):
    y = BaseRate(x)
    return np.log(alpha) / np.log(y)


def GetLegendCummul():
    return dict(
        title = '''Nombre de cas officiels cummulés''',
        xaxis_title = '''Nombre de jours''',
        yaxis_title = '''Nombre de cas'''
    )

def GetFont():
    return dict(
            family="Courier New, monospace",
            size=18,
            color="#7f7f7f"
        )

def GetLegend():
    return GetLegendCummul()

def plot(report, threshold=50, outputfile=None):
    
    filter_windowsize = 7
    fig = go.Figure()
    for country_code,  time_series in report.items():

        time_series[time_series < threshold ] = 0
        time_series = np.trim_zeros(time_series, 'f') #/ country["population"] * 1000000
        
        #print(country["name"], len(time_series), time_series )
        #p = plt.plot( time_series, c[1], label=country_code )

        signal = time_series#savgol_filter(time_series, 5, 3)

        if len(time_series) > filter_windowsize :
            signal = savgol_filter(time_series, filter_windowsize, 3)
#        signal = savgol_filter( DaysToMultiplyBy(time_series, 2.), 9, 3)

        #signal = Derive(signal)

        fig.add_trace(go.Scatter(
            y=signal,
            mode='lines',
            name=country_code
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