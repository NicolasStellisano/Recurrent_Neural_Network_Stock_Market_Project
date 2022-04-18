import plotly.graph_objects as go
import plotly
import yfinance_api as yf
import rnn_lstm as rnn
import json
from threading import Thread
import datetime 
import sqlite3
def graph_prediction_json(symbol,start="",end=""):
    df_prediction=db_get_prediction(symbol)
    if df_prediction is None:
        df_prediction=rnn.getPrediction(symbol,start,end)
    else:
        return df_prediction

    title=yf.getInfo(symbol)
    layout = go.Layout(xaxis=dict(range=[(datetime.date.today()-datetime.timedelta(days=800)).strftime('%Y-%m-%d'),(datetime.date.today()+datetime.timedelta(days=5)).strftime('%Y-%m-%d')]))
    fig = go.Figure([go.Scatter(x=df_prediction.index, y=df_prediction['Real'],name="Real",line=dict(color="#00FF00") )],layout=layout)
    fig.add_scatter(x=df_prediction.index, y=df_prediction['Prediccion'],name="Prediccion", mode='lines')
    fig.update_layout(xaxis_rangeslider_visible=False,title=title["longName"],yaxis_title="Precio $")
    fig.update_layout(height=750,dragmode="pan",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="white",title_font_size=20)
    fig.update_layout(title=dict(font=dict(size=26)))

    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    thread=Thread(target=db_insert_prediction,args=(symbol,plot_json))
    thread.start()
    return plot_json


def graph_history_json(symbol,start="",end=""):
    df_history = yf.getHistory(symbol,start,end)
    #df_history= df_history.truncate(before = df_history.index[-1044])
    print(symbol)

    title=yf.getInfo(symbol)
    layout = go.Layout(xaxis=dict(range=[(datetime.date.today()-datetime.timedelta(days=1044)).strftime("%Y-%m-%d"),(datetime.date.today()+datetime.timedelta(days=5)).strftime("%Y-%m-%d")]))
    fig = go.Figure([go.Scatter(x=df_history.index, y=df_history["Close"], line=dict(color="#00FF00"))],layout=layout)#layout=layout
    fig.update_layout(height=750,dragmode="pan",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="white",title_font_size=20)
    fig.update_layout(xaxis_rangeslider_visible=False,title=title["longName"],yaxis_title="Precio $")
    fig.update_layout(title=dict(font=dict(size=26)))

    
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return plot_json

def db_insert_prediction(symbol:str,json:str):
    try: 
         with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            cur.execute('CREATE TABLE IF NOT EXISTS predictions (symbol TEXT, date TEXT, json TEXT)')
            con.commit()
            cur.execute("INSERT INTO predictions (symbol,date,json) VALUES (?,?,?)",(symbol,datetime.date.today().strftime('%Y-%m-%d'),json))    
            con.commit()
            print("Record successfully added")
    except Exception as e:
         con.rollback()
         print("ERROR INSERT " +str(e))

def db_get_prediction(symbol:str):
    try: 
        with sqlite3.connect("database.db") as con:
            print("Entro select cur")
            cur = con.cursor()
            query = "SELECT json FROM predictions WHERE symbol='"+symbol+"' and date='"+datetime.date.today().strftime('%Y-%m-%d')+"'"
            print(query)
            cur.execute(query)
            con.commit()
            row = cur.fetchone(); 
            print(row[0])
            if row is not None:
                return row[0]

    except Exception as e:
         return None