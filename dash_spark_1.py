import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import json
import plotly.graph_objs as go
import plotly.plotly as py
import numpy as np
import random

from random import shuffle
from datetime import date, datetime
from dash.dependencies import Input, Output
import plotly.tools as tls



def time_conv(nanos):
    '''
    time_conv converts a unix style timestamp in nanoseconds
    to an ISO style timestamp in the format YYYY-MM-DDTHH:MM:SS
 
    Input
    nanos as a long
 
    Returns
    ISO timestamp as str
    '''
    d = datetime.fromtimestamp(nanos/1000)
    ds = d.isoformat().split('.')
    return ds[0]

with open('ex_data_JSON.txt', mode='r') as inp:

    i = json.load(inp)

df = pd.DataFrame(i['builds'])
res_lst = [random.randint(0,1) for _ in range(100)]
r2 = [x if x == 1 else -1 for x in res_lst]
df['timestamp'] = df['timestamp'].apply(time_conv)
df['results'] = r2
df.loc[df['results'] == 1, 'result'] = 'SUCCESS'
df

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
    }

app.layout = html.Div([
    html.H1(
        children='Sparklinez',
        style={
            'textAlign': 'center',
            'color': colors['text']
            }
        ),

    #html.H2("Show me the last..."),\
    
    dcc.Graph(id='spark-bar-plot'),
    dcc.Slider(
        id= 'spark-slider', 
        min=10,
        max=21,
        marks={str(num): str(num) for num in range(10,21)} 
        )
    ])

@app.callback(
    Output('spark-bar-plot', 'figure'),
    [Input('spark-slider', 'value')])



def top_num_results(spark_slider):
    df = pd.DataFrame(i['builds'])
    res_lst = [random.randint(0,1) for _ in range(100)]
    r2 = [x if x == 1 else -1 for x in res_lst]
    df['timestamp'] = df['timestamp'].apply(time_conv)
    df['scores'] = r2
    df.loc[df['scores'] == 1, 'result'] = 'SUCCESS'
    results_df = df[['number', 'scores', 'result']]
    top_res = results_df[:spark_slider]
    not_top = results_df[spark_slider:]
    
    fig = tls.make_subplots(rows=2, cols=1, shared_xaxes=True,vertical_spacing=0.009,horizontal_spacing=0.009)
    fig['layout']['margin'] = {'l': 30, 'r': 10, 'b': 50, 't': 25}

    fig.append_trace({'x':top_res['number'],'y':top_res['scores'],'type':'bar','text':top_res['result'], 'hoverinfo': 'x,text', 'name':'Latest'},1,1)
    fig.append_trace({'x':results_df['number'],'y':results_df['scores'],'type':'bar','text':results_df['result'], 'hoverinfo': 'x,text','name':'Full'},2,1)
    fig['layout'].update(title='1 Minute plot of '+ "spark-slider")  

    return fig

    
    """return {
        'data': [go.Bar(
            x = top_res['number'],
            y = top_res['scores'], 
            text = top_res['result'],
            hoverinfo = 'x,text'
            )]
    }"""
    
    
if __name__ == '__main__':
    app.run_server(debug=True)
