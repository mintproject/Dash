from viz.utils import * 
import random

list_of_images = [
    '/tmp/images/2.png',
    '/tmp/images/3.png'
]

def generate_layout(thread_id=None):
    # layout = html.Div([
    #     dcc.Dropdown(
    #         id='image-dropdown',
    #         options=[{'label': i, 'value': i} for i in list_of_images],
    #         # initially display the first entry in the list
    #         value=list_of_images[0]
    #     ),
    #     html.Img(id='image')
    # ])

    return html.Div([
        html.Div([
            html.H3(['Flooding']),
            html.Label(['for MINT modeling thread: '],style={'float':'left'}),
            dcc.Input(id='images_thread_id', value=thread_id,style={'float':'left'}),
                html.Div(id='dd-output-container'),
        ],className='row'),


        dcc.Dropdown(
            id='images_dropdown',
        ),
        html.Img(id='image')
    ])

@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_output(value):
    return 'You have selected "{}"'.format(value)



@app.callback(
    [
        Output('images_dropdown','options'),
        Output('images_dropdown','value')
    ],
    [
        Input(component_id='images_thread_id', component_property='value')
    ]
    )
def set_dropdowns(thread_id):
    items = [
    ]
    df = obtain_params(thread_id)

    for index, row in df.iterrows():
        print("insert {}".format(row))
        items.append({"label": "{} - {}".format(row['ts_sfctmp'], row['ts_prcp']), "value": random.randint(1,101)})

    return [
        items, 
        items[0]["value"]
    ]

def obtain_params(thread_id):
    thread_id='VggqferoeUnXQB93yeBM';
    tablename = 'pihm_v4_1_0_runs'
    query = """SELECT ts_sfctmp, ts_prcp from {} where threadid='{}';""".format(tablename,thread_id)
                
    df = pd.DataFrame(pd.read_sql(query, con))
    if df.empty:      
        empty_data_options = [{'label':'Waiting on Data Ingestion','value':'waiting'}]
        emptymsg = 'Please Wait for Data Ingestion'
    return df


@app.callback(
        Output('image', 'src'),
    [   
        Input('images_dropdown', 'value')
    ]
    )
def update_image_src(image_path):
    # print the image_path to confirm the selection is as expected
    print('current image_path = {}'.format(image_path))
    encoded_image = base64.b64encode(open(image_path, 'rb').read())
    return 'data:image/png;base64,{}'.format(encoded_image.decode())


if __name__ == '__main__':
    app.run_server(debug=True, port=8053, host='0.0.0.0')