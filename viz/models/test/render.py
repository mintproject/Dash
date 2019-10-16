from viz.utils import *

# styling
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
                        'https://codepen.io/chriddyp/pen/brPBPO.css']

layout = html.Div([
    html.Div(id='test_thread_id')
])


@app.callback(Output(component_id="test_thread_id", component_property='children'),
              inputs=[
                  Input('url', component_property='search')
              ]
              )
def obtain_thread_id(search):
    thread_id = parse_search(search)
    if thread_id is None or thread_id == '':
        raise PreventUpdate
    tablename = 'public."cycles-0.9.4-alpha-advanced-pongo-weather"'
    query = """select crop_name, fertilizer_rate, start_planting_day, start_year, end_year, weed_fraction, location
                from {} WHERE threadid = '{}';""".format(tablename, thread_id)
    df = pd.DataFrame(pd.read_sql(query, engine))
    crops = df.crop_name.unique()
    return crops
