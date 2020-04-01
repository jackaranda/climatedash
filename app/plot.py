import pandas as pd

import plotly.graph_objects as go


import dash
import dash_core_components as dcc
import dash_html_components as html

query = 'South Africa'

cases = pd.read_json('../data/covid-19/cases.json')
deaths = pd.read_json('../data/covid-19/deaths.json')
recovered = pd.read_json('../data/covid-19/recovered.json')

#fig = go.Figure(data=go.Bar(name='cases', x=cases.index, y=cases[query]))

app = dash.Dash(__name__)

app.layout = html.Div([
	html.Div([
		html.H3(children='Covid-19 case dashboard'),
	    dcc.Graph(id='timeseries-plot', figure={}),
   	    dcc.RadioItems(
	    	id='log-scale',
	    	options=[{'label':'linear','value':'linear'},{'label':'logarithmic','value':'log'}],
	    	value='linear',
	    	style={'width':300}),
	    html.Div([
		    dcc.Dropdown(
		    	id='country-select',
		    	options=[{'label':i, 'value':i} for i in cases.columns],
		    	value=query,
		    	placeholder="Select a country",
		    	style={"width":300}),
		    html.H5(' compared with '),
		    dcc.Dropdown(
		    	id='country-compare',
		    	options=[{'label':i, 'value':i} for i in cases.columns],
		    	placeholder="Select countries to compare",
		    	multi=True,
		    	value=[query],
		    	style={"width":300})
		   	],
		   	className='row')
	],
	className='container')
])

@app.callback(
	dash.dependencies.Output('timeseries-plot', 'figure'),
	[dash.dependencies.Input('country-select', 'value'),
	 dash.dependencies.Input('country-compare', 'value'),
	 dash.dependencies.Input('log-scale', 'value')])
def update_timeseries_plot(select, compare, scale):

	result = {
		'data':[
			{'x':cases[select].index, 'y':cases[select], 
				'type':'bar', 'marker':{'color':'rgb(128,128,128)','alpha':0.7}, 'name':'cases'},
			{'x':deaths[select].index, 'y':deaths[select], 
				'type':'bar', 'marker':{'color':'rgb(64,64,64)'}, 'name':'deaths'},
			{'x':recovered[select].index, 'y':recovered[select], 
				'type':'bar', 'marker':{'color':'rgb(64,256,64)'}, 'name':'recovered'}
		],
		'layout':{
			'barmode':'stack',
			'yaxis':{'type':'log'}
		}
	}

	if scale != 'log':
		result['layout']['yaxis']['type'] = 'linear'

	if len(compare):
		for country in compare:
			result['data'].append(
				{'x':cases[country].index, 'y':cases[country], 
					'type':'line', 'marker':{'color':'rgb(256,128,128)', 'line-width':40}, 'name':country}
				)

	return result

if __name__ == '__main__':
    app.run_server(debug=True)
