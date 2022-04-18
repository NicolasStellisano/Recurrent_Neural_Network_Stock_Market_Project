from flask import Flask, render_template
import sys
sys.path.insert(1, '../python_files')
import plotly_graphs as plotly

app = Flask(__name__)

@app.route('/index/<symbol>')
def history(symbol:str):
    plot_json=plotly.graph_history_json(symbol,"2014-01-01")
    return render_template('index.html',plot_json=plot_json,prediction="False",symbol=symbol)

@app.route('/index')
def index(symbol="ALUA.BA"):
    plot_json=plotly.graph_history_json(symbol,"2014-01-01")
    return render_template('index.html',plot_json=plot_json,prediction="False",symbol=symbol)

@app.route('/prediction/<symbol>')
def prediction(symbol:str):
    plot_json=plotly.graph_prediction_json(symbol,"2014-01-01")
    return render_template('index.html',plot_json=plot_json,prediction="True",symbol=symbol)

if __name__=='__main__':
    app.run(debug=True)