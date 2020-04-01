import pandas as pd
import json
import copy

import plotly.graph_objects as go


import dash
import dash_core_components as dcc
import dash_html_components as html

query = 'South Africa'

cases = pd.read_json('../data/covid-19/cases.json')
deaths = pd.read_json('../data/covid-19/deaths.json')
recovered = pd.read_json('../data/covid-19/recovered.json')

with open('../data/mapping/ne_50m_admin_0_countries.json') as src:
	mapdata = json.loads(src.read())

app = dash.Dash(__name__)

app.layout = html.Div([
	html.Div([
		html.H3(children='Covid-19 case dashboard'),

#		dcc.Graph(id='map-plot', figure={}),

	    dcc.Graph(id='timeseries-plot', figure={}),
   	    
   	    dcc.RadioItems(
	    	id='log-scale',
	    	options=[{'label':'linear','value':'linear'},{'label':'logarithmic','value':'log'}],
	    	value='linear',
	    	style={'width':300}),
	    
   	    dcc.RadioItems(
	    	id='delta',
	    	options=[{'label':'cumulative','value':'cumulative'},{'label':'delta','value':'delta'}],
	    	value='cumulative',
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


timeseries_plot = {
	'data':[
		{'type':'bar', 'marker':{'color':'rgb(128,128,128)','alpha':0.7}, 'name':'cases'},
		{'type':'bar', 'marker':{'color':'rgb(64,64,64)'}, 'name':'deaths'},
		{'type':'bar', 'marker':{'color':'rgb(64,256,64)'}, 'name':'recovered'}
	],
	'layout':{
		'barmode':'stack',
		'yaxis':{'type':'log'}
	}
}


@app.callback(
	dash.dependencies.Output('timeseries-plot', 'figure'),
	[dash.dependencies.Input('country-select', 'value'),
	 dash.dependencies.Input('country-compare', 'value'),
	 dash.dependencies.Input('log-scale', 'value'),
	 dash.dependencies.Input('delta', 'value')])
def update_timeseries_plot(select, compare, scale, delta):

	plot = copy.deepcopy(timeseries_plot)

	if delta == 'cumulative':
		plot['data'][0]['x'] = cases[select].index
		plot['data'][0]['y'] = cases[select]

		plot['data'][1]['x'] = deaths[select].index
		plot['data'][1]['y'] = deaths[select]

		plot['data'][2]['x'] = recovered[select].index
		plot['data'][2]['y'] = recovered[select]

	else:
		plot['data'][0]['x'] = cases[select].index[1:]
		plot['data'][0]['y'] = cases[select].diff()

		plot['data'][1]['x'] = deaths[select].index[1:]
		plot['data'][1]['y'] = deaths[select].diff()

		plot['data'][2]['x'] = recovered[select].index[1:]
		plot['data'][2]['y'] = recovered[select].diff()


	if scale != 'log':
		plot['layout']['yaxis']['type'] = 'linear'

	if len(compare):
		for country in compare:
			plot['data'].append(
				{'x':cases[country].index, 'y':cases[country], 
					'type':'line', 'marker':{'color':'rgb(256,128,128)', 'line-width':40}, 'name':country}
				)

	return plot


if __name__ == '__main__':
    app.run_server(debug=True)
