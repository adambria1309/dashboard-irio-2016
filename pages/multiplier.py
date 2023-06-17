import pandas as pd
import dash
from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go

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
                                        dcc.Dropdown(options=[{'label': i, 'value': i} for i in sector],
                                            style={'width':'100%'},
                                            placeholder="Pilih Sektor", value="Industri Pengolahan",
                                            id='sector-selection-1',clearable=False,searchable=False)
                                            ],style={'width':'600%','display':'flex','margin-left':'200%'})
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

    html.Div([
        html.Div([
            dcc.Graph(
                id='crossfilter-income-output',
                style={'height':'98%','margin-top':'1%'},
                clickData={'points': [{'customdata': 'Nusa Tenggara Timur'}]}
            )
        ], style={'margin-bottom':'1%','width': '50%','height':'100vh', 'padding': '0','background':'#ffffff','border-radius':'8px'}),
        html.Div([
            html.Div([dcc.Graph(id='top-5-income',style={'padding':'0','height':'95%','margin-top':'1%','margin-left':'1%','margin-right':'1%'})],style={'width': '50%','background':'#ffffff','border-radius':'8px','margin-bottom':'2%'}),
            html.Div([dcc.Graph(id='top-5-output',style={'padding':'0','height':'95%','margin-top':'1%','margin-left':'1%','margin-right':'1%'})],style={'width': '50%','background':'#ffffff','border-radius':'8px','margin-bottom':'2%'})            
        ], style={'display': 'grid', 'width': '50%','margin-left':'5%'})
    ],style={'margin-left':'8%','margin-top':'3%','margin-bottom':'1%','display':'flex'})
])

layout = content

@callback(
    Output('crossfilter-income-output', 'figure'),
    Input('sector-selection-1', 'value'))
def update_graph(value_sec):
    dff = df[df['Kategori'] == value_sec]
    fig = px.scatter(
        dff,x='Income Multiplier',
        y='Output Multiplier',
        hover_name=dff['Provinsi'])
    fig.update_traces(customdata=dff['Provinsi'])
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 40, 'r': 40}, hovermode='closest')

    return fig


def create_pie_5(labels, values, title):

    fig = go.Figure(data=[go.Pie(labels=labels, values=values,marker_colors=['#7616C0','#645CAA','#A084CA'],
                                #  textinfo='none',
                                 hoverinfo='percent+label',direction ='clockwise',
                                 sort=True,pull=[0.1, 0, 0, 0, 0],
                                 texttemplate=[f'Top 1: {labels[0]}',f'Top 2: {labels[1]}',f'Top 3: {labels[2]}',f'Top 4: {labels[3]}',f'Top 5:cls {labels[4]}'])])
    fig.update(layout_showlegend=False)
    fig.update_layout(font={'size':12},
                        font_family="Arial",
                        margin=dict(t=80, b=20, l=15, r=15)
                       )

    fig.add_annotation(x=0, y=1, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       text=title)

    fig.update_layout(height=225, margin={'l': 20, 'b': 0, 'r': 10, 't': 50})

    return fig


@callback(
    Output('top-5-income', 'figure'),
    Input('crossfilter-income-output', 'clickData'))
def update_y_timeseries(provinsi):
    value_prov = provinsi['points'][0]['customdata']
    fdf = df[df['Provinsi']==f'{value_prov}']
    fdf = fdf.sort_values('Income Multiplier', ascending = False).head(5).reset_index()

    values = fdf['Income Multiplier'].values
    labels = fdf['Kode Kategori'].values

    title = '<b>{}</b><br>Top 5 Sektor Dengan Income Multiplier Tertinggi'.format(value_prov)
    return create_pie_5(labels, values, title)


@callback(
    Output('top-5-output', 'figure'),
    Input('crossfilter-income-output', 'clickData'))
def update_x_timeseries(provinsi):
    value_prov = provinsi['points'][0]['customdata']
    fdf = df[df['Provinsi']==f'{value_prov}']
    fdf = fdf.sort_values('Output Multiplier', ascending = False).head(5).reset_index()

    values = fdf['Output Multiplier'].values
    labels = fdf['Kode Kategori'].values

    title = '<b>{}</b><br>Top 5 Sektor Dengan Output Multiplier Tertinggi'.format(value_prov)
    return create_pie_5(labels, values, title)
