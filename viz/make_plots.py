from viz.utils import *

# functions to convert inputs into plotly subplots
#GRAPHING FUNCTIONS
# Function to return choropleth_mapbox
def create_choropleth(df, geojson, locations, color,
                        hover_name = None, hover_data = None, animation_frame = None, opacity = None ,
                        color_continuous_scale=None, range_color = None, mapbox_style="carto-positron"):
    fig = px.choropleth_mapbox(df, geojson=geojson, locations=locations, color=color,
                                hover_name=hover_name,
                                hover_data = hover_data,
                                animation_frame = animation_frame,
                                range_color = range_color,
                                mapbox_style = mapbox_style,
                                opacity = opacity,
                                zoom=4, center = {"lat": 31.9686, "lon": -98.5018},
                              )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_layout(clickmode = 'event+select')
    return fig

# create line graph
def create_line_graph(df, xaxis, yaxis, color):
    fig = px.line(df, x=xaxis, y=yaxis, color=color,height=250)
    fig.update_layout(
        # showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0),
    )
    return fig

def create_datatable(df, table_id):
    return dash_table.DataTable(
            id=table_id,
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
                style_table={
                    'maxHeight': '450px',
                    'overflowY': 'scroll'
                },
        )
