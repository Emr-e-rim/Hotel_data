from dash import dash, html, dcc, callback_context, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from data import getCityReviews, initData, getHotelData
import pandas as pd

data = initData()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.title = "Hotel Reviews"

def setStyle(fig):
    fig.update_layout(dragmode="zoom")
    fig.update_layout(modebar_orientation="v")
    fig.update_layout(modebar_add="zoom")
    fig.update_layout(modebar_remove=["lasso", "select"])
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_layout(clickmode='event+select')
    fig.update_layout(coloraxis_showscale=False)
    return fig

def setTheme(fig):
    fig.update_layout(paper_bgcolor="#222")
    fig.update_layout(font_color="#fff")
    return fig

def createPie(df, n):
    n = df[df.Reviewer_Score < n].count()[0]
    d = {'score': [n, abs(len(df)-n)], 'category': ['Negative', 'Positive']}
    d = pd.DataFrame(data=d)
    fig = px.pie(d, values='score', names='category', height=280, width=445, template="plotly_dark")
    return fig

def updateMap(map, lat, lon, zoom=12):
    map.update_layout(
        mapbox=dict(
            center=dict(
                lat=lat,
                lon=lon
            ),
        zoom=zoom)
    )
    return map

mapSettings = px.scatter_mapbox(data, lat="lat", lon="lng", hover_name="Hotel_Name", size="Average_Score",
                            color="Average_Score", color_continuous_scale=["Orange", "Yellow", "Green"],
                            zoom=4, height=640, width=1040, mapbox_style="open-street-map", opacity=1,
                            hover_data={'lat':False,'lng':False,'Average_Score':True,"Hotel_Address":True},
                            custom_data=["City"], template="plotly_dark"
                            )
map = mapSettings
map = setStyle(map)

app.layout = html.Div([
    html.Br(),
    html.H1('Find your hotel', style={'textAlign': 'center'}),
    html.Br(),
    html.Div(children=[
        html.Div(
            children=[
                dcc.Graph(
                    id='map',
                    figure=map
                )
            ]),

        html.Div(children=[
            html.Div([
                dbc.DropdownMenu(
                label="Select your destination",
                menu_variant="dark",
                size="lg",
                children=[
                        dbc.DropdownMenuItem("All", id="All"),
                        dbc.DropdownMenuItem("Amsterdam", id="Amsterdam"),
                        dbc.DropdownMenuItem("Barcelona", id="Barcelona"),
                        dbc.DropdownMenuItem("London", id="London"),
                        dbc.DropdownMenuItem("Milan", id="Milan"),
                        dbc.DropdownMenuItem("Paris", id="Paris"),
                        dbc.DropdownMenuItem("Vienna", id="Vienna"),
                ]
                )
            ], style={'padding': 5}),
            html.Br(),
            html.Div(children=[
                dcc.Markdown("""
                    **City Stats**
                """),
                dcc.Graph(
                    id='averageScore'
                ),
                html.Br(),
                dcc.Graph(
                    id='reviewRatio'
                )
            ])
        ], style={'padding': 5})
    ], style={'padding': 0, 'display': 'flex', 'flex-direction': 'row'}),

    html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle(id='hotel-name')),
                dbc.ModalBody(
                    [
                        dbc.Label("Address:", id='hotel-address', style=dict(marginLeft=10, marginRight=70)),
                        dbc.Label("City:", id='hotel-city', style=dict(marginRight=70)),
                        dbc.Label("Average Score:", id='hotel-score'),
                        html.Br(), html.Br(),
                        html.Div(
                            id="table",
                            style={"maxHeight": "595px", "overflowY": "scroll"}
                            )
                    ]
                ),
            ],
            id="modal",
            fullscreen=True
        )
    ])
])

@app.callback(
    Output("modal", "is_open"),
    Input('map', 'selectedData'),
    State("modal", "is_open"),
    prevent_initial_call=True
)
def toggle_modal(n, is_open):
    if n:
        return not is_open
    return is_open
    
@app.callback(
    Output('map', 'figure'),
    Output('averageScore', 'figure'),
    Output('reviewRatio', 'figure'),
    [
        Input("All", "n_clicks"),
        Input("Amsterdam", "n_clicks"),
        Input("Barcelona", "n_clicks"),
        Input("London", "n_clicks"),
        Input("Milan", "n_clicks"),
        Input("Paris", "n_clicks"),
        Input("Vienna", "n_clicks")
    ]
)
def update_output(*args):
    ctx = callback_context
    if not ctx.triggered:
        city = "All"
    else:
        city = str(callback_context.triggered[0]["prop_id"].split(".")[0])
    
    if(city == "Amsterdam"):
        map = mapSettings
        map = setStyle(map)
        map = updateMap(map, lat=52.36, lon=4.89)
    elif(city == "Barcelona"):
        map = mapSettings
        map = setStyle(map)
        map = updateMap(map, lat=41.385, lon=2.17, zoom=13)
    elif(city == "London"):
        map = mapSettings
        map = setStyle(map)
        map = updateMap(map, lat=51.51, lon=-0.12)
    elif(city == "Milan"):
        map = mapSettings
        map = setStyle(map)
        map = updateMap(map, lat=45.47, lon=9.18)
    elif(city == "Paris"):
        map = mapSettings
        map = setStyle(map)
        map = updateMap(map, lat=48.86, lon=2.34)
    elif(city == "Vienna"):
        map = mapSettings
        map = setStyle(map)
        map = updateMap(map, lat=48.21, lon=16.36)
    else:
        map = mapSettings
        map = setStyle(map)
        map = updateMap(map, lat=48.5, lon=4, zoom=4)

    if(city != "All"):
        score = data[data['City'] == city].Average_Score.mean()
    elif(city == ""):
        score = data.Average_Score.mean()
    else:
        score = data.Average_Score.mean()
        
    fig = go.Figure().add_trace(go.Indicator(
            mode = "number",
            value = score,
            title = f"Average Score of {city}",
            title_font_size=25,
            number_font_size=50))

    fig.update_layout(
        paper_bgcolor="lightgray",
        height=180, width=445
    )

    df = getCityReviews(city)
    pie = createPie(df, 6)
    
    return [map, fig, pie]

@app.callback(
    [
        Output("hotel-name", "children"),
        Output("hotel-address", "children"),
        Output("hotel-city", "children"),
        Output("hotel-score", "children"),
        Output("table", "children")
    ],
    Input('map', 'selectedData'),
    prevent_initial_call=True
)
def display_selected_data(selectedData):

    hotel = selectedData['points'][0]['hovertext']
    city = selectedData['points'][0]['customdata'][0]
    address = selectedData['points'][0]['customdata'][4]
    score = selectedData['points'][0]['customdata'][3]
    df = getHotelData(hotel)

    return (hotel, ["Address: ", address], ["City: ", city], ["Average Score: ", score],
            dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, id="review-table")) #json.dumps(hotel, indent=2)
            
if __name__ == '__main__':
    app.run_server(debug=True)