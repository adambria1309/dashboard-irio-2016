import dash
from dash import Dash, html
import dash_bootstrap_components as dbc

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
                html.I(className="fa-solid fa-face-smile me-5 fa-2xl",style={'color':'#0062ff','margin-left':'10px'}),
                html.H2("Wellcome!",style={'color':'#0062ff','margin-left':'-10%'}),
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

app.layout = dbc.Spinner([
    html.Div([
    sidebar,
    dash.page_container,
    ],className='page',style={'background-image':'linear-gradient( 108.7deg,  rgba(221,22,224,1) 11%, rgba(111,22,190,1) 88.2% )','width':'100%','height':'100%'})
],color="primary",fullscreen=True,size='md')


if __name__== '__main__':
    app.run_server(debug=True)