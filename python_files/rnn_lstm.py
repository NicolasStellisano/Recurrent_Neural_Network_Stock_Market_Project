import numpy as np
import pandas as pd
import yfinance as yf
import tensorflow as tf
from tensorflow.keras.layers import Dense, LSTM
from tensorflow.keras.models import Sequential
from sklearn.preprocessing import MinMaxScaler
import yfinance_api as yf

def getPrediction(symbol:str,start="",end=""):
    print("Entro Prediction")
    pd.options.mode.chained_assignment = None
    tf.random.set_seed(0)
    df = yf.getHistory(symbol,start,end)

    # download the data
    y = df['Close'].fillna(method='ffill')
    y = y.values.reshape(-1, 1)

    # scale the data
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaler = scaler.fit(y)
    y = scaler.transform(y)

    # generate the input and output sequences
    n_lookback = 60  # length of input sequences (lookback period)
    n_forecast = 30  # length of output sequences (forecast period)

    X = []
    Y = []

    for i in range(n_lookback, len(y) - n_forecast + 1):
        X.append(y[i - n_lookback: i])
        Y.append(y[i: i + n_forecast])

    X = np.array(X)
    Y = np.array(Y)

    # fit the model
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(n_lookback, 1)))
    model.add(LSTM(units=50))
    model.add(Dense(n_forecast))

    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(X, Y, epochs=100, batch_size=32, verbose=0)

    # generate the forecasts
    X_ = y[- n_lookback:]  # last available input sequence
    X_ = X_.reshape(1, n_lookback, 1)

    Y_ = model.predict(X_).reshape(-1, 1)
    Y_ = scaler.inverse_transform(Y_)

    # organize the results in a data frame
    df_past = df[['Close']].reset_index()
    df_past.rename(columns={'index': 'Date', 'Close': 'Real'}, inplace=True)
    df_past['Date'] = pd.to_datetime(df_past['Date'])
    df_past['Prediccion'] = np.nan
    df_past['Total'] =df_past['Real']
    df_past['Prediccion'].iloc[-1] = df_past['Real'].iloc[-1]

    df_future = pd.DataFrame(columns=['Date', 'Real', 'Prediccion'])
    df_future['Date'] = pd.date_range(start=df_past['Date'].iloc[-1] + pd.Timedelta(days=1), periods=n_forecast)
    df_future['Prediccion'] = Y_.flatten()
    df_future['Real'] = np.nan
    df_future['Total']=Y_.flatten()

    total_results = df_past.append(df_future).set_index('Date')
    return total_results

