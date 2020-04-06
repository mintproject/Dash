from viz.utils import *
from viz.load_data import *
from viz.make_plots import *

# MAP INFORMATION BY COUNTY
# Load county Data for mapping
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties_geojson = json.load(response)
# # state_fips_codes = [22,48]
txla_counties = {'type': 'FeatureCollection', 'features': []}
for county in counties_geojson['features']:
    if county['properties']['STATE'] in ['22','48']:
        txla_counties['features'].append(county)
tx_counties = {'type': 'FeatureCollection', 'features': []}
for county in counties_geojson['features']:
    if county['properties']['STATE'] in ['48']:
        tx_counties['features'].append(county)


# READ IN NYT DATA AND PROCESS
# Get NY Times by County Data
nyt_data = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'
nyt = pd.read_csv(nyt_data, dtype={'fips': object},parse_dates=['date'])
# Process date information
nyt['dayofyear'] = nyt['date'].dt.dayofyear
nyt['Date'] = nyt['date'].dt.strftime("%m/%d")
# County data = data with fips values for county data [** TODO: figure outgeojson for NYC and KC**]
nyt_state = nyt[nyt['fips'].notnull()]
# Start data March 3
nyt_state = nyt_state[nyt_state['dayofyear']>62]

# LOAD US POPULATION DATA
# ** REPLACE WITH HOUSEHOLD DATA WHEN AVAILABLE**
# US Population downloaded from US Census
USpopfile = 'https://raw.githubusercontent.com/mepearson/tacc_dash/master/data/US_population.csv'
uspop = pd.read_csv(USpopfile)
# Convert population to numeric
uspop['POP'] = uspop['POP'].str.replace(',','')
uspop['POP'] = pd.to_numeric(uspop['POP'])
# Split County, State column into separate columns
uspop[['County','State']] = uspop['CTY STATE'].str.split(', ',expand=True)
# Remove leading '.' from County name
uspop['County']  = uspop['County'] .str[1:]
# Remove ' County' from county name
uspop['County'] = uspop['County'].str.replace(' County','')
# Handle Louisiana where counties are called parishes
uspop['County'] = uspop['County'].str.replace(' Parish','')
# Handle Anchorage (added 'Municipality' in US Pop data)
uspop['County'] = uspop['County'].replace('Anchorage Municipality', 'Anchorage')
# Handle lower case 'James city' from NYT data
uspop['County'] = uspop['County'].replace('James City', 'James city')

# MERGE COVID AND DEMOGRAPHIC DATA, DROP COLUMNS, CALC PER CAPITA
# Merge COVID and POPULATION data by County
county_data = pd.merge(nyt_state, uspop, left_on=['county','state'], right_on=['County','State'], how='left')
# Check for merge fails
county_data[county_data['POP'].isnull()]['fips'].unique()
# Drop unnecessary columns
county_data = county_data.drop(['CTY STATE', 'County', 'State'], axis=1)
# Rename Columns to more user friendly versions
county_data = county_data.rename(columns={"county": "County", "state": "State","POP":"Population","cases":"Cases","deaths":"Deaths"})
# Generate dataframe for page and Calculate per capita values
cols_to_select = ['dayofyear','fips','date','Date','State','County','Population','Cases', 'Deaths']
county_data = county_data[cols_to_select]
county_data['Cases per 1000'] = county_data['Cases']*1000/county_data['Population']
county_data['Deaths per 1000'] = county_data['Deaths']*1000/county_data['Population']

#TX AND LA SPECIFIC DATA
#Get TX and LA data
tx_la_data = county_data[county_data['State'].isin(['Texas','Louisiana'])]
tx_data = tx_la_data[tx_la_data['State'] == 'Texas']
dates_dict = pd.Series(tx_la_data.Date.values,index=tx_la_data.dayofyear).to_dict()
# 3 Limit labels to every 3 days
for i in dates_dict:
    if (i + 1) % 3 != 0:
        dates_dict[i] = ''
date_min = tx_la_data.dayofyear.min()
date_max = tx_la_data.dayofyear.max()
# most recent day data
txla_latest = tx_la_data[tx_la_data['dayofyear'] == date_max]
tx_latest = tx_data[tx_data['dayofyear'] == date_max]

# Get options lists from data sources
# **TODOL: -move data code to separate file and add dropdown to select dataset**
cases_index = county_data.columns.get_loc('Cases')
metrics = county_data.columns[cases_index:]

#GRAPHING FUNCTIONS
# Function to return choropleth_mapbox
# def create_choropleth(df, geojson, locations, color,
#                         hover_name = None, hover_data = None, animation_frame = None, opacity = None ,
#                         color_continuous_scale=None, mapbox_style="carto-positron"):
#     fig = px.choropleth_mapbox(df, geojson=geojson, locations=locations, color=color,
#                                 hover_name=hover_name,
#                                 hover_data = hover_data,
#                                 animation_frame = animation_frame,
#                                 color_continuous_scale = color_continuous_scale,
#                                 mapbox_style = mapbox_style,
#                                 opacity = opacity,
#                                 zoom=4, center = {"lat": 31.9686, "lon": -98.5018},
#                               )
#     fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
#     fig.update_layout(clickmode = 'event+select')
#     return fig
initial_fig = create_choropleth(tx_latest,tx_counties,'fips','Cases',hover_name='County',hover_data=metrics)

# PAGE LAYOUT
def generate_layout(thread_id=None):
    return html.Div([
        html.Div([
            html.H3(['Covid19 Spread: Texas'],className='nine columns'),
            html.Div([
                dcc.RadioItems(
                    id='covid_animate_location_radio',
                    options=[
                        {'label': 'Texas Only', 'value': 'TX'},
                        {'label': 'Texas and Louisiana', 'value': 'TXLA'},
                    ],
                    value='TX',
                    labelStyle={'display': 'inline-block'}
            )],className='three columns')
        ],className='row'),
        # html.Div([
        #     html.Div([
        html.Div([
            html.Div([
                html.P(['Show values for:']),
                dcc.Dropdown(id='covid_animate_map_dd_metric',
                    options=[dict(label=x, value=x) for x in metrics],
                    value=metrics[0],
                    # style={'width':'200px','margin':'0px 30px 0px 5px'}
                    ),
            ],className='two columns'),
            html.Div([
                html.P(['Exclude Observations of ']),
                html.Div([
                    dcc.Dropdown(id='covid_animate_map_dd_threshold_metric',
                        options=[dict(label=x, value=x) for x in metrics],
                        value=metrics[0],
                        # style={'width':'200px','margin':'0px 5px'}
                        className= 'six columns'
                        ),
                    html.Span([' below '],className='two columns'),
                    dcc.Input(id='covid_animate_map_input_threshold',
                        type='number',
                        placeholder='value',
                        className= 'four columns'
                        ),
                ]),
            ],className='four columns'),
            html.Div([
                html.P(['Color Scale:']),
                dcc.RadioItems(id='covid_animate_scale',
                            options=[
                                {'label': 'Changes daily', 'value': 'daily'},
                                {'label': 'Fixed to range', 'value': 'range'},
                                #{'label': 'Custom', 'value': 'userchoice'}
                            ],
                            value='daily',
                            labelStyle={'display': 'inline-block'}
                    ),
                html.Div([

                ])
            ],className='four columns'),
        ],className='row'),
        html.Div([
            html.Span(['Dates:'], className='one column'),
            html.Div([
            dcc.RangeSlider(
                id='animate_date_slider',
                min=date_min,
                max=date_max,
                step=None,
                value=[date_min,date_max],
                marks={i: dates_dict[i] for i in dates_dict})
            ],className='seven columns'),
            html.Div([
                dcc.RadioItems(id='covid_animate_select',
                            options=[
                                {'label': 'End date only ', 'value': 'daily'},
                                {'label': 'Animate over Range', 'value': 'animate'},
                                # {'label': 'Custom', 'value': 'userchoice'}
                            ],
                            value='daily',
                            labelStyle={'display': 'inline-block'}
                    ),
            ],className='four columns'),
        ], className='row', style={'margin-top':'15px'}),
        #     ],className='eight columns'),
        #
        # ],className='row'),
        html.Div([
            dcc.Loading([
                dcc.Graph(
                    id='covid_animate_map',
                    figure = initial_fig
                    )
            ]),
        ],className='row'),
        html.Div(id='animatetester')
    ],id='covid_animate_main')

# CALLBACK FOR PAGE BEHAVIOR
@app.callback(
    #Output('mtest','children'), tx_date_slider
    [Output('covid_animate_map','figure'),Output('animatetester','children')],
    [Input('covid_animate_map_dd_metric', 'value'),Input('covid_animate_map_input_threshold', 'value'),Input('covid_animate_map_dd_threshold_metric', 'value'),
    Input('animate_date_slider', 'value'),Input('covid_animate_location_radio','value'), Input('covid_animate_select','value'),
    Input('covid_animate_scale','value')
    ])
def update_map(metric, threshold, threshold_metric, mapdate,location,animate, scale):
    # Set changeable to None to start
    range_color = None
    animation_frame = None

    # set data and geojson depending on location selected
    if location == 'TX':
        mapdata = tx_data
        geojson = tx_counties
    if location == 'TXLA':
        mapdata = tx_la_data
        geojson = txla_counties
        
    # Set data depending on parameters
    if threshold is not None:
        mapdata = mapdata[mapdata[threshold_metric]>=threshold]

    if animate == 'daily':
        mapdata = mapdata[mapdata['dayofyear']==mapdate[1]]

    if animate == 'animate':
        mapdata = mapdata[(mapdata['dayofyear']>=mapdate[0]) & (mapdata['dayofyear']<=mapdate[1])]
        if scale == 'range':
            range_color = [mapdata[metric].min(),mapdata[metric].max()]
        animation_frame = 'Date'

    map_fig = create_choropleth(mapdata,geojson,'fips',metric, hover_name='County',hover_data = metrics, animation_frame = animation_frame, range_color = range_color)

    # test kids section if testing needed
    testkids = []

    return map_fig, testkids
