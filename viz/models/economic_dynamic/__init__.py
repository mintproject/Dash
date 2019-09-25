import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_table

import pandas as pd
import numpy as np
import plotly.express as px

# Data Management Section: import and massage
econ_data = pd.read_csv('./Data/EconModel/results_summary_bycrop.csv')

# Create dataframe of parameters by run_ID index
run_IDs =(econ_data['run_ID'].unique())
data_parameters = pd.DataFrame({'run_ID':run_IDs,'run_description':''})

# Get parameters for each crop
croplist = econ_data.crop.unique()
for crop in croplist:
    pname = crop + '-p'
    c1name = crop + '-c1'
    c2name = crop + '-c2'
    dcrop = econ_data[econ_data['crop']==crop][['run_ID','p','c1','c2']]
    dcrop['p_description'] = np.where((dcrop['p'] == 0),'','p='+dcrop['p'].astype(str))
    dcrop['c1_description'] = np.where((dcrop['c1'] == 0),'','c1='+dcrop['c1'].astype(str))
    dcrop['c2_description'] = np.where((dcrop['c2'] == 0),'','c2='+dcrop['c2'].astype(str))
    dcrop['run_description']= np.where((dcrop['p'] == 0) & (dcrop['c1'] == 0) & (dcrop['c2'] == 0),'',#(crop + ': base'),
        (crop + '[' + dcrop['p_description'] +'; '+ dcrop['c1_description'] +'; '+ dcrop['c2_description']+']' ))
    dcrop = dcrop[['run_ID','run_description','p','c1','c2']].rename(columns={"p": pname, "c1": c1name, "c2": c2name})
    data_parameters = pd.merge(data_parameters, dcrop,on='run_ID', how='left')
    data_parameters['run_description'] = data_parameters['run_description_x'] +' '+ data_parameters['run_description_y']
    data_parameters = data_parameters.drop(["run_description_x", "run_description_y"], axis=1)

runs_param = [
            ['cassava',[[0],[0],[0]]],
            ['groundnuts',[[0],[0],[0]]],
            ['maize',[[0],[0],[-10,0,10]]],
            ['sesame',[[0],[-10,0,10],[0]]],
            ['sorghum',[[0],[-10,0,10],[-10,0,10]]]
             ]

# Select Runs to view
selected_runs = data_parameters[(data_parameters.iloc[:, 1].isin(runs_param[0][1][0]))&
                                (data_parameters.iloc[:, 2].isin(runs_param[0][1][1]))&
                                (data_parameters.iloc[:, 3].isin(runs_param[0][1][2]))&
                            (data_parameters.iloc[:, 4].isin(runs_param[1][1][0]))&
                                (data_parameters.iloc[:, 5].isin(runs_param[1][1][1]))&
                                (data_parameters.iloc[:, 6].isin(runs_param[1][1][2]))&
                            (data_parameters.iloc[:, 7].isin(runs_param[2][1][0]))&
                                (data_parameters.iloc[:, 8].isin(runs_param[2][1][1]))&
                                (data_parameters.iloc[:, 9].isin(runs_param[2][1][2]))&
                            (data_parameters.iloc[:, 10].isin(runs_param[3][1][0]))&
                                (data_parameters.iloc[:, 11].isin(runs_param[3][1][1]))&
                                (data_parameters.iloc[:, 12].isin(runs_param[3][1][2]))&
                            (data_parameters.iloc[:, 13].isin(runs_param[4][1][0]))&
                                (data_parameters.iloc[:, 14].isin(runs_param[4][1][1]))&
                                (data_parameters.iloc[:, 15].isin(runs_param[4][1][2]))
                            ]
#                             ]['run_ID']
#
# data_graph = econ_data.query('run_ID in @selected_runs')
data_graph = pd.merge(econ_data,selected_runs,on='run_ID',how='right')

#Build graph
col_options = [dict(label=x, value=x) for x in data_graph.columns]
dimensions = ["x", "y", "color", "facet_col", "facet_row"]
dgraph = dimensions + ["dd_hover"]
app = dash.Dash(
    __name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"]
)



#Config elements
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

app.layout = html.Div(
    [
        html.H1("Data Exploration: Scatter Plot"),
        html.Div(
            [
                html.Div([
                html.P([d + ":", dcc.Dropdown(id=d, options=col_options)])
                for d in dimensions
                ]),
                html.P(['On Hover show: ',
                    dcc.Dropdown(
                    id='dd_hover',
                    options=col_options,
                    multi=True
                )])
            ],
            style={"width": "25%", "float": "left"},
        ),
        dcc.Graph(id="graph", style={"width": "75%", "display": "inline-block"}),
    ]
)

@app.callback(Output("graph", "figure"), ([Input(d, "value") for d in dgraph]))
def make_figure(x, y, color, facet_col, facet_row, hover_info):
    fig = px.line(
        data_graph,
        x=x,
        y=y,
        color=color,
        facet_col=facet_col,
        facet_row=facet_row,
        height=700,
        hover_data = hover_info,
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True,port=8080)
