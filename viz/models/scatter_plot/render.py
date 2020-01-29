from viz.utils import *

# styling
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
                        'https://codepen.io/chriddyp/pen/brPBPO.css']

# Layout
def generate_layout(thread_id):
    return html.Div([
        dcc.Store(id='e-cols'),
        dcc.Store(id='e-data'),
        html.Div([
            html.Label('Thread id'),
            dcc.Input(id='thread_id', value=thread_id, type='text', style={"width": "33%"}),
        ]),
        html.H2('Scatter Plot for Modelling Thread Data'),
            html.Div([
                html.Div([
                    html.P(['X Axis: ']),
                    dcc.Dropdown(id='e-dd-x'),
                    html.P(['Y Axis: ']),
                    dcc.Dropdown(id='e-dd-y'),
                    html.P(['Color: ']),
                    dcc.Dropdown(id='e-dd-color'),
                    html.P(['Facet Column: ']),
                    dcc.Dropdown(id='e-dd-facet_col'),
                    html.P(['Facet Row: ']),
                    dcc.Dropdown(id='e-dd-facet_row'),
                    html.P(['On Hover show: ']),
                    html.Div([dcc.Dropdown(id='e-dd-hover',multi=True)]),
                    html.Div([html.Button('Build Graph', id='btn-scatter')]),
                ],className='three columns'),
                html.Div([
                    dcc.Graph(id='e-graph-scatter')
                ],className="nine columns"),
            ],className='row')
        ])


def fix_dbname(name):
    return name.strip().lower().replace(' ', '_').replace('(',
        '').replace(')', '').replace('%', 'percentage').replace('/', 
        '_per_').replace('.', '_').replace('-', '_')


def load_thread_data(thread_id):
    if thread_id != None and thread_id != None:
        meta_query = "SELECT metadata FROM threads WHERE threadid='{}'".format(thread_id)
        meta_df = pd.DataFrame(pd.read_sql(meta_query, con))
        if meta_df.empty:
            print("Thread doesn't exist")
            return None
        meta = meta_df.metadata[0]
        models = meta["thread"]["models"]
        for modelid in models:
            model = models[modelid]
            model_config = model["model_configuration"]
            runs_table_name = fix_dbname("{}_runs".format(model_config))

            op_table_query = "SELECT output_table_name from threads_output_table WHERE threadid='{}'".format(thread_id)
            op_table_df = pd.DataFrame(pd.read_sql(op_table_query, con))
            output_table_name = op_table_df.output_table_name[0]

            data_query = """SELECT * from {} runs LEFT JOIN {} outputs 
                ON runs.mint_runid = outputs.mint_runid AND runs.threadid = outputs.threadid
                WHERE runs.threadid='{}' """.format(runs_table_name, output_table_name, thread_id)
            df = pd.DataFrame(pd.read_sql(data_query, con))
            df = df.drop(["threadid", "mint_runid"], axis=1)
            return df

def store_data(dataframe):
    scols = dataframe.columns.values.tolist()
    sdata = dataframe.to_dict('records')
    return scols, sdata

## CALLBACKS ##
# Upload data into data stores
@app.callback([Output('e-cols','data'),Output('e-data','data')],
              [Input('thread_id', 'value')])
def update_output(thread_id):
    df = load_thread_data(thread_id)
    return store_data(df)

# Build dropdowns for Scatter plot
scatter_dropdowns = ['e-dd-x','e-dd-y','e-dd-color','e-dd-facet_col','e-dd-facet_row','e-dd-hover']
for dd in scatter_dropdowns:
    @app.callback(Output(dd,'options'),
                [Input('e-cols','data')])
    def scatter_options(cols):
        if cols is None:
            raise PreventUpdate
        col_options = [dict(label=x, value=x) for x in cols]
        return col_options

# Build Scatter graph
@app.callback(Output("e-graph-scatter", "figure"),
                [Input('e-dd-x','value'),Input('e-dd-y','value'),Input('e-dd-color','value'),
                Input('e-dd-facet_col','value'),Input('e-dd-facet_row','value'),Input('e-dd-hover','value')]
                ,[State('e-data','data')])
def make_scatter(x, y, color, facet_col, facet_row, hover_info,sdata):
    if sdata is None:
        raise PreventUpdate
    data_graph = pd.DataFrame(sdata)
    fig = px.scatter(
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
    
