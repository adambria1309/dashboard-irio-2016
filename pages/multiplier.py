import pandas as pd
import dash
from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go
import numpy as np

df = pd.read_excel("irio_bersih untuk latihan.xlsx",sheet_name="Untuk Dashboard")

province = df['Provinsi'].unique()
sector = df['Kategori'].unique()

columns = ["Income Multiplier","Output Multiplier"]
variabel = df.loc[:,columns].columns

dash.register_page(__name__,path='/multiplier')

content = html.Div([
    
    dbc.Navbar(
                dbc.Container(
                    [
                        dbc.Row(
                            [
                                dbc.Col(dbc.NavbarBrand("DASHBOARD IRIO 2016", className="ms-xxl",style={'font-weight':'bold'})),
                                dbc.Col(
                                    html.Div([
                                        dcc.Dropdown(options=[{'label': i, 'value': i} for i in variabel],
                                            placeholder="Pilih Variabel", value="Output Multiplier",style={'width':'100%'},
                                            id='variable-selection-1',clearable=False,searchable=False)
                                            ],style={'display':'flex','width':'600%','margin-left':'200%'})
                                        ),
                                dbc.Col(
                                    html.Div([
                                        dcc.Dropdown(options=[{'label': i, 'value': i} for i in sector],
                                            style={'width':'100%'},
                                            placeholder="Pilih Sektor", value="Industri Pengolahan",
                                            id='sector-selection-1',clearable=False,searchable=False)
                                            ],style={'width':'600%','display':'flex','margin-left':'800%'})
                                        )
                            ],
                            align="center",
                            className="g-0",
                        ),
                    ]
                ),
            color="#7616C0",
            dark=True,
            className="sticky-top"
            ),
   
    html.Div(
                [
                    dbc.Button(
                        "Penting!",
                        id="alert-toggle-fade-1",
                        className="me-1",
                        n_clicks=0,
                    ),
                    dbc.Alert(
                        "Untuk memilih provinsi silahkan click pada salah satu batang bar cahrt.",
                        id="alert-fade-1",
                        dismissable=True,
                        is_open=True,style={'margin-right':'5%'}
                    ),
                ],style={'display':'flex','margin-top':'1%','margin-left':'8%'}
            ),

    html.Div([
        html.Div([
            dcc.Graph(figure = {},
                      id='crossfilter-income-output',style={'height':'95vh','width':'50vw','margin-top':'1%'},
                      clickData={'points': [{'customdata': 'Nusa Tenggara Timur'}]}
            )
        ], style={'margin-bottom':'1%','height': '97vh','width':'52vw', 'padding': '0','background':'#ffffff','border-radius':'8px'}),
        html.Div([
            html.Div([dcc.Graph(figure = {},id='top-5-income',style={'padding':'0','height':'44vh','width':'28vw','margin-top':'2%','margin-left':'1%','margin-right':'1%'})],
                     style={'height': '46vh','width':'30vw','background':'#ffffff','border-radius':'8px','margin-bottom':'2%'}),
            html.Div([dcc.Graph(figure = {},id='top-5-output',style={'padding':'0','height':'44vh','width':'28vw','margin-top':'2%','margin-left':'1%','margin-right':'1%'})],
                     style={'height': '46vh','width':'30vw','background':'#ffffff','border-radius':'8px','margin-bottom':'2%'})            
        ], style={'display': 'grid', 'height': '100vh','width':'25vw','margin-left':'5%'})
    ],style={'margin-left':'8%','margin-top':'3%','margin-bottom':'1%','display':'flex','width':'100vw','height':'100vh'})
])

layout = dbc.Spinner([content],color="primary",fullscreen=True,size='md')

@callback(
    Output('crossfilter-income-output', 'figure'),
    Input('sector-selection-1', 'value'),
    Input('variable-selection-1','value'))
def update_graph(value_sec,value_var):
    dff = df[df['Kategori'] == value_sec]
    dff["Nilai Output Multiplier"] = np.where(dff['Output Multiplier'] >= 1.5,">= 1.5","< 1.5")
    dff["Nilai Income Multiplier"] = np.where(dff['Income Multiplier'] >= 0.5,">= 0.5","< 0.5")


    if (value_var=='Income Multiplier'):
        fig = px.bar(dff, y='Provinsi', x=value_var,
                     hover_data=[value_var, 'Output Multiplier'], color='Output Multiplier',
                     labels={'pop':f'{value_var}'},orientation='h')
        fig.update_traces(customdata=dff['Provinsi'])
        fig.update_layout(clickmode='event')
        fig.update_layout(margin={'l': 40, 'b': 40, 't': 40, 'r': 0})

        return fig
    else:
        fig = px.bar(dff, y='Provinsi', x=value_var,
                     hover_data=[value_var, 'Income Multiplier'], color='Income Multiplier',
                     labels={'pop':f'{value_var}'},custom_data='Provinsi',orientation='h')
        fig.update_traces(customdata=dff['Provinsi'])
        fig.update_layout(clickmode='event')
        fig.update_layout(margin={'l': 40, 'b': 40, 't': 40, 'r': 0})

        return fig


def create_pie_5(labels, values, title):

    fig = go.Figure(data=[go.Pie(labels=labels, values=values,marker_colors=['#7616C0','#645CAA','#A084CA'],
                                #  textinfo='none',
                                 hoverinfo='percent+label',direction ='clockwise',
                                 sort=True,pull=[0.1, 0, 0, 0, 0],
                                 texttemplate=[f'Top 1: {labels[0]}',f'Top 2: {labels[1]}',f'Top 3: {labels[2]}',f'Top 4: {labels[3]}',f'Top 5: {labels[4]}'])])
    fig.update(layout_showlegend=False)
    fig.update_layout(font={'size':12},
                        font_family="Arial"
                       )

    fig.add_annotation(x=0, y=1.05, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       text=title)

    fig.update_layout(margin={'l': 5, 'b': 0, 'r': 10, 't': 50})

    return fig


@callback(
    Output('top-5-income', 'figure'),
    Input('crossfilter-income-output', 'clickData'))
def update_income_multiplier(provinsi):
    value_prov = provinsi['points'][0]['customdata']

    fdf = df[df['Provinsi']==value_prov]
    fdf = fdf.sort_values('Income Multiplier', ascending = False).head(5).reset_index()

    values = fdf['Income Multiplier'].values
    labels = fdf['Kode Kategori'].values

    title = '<b>{}</b><br>Top 5 Sektor Dengan Income Multiplier Tertinggi'.format(value_prov)
    return create_pie_5(labels, values, title)


@callback(
    Output('top-5-output', 'figure'),
    Input('crossfilter-income-output', 'clickData'))
def update_output_multiplier(provinsi):
    value_prov = provinsi['points'][0]['customdata']
    fdf = df[df['Provinsi']==value_prov]
    fdf = fdf.sort_values('Output Multiplier', ascending = False).head(5).reset_index()

    values = fdf['Output Multiplier'].values
    labels = fdf['Kode Kategori'].values

    title = '<b>{}</b><br>Top 5 Sektor Dengan Output Multiplier Tertinggi'.format(value_prov)
    return create_pie_5(labels, values, title)

@callback(
    Output("alert-fade-1", "is_open"),
    [Input("alert-toggle-fade-1", "n_clicks")],
    [State("alert-fade-1", "is_open")],
)
def toggle_alert(n, is_open):
    if n:
        return not is_open
    return is_open