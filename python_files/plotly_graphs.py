import plotly.graph_objects as go
import plotly
import yfinance_api as yf
import rnn_lstm as rnn
import json
from threading import Thread
import datetime 
def graph_prediction_json(symbol,start="",end=""):
    df_prediction=rnn.getPrediction(symbol,start,end)
    df_prediction= df_prediction.truncate(before = df_prediction.index[-80])

    # df_prediction_thread = Thread(target=rnn.getPrediction,args=(symbol,start,end))
    # df_prediction_thread.start()
    # df_prediction=df_prediction_thread.join()
    fig = go.Figure([go.Scatter(x=df_prediction.index, y=df_prediction['Real'],name="Real")])
    fig.add_scatter(x=df_prediction.index, y=df_prediction['Prediccion'],name="Prediccion", mode='lines')
    fig.update_layout(xaxis_rangeslider_visible=False,title=yf.getInfo(symbol)["longName"],yaxis_title="Precio $")
    fig.update_layout(height=500)
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return plot_json


def graph_history_json(symbol,start="",end=""):
    df_history = yf.getHistory(symbol,start,end)
    df_history= df_history.truncate(before = df_history.index[-1044])

    #layout = go.Layout(xaxis=dict(range=[(datetime.date.today()-datetime.timedelta(days=60)).strftime('%Y-%m-%d'),datetime.date.today().strftime('%Y-%m-%d')]))
    fig = go.Figure([go.Scatter(x=df_history.index, y=df_history["Close"])])#layout=layout
    fig.update_layout(xaxis_rangeslider_visible=True,title=yf.getInfo(symbol)["longName"],yaxis_title="Precio $")
    fig.update_layout(height=500)

    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return plot_json