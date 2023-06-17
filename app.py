import pandas as pd
import dash
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import dash_daq as daq
from urllib.request import urlopen
import json

df = pd.read_excel("irio_bersih untuk latihan.xlsx",sheet_name="Untuk Dashboard")

province = df['Provinsi'].unique()
sector = df['Kategori'].unique()
columns = ["Output","Income Multiplier","Output Multiplier"]
variabel = df.loc[:,columns].columns


# Geojson
with urlopen('https://github.com/superpikar/indonesia-geojson/blob/master/indonesia-edit.geojson?raw=true') as response:
    ind = json.load(response)

app = Dash(__name__,
           external_stylesheets=[dbc.themes.BOOTSTRAP,dbc.icons.FONT_AWESOME],
           use_pages=True)

server = app.server

sidebar = html.Div(
    [
        html.Div(
            [
                # width: 3rem ensures the logo is the exact width of the
                # collapsed sidebar (accounting for padding)
                html.Img(src='./assets/profile.png', style={"width": "3rem"}),
                html.H2("Wellcome!"),
            ],
            className="sidebar-header",
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink(
                    [html.I(className="fa-solid fa-scale-balanced me-4"), html.Span("EXPOR-IMPOR",style={'font-size':'20px','font-family':'Arial'})],
                    href="/",
                    active="exact",
                ),
                dbc.NavLink(
                    [html.I(className="fa-solid fa-xmark me-4"), html.Span("MULTIPLIER",style={'font-size':'20px','font-family':'Arial'})],
                    href="/multiplier",
                    active="exact",
                ),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="sidebar",
)

app.layout = html.Div([
    sidebar,
    dash.page_container,
],className='page',style={'background-image':'linear-gradient( 108.7deg,  rgba(221,22,224,1) 11%, rgba(111,22,190,1) 88.2% )','width':'100%','height':'100%'})

if __name__== '__main__':
    app.run_server(debug=True)