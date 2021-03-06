import pandas as pd
import json
import copy

import plotly.graph_objects as go


import dash
import dash_core_components as dcc
import dash_html_components as html

query = 'South Africa'

positives = pd.read_json('../data/covid-19/cases.json').iloc[20:]
deaths = pd.read_json('../data/covid-19/deaths.json').iloc[20:]
recovered = pd.read_json('../data/covid-19/recovered.json').iloc[20:]

with open('../data/mapping/ne_50m_admin_0_countries.json') as src:
	mapdata = json.loads(src.read())

app = dash.Dash(__name__)

app.layout = html.Div([
	html.Div([
		html.H3(children='Covid-19 case dashboard'),

#		dcc.Graph(id='map-plot', figure={}),
		dcc.Location(id='location', refresh=True),
	    
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
		    	options=[{'label':i, 'value':i} for i in positives.columns],
		    	value=query,
		    	placeholder="Select a country",
		    	style={"width":300}),
		    html.H5(' compared with '),
		    dcc.Dropdown(
		    	id='country-compare',
		    	options=[{'label':i, 'value':i} for i in positives.columns],
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
		{'type':'bar', 'marker':{'color':'rgb(128,128,128)','alpha':0.7}, 'name':'positives'},
		{'type':'bar', 'marker':{'color':'rgb(64,64,64)'}, 'name':'deaths'},
		{'type':'bar', 'marker':{'color':'rgb(64,256,64)'}, 'name':'recovered'}
	],
	'layout':{
		'barmode':'relative',
		'yaxis':{'type':'log'}
	}
}


@app.callback(
	dash.dependencies.Output('timeseries-plot', 'figure'),
	[dash.dependencies.Input('location', 'hash'),
	 dash.dependencies.Input('country-select', 'value'),
	 dash.dependencies.Input('country-compare', 'value'),
	 dash.dependencies.Input('log-scale', 'value'),
	 dash.dependencies.Input('delta', 'value')])
def update_timeseries_plot(hash_select, select, compare, scale, delta):

	plot = copy.deepcopy(timeseries_plot)

	if hash_select:
		select = hash_select[1:]
		

	if delta == 'cumulative':

		plot['data'][2]['x'] = recovered[select].index
		plot['data'][2]['y'] = -recovered[select]

		plot['data'][0]['x'] = positives[select].index
		plot['data'][0]['y'] = positives[select] - recovered[select] - deaths[select]

		plot['data'][1]['x'] = deaths[select].index
		plot['data'][1]['y'] = -deaths[select]


	else:
		plot['data'][2]['x'] = recovered[select].index[1:]
		plot['data'][2]['y'] = -recovered[select].diff()

		plot['data'][0]['x'] = positives[select].index[1:]
		plot['data'][0]['y'] = positives[select].diff()

		plot['data'][1]['x'] = deaths[select].index[1:]
		plot['data'][1]['y'] = -deaths[select].diff()



	if scale != 'log':
		plot['layout']['yaxis']['type'] = 'linear'

	if len(compare):
		for country in compare:
			plot['data'].append(
				{'x':positives[country].index, 'y':positives[country] - recovered[country] - deaths[country], 
					'type':'line', 'marker':{'color':'rgb(256,128,128)', 'line-width':40}, 'name':country}
				)

	plot['layout']['title'] = select

	return plot


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True)
