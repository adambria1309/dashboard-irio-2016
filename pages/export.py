import pandas as pd
import dash
from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go
from urllib.request import urlopen
import json

df = pd.read_excel("irio_bersih untuk latihan.xlsx",sheet_name="Untuk Dashboard")

province = df['Provinsi'].unique()
sector = df['Kategori'].unique()

df_baru = df
df_baru["Ekspor"] = df['Permintaan Akhir dari luar provinsi']
df_baru["Impor"] = df['Permintaan Antara dari luar provinsi']
df_baru["% Ekspor"] = df['% permintaan akhir dari luar prov']
df_baru["% Impor"] = df['% bahan baku dari luar provinsi']

columns = ["Ekspor","Impor"]
variabel = df_baru.loc[:,columns].columns

# Geojson
with urlopen('https://github.com/superpikar/indonesia-geojson/blob/master/indonesia-edit.geojson?raw=true') as response:
    ind = json.load(response)

dash.register_page(__name__,path='/')

content = html.Div([
            dbc.Navbar(
                dbc.Container(
                    [
                        dbc.Row(
                            [
                                dbc.Col(dbc.NavbarBrand("DASHBOARD IRIO 2016", className="ms-xxl",style={'font-weight':'bold'})),
                                dbc.Col(html.Div([],id='provinsi-container',style={'justify-content':'left','margin-left':'-2.7%'})),
                                dbc.Col(
                                    html.Div([
                                        dcc.Dropdown(options=[{'label': i, 'value': i} for i in variabel],
                                            placeholder="Pilih Variabel", value="Ekspor",style={'width':'100%'},
                                            id='variable-selection',clearable=False,searchable=False)
                                            ],style={'display':'flex','width':'600%'})
                                        ),
                                dbc.Col(
                                    html.Div([
                                        dcc.Dropdown(options=[{'label': i, 'value': i} for i in sector],
                                            style={'width':'100%'},
                                            placeholder="Pilih Sektor", value="Industri Pengolahan",
                                            id='sector-selection',clearable=False,searchable=False)
                                            ],style={'width':'600%','display':'flex','margin-left':'600%'})
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
            
            ## batas navbar
            
            html.Div([
                html.Div(
                            [
                                dbc.Button(
                                    "Penting!",
                                    id="alert-toggle-fade",
                                    className="me-1",
                                    n_clicks=0,
                                ),
                                dbc.Alert(
                                    "Untuk memilih provinsi silahkan click pada salah satu polygon map. Nilai ekspor yang dimaksud di sini adalah nilai permintaan akhir dari luar provinsi. Sedangkan, impor yang dimaksud ialah nilai permintaan antara dari luar provinsi.",
                                    id="alert-fade",
                                    dismissable=True,
                                    is_open=True,
                                ),
                            ],style={'display':'flex','margin-top':'1%'}
                        ),
                html.Div([
                    html.Div([   
                        html.Div([
                                html.Div(
                                    [
                                        html.Div([
                                            
                                            dcc.Graph(figure={},id='map-tematik',
                                                    style={
                                                        'width': '58vw', 'height': '50vh',
                                                        'background':'#FFF',
                                                        'border-radius':'8px',
                                                        'margin-top':'1%',
                                                        'margin-left':'1%',
                                                        'padding':'0'},
                                                    clickData={'points': [{'location': 'Nusa Tenggara Timur'}]}),
                                            html.I(className='fa-solid fa-angles-right fa-beat-fade fa-2xl',style={'margin-top':'18%',
                                                                                                                  'margin-left':'5%',
                                                                                                                  'size':'120%'}),
                                            html.I(className='fa-solid fa-arrow-trend-down fa-beat-fade fa-2xl',style={'color':'#ffffff','margin-top':'34%',
                                                                                                         'margin-left':'-4%'})
                                            ],style={'display':'flex','width':'70vw','color':'#f2f2f2'}),

                                    html.Div([
                                    html.Div([
                                        dcc.Graph(figure={},id='variable-value',style={'width': '18vw', 'height': '45vh'})
                                    ],style={'width':'20vw','height':'50vh','background-color':'#FFFFFF','border-radius':'8px',
                                             'margin-left':'1%','margin-top':'1%','margin-bottom':'1%','padding':'1%'}),
                                        dcc.Graph(figure={},id='graph1',
                                                    style={
                                                        'width': '78vh', 'height': '50vh',
                                                        'background':'#FFF',
                                                        'border-radius':'8px',
                                                        'margin-left':'1%','margin-top':'1%',
                                                        'margin-bottom':'1%'}),
                                            ],style={'display':'flex'}) 
                                        ],style={'display':'grid'}),
                                ],style={'display':'grid'}),
                                html.Div([ 
                                        html.Div([
                                                dcc.Graph(figure={},id='variable-value-side',style={'width': '18vw', 'height': '48vh'})
                                            ],style={'width': '20vw', 'height': '50vh',
                                                    'text-align':'center',
                                                    'align-items':'center',
                                                    'justify-content':'center',
                                                    'border-radius':'8px',
                                                    'margin-top':'1%',
                                                    'margin-left':'1%',
                                                    'display':'grid',
                                                    'background-color':'#FFFFFF'}),
                                         html.Div(children=[
                                             dcc.Graph(figure={},id='variable-value-side2',style={'width': '18vw', 'height': '48vh'})
                                         ],
                                                    style={
                                                        'width': '20vw', 'height': '50vh',
                                                        'text-align':'center',
                                                        'align-items':'center',
                                                        'justify-content':'center',
                                                        'border-radius':'8px',
                                                        'margin-top':'5%',
                                                        'margin-left':'1%',
                                                        'display':'grid',
                                                        'background-color':'#FFFFFF'})
                                                        ]
                                                        ,style={'margin-left':'-5%','padding-left':'1%','padding-right':'1%',
                                                                'margin-top':'0.5%','display':'gird'})
                                    ],style={'display':'flex'}),
                        ],style={'display':'grid','grid-template-columns':'155vh 80vh'})
                ],style={'margin-left':'8.5%'}
            )
        ])


layout = content

@callback(
        Output('provinsi-container','children'),
        Input('map-tematik','clickData')
)
def provinsi_container(value_prov):
    value_prov = value_prov['points'][0]['location']
    return [dbc.NavbarBrand(f"{value_prov}".upper(),style={'font-weight':'bold',
                                                           'color':'#FFFFFF','font-size':'1.1em'})]

@callback(
    Output('map-tematik','figure'),
    [Input('variable-selection','value'),
    Input('sector-selection','value')]
)
def upate_figure(value_var,value_sec):
    if value_var:
        if value_sec:
            fdf = df_baru[df_baru["Kategori"]==f'{value_sec}']
            fig1 = px.choropleth_mapbox(
                fdf,
                geojson=ind,
                locations='Provinsi',
                featureidkey='properties.state',
                color=f'{value_var}',
                color_continuous_scale="Viridis",
                range_color=(fdf[f'{value_var}'].min(),fdf[f'{value_var}'].max()),
                mapbox_style='white-bg',
                center = dict(lat = -5.135399, lon =  119.423790),
                zoom = 3)

            fig1.update_layout(
                plot_bgcolor= "rgba(0, 0, 0, 0)",
                paper_bgcolor= "rgba(0, 0, 0, 0)",
                font_family="Arial",
                font_color="blue",
                title={
                    'y':0.9,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                font={'size': 12},
                margin=dict(t=40, b=80, l=80, r=40)
                )
    return fig1

@callback(
        Output('graph1','figure'),
        Input('map-tematik','clickData'),
        Input('variable-selection','value'),
        Input('sector-selection','value')
)
def update_graph1(value_prov,value_var,value_sec):
    value_prov = value_prov['points'][0]['location']
    fdf = df_baru[df_baru['Provinsi']==f'{value_prov}']
    fdf = fdf.sort_values(f'{value_var}', ascending = False).head(5).reset_index()
    # fig2 = px.bar(fdf,y='Kode Kategori',x='Permintaan Akhir',orientation='h',title=f'Permintaan Akhir Provinsi {value_prov}')
    fig2 = go.Figure(layout=dict(xaxis = dict(title = 'Kode Sektor', showgrid=False, ticks='outside',mirror=True,showline=True),
                                 yaxis = dict(title = 'Nilai Ekspor-Impor', showgrid=False, ticks='outside',mirror=True,showline=True)))
    fig2.add_trace(go.Bar(x=fdf["Kode Kategori"],
                     y=fdf[f"Ekspor"],
                     name="Ekspor",
                     marker=dict(color = '#58C565')))
    fig2.add_trace(go.Bar(x=fdf["Kode Kategori"],
                     y=fdf[f"Impor"],
                     name="Impor",
                     marker=dict(color = '#3C4E8A')))
    fig2.update_layout(
                plot_bgcolor= "rgba(0, 0, 0, 0)",
                paper_bgcolor= "rgba(0, 0, 0, 0)"
                )
    fig2.update_layout(title_text=f"Perbandingan Ekspor-Impor Pada<br>Top 5 Sektor Dengan {value_var} Terbesar",
                       title={
                           'y':0.9,
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top'},
                        legend=dict(yanchor="top", y=-0.4, xanchor="left", x=0.0),
                        font={'size':12},
                        font_family="Arial",
                        margin=dict(t=100, b=80, l=80, r=40))
    return fig2

@callback(
        Output('variable-value-side','figure'),
        Input('variable-selection','value'),
        Input('sector-selection','value'),
        Input('map-tematik','clickData')
)
def update_variable_value(var_value,sec_value,value_prov):
    value_prov = value_prov['points'][0]['location']
    # sumgroup = df[['Provinsi','Permintaan Antara dari luar provinsi']].groupby('Provinsi').sum()
    # max_ = sumgroup['Permintaan Antara dari luar provinsi'].max()
    df_prov = df_baru[df_baru['Provinsi']==f'{value_prov}'][['Kode Kategori',f'{var_value}']]
    max_ = df_prov[f'{var_value}'].max()
    # sumgroup = pd.DataFrame(sumgroup).reset_index()
    # prov_max = sumgroup[sumgroup['Permintaan Antara dari luar provinsi']==max_]['Provinsi'].values[0]
    sec_max = df_prov[df_prov[f'{var_value}']==max_]['Kode Kategori'].values[0]
    # exp_max = sumgroup[sumgroup['Permintaan Antara dari luar provinsi']==max_]['Permintaan Antara dari luar provinsi'].values[0]

    variabel_rp = ['NTB','Output','Total Permintaan Antara','Permintaan Antara Dalam Provinsi','Permintaan Antara dari luar provinsi',
                   'Permintaan Akhir','Permintaan Akhir dari dalam provinsi','Permintaan Akhir dari luar provinsi']

    labels = [f'{sec_max}','Sektor Lainnya']
    # full = sumgroup['Permintaan Antara dari luar provinsi'].sum()
    full = df_prov[f'{var_value}'].sum()
    values = [max_, full-max_]

    # Use `hole` to create a donut-like pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5,marker_colors=['#7616C0','#AABBCC'],textinfo='none',
                                 hoverinfo='percent+label',direction ='clockwise',
                                 sort=False)])
    fig.update(layout_showlegend=False)
    fig.update_layout(title_text=f'{var_value} Terbesar<br>Sektor {sec_max}',
                       title={
                           'y':0.9,
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top'},
                        font={'size':12},
                        font_family="Arial",
                        margin=dict(t=80, b=20, l=15, r=15)
                       )
    fig.add_annotation(text=f'Rp{round(max_/1000000,2)}J', x=0.5, y=0.5, font={'size':20}, showarrow=False,
                       xref="x domain",
                        yref="y domain",)

    return fig

@callback(
        Output('variable-value','figure'),
        Input('variable-selection','value'),
        Input('sector-selection','value'),
        Input('map-tematik','clickData')
)
def update_variable_value(var_value,sec_value,value_prov):
    value_prov = value_prov['points'][0]['location']
    fdf = df_baru[df_baru['Provinsi']==f'{value_prov}']
    fdf["NX"] = fdf['Ekspor']-fdf['Impor']
    fdf = fdf.sort_values('NX', ascending = False).head(3).reset_index()

    values = fdf['NX'].values
    labels = fdf['Kode Kategori'].values

    # Use `hole` to create a donut-like pie chart '#BFACE0','#EBC7E8'
    fig = go.Figure(data=[go.Pie(labels=labels, values=values,marker_colors=['#7616C0','#645CAA','#A084CA'],
                                #  textinfo='none',
                                texttemplate=[f'Rp{round(values[0]/1000000,2)} Juta','',''],
                                 hoverinfo='percent+label',direction ='clockwise',
                                 sort=True,pull=[0.1, 0, 0])])
    fig.update(layout_showlegend=False)
    fig.update_layout(title_text=f'Top 3 Sektor<br>Dengan Surplus Terbesar',
                       title={
                           'y':0.9,
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top'},
                        font={'size':12},
                        font_family="Arial",
                        margin=dict(t=80, b=20, l=15, r=15)
                       )

    return fig

@callback(
        Output('variable-value-side2','figure'),
        Input('variable-selection','value'),
        Input('sector-selection','value'),
        Input('map-tematik','clickData')
)
def update_variable_value(var_value,sec_value,value_prov):
    value_prov = value_prov['points'][0]['location']
    nilai = df_baru[(df_baru['Provinsi']==f'{value_prov}') & (df['Kategori']==f'{sec_value}')][f'{var_value}'].values[0]
    sumsektor = df_baru[(df_baru['Provinsi']==f'{value_prov}')][f'{var_value}'].sum()

    labels = [f'{sec_value}','Sektor lainnya']
    values = [nilai, sumsektor]
    
    key_prov = df_baru[df_baru['Provinsi']=='Papua']['Kategori'].values
    value_code = df_baru[df_baru['Provinsi']=='Papua']['Kode Kategori'].values
    code_sec = dict(zip(key_prov,value_code))

    # Use `hole` to create a donut-like pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5,marker_colors=['#58C565','#AABBCC'],textinfo='none',
                                 hoverinfo='label+value',direction ='clockwise',
                                 sort=False)])
    fig.update(layout_showlegend=False)
    fig.update_layout(title_text=f'Kontribusi Sektor {code_sec[sec_value]} Terhadap<br>{var_value}',
                       title={
                           'y':0.9,
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top'},
                        font={'size':12},
                        font_family="Arial",
                        margin=dict(t=80, b=15, l=15, r=15)
                       )
    fig.add_annotation(text=f'{round(nilai/sumsektor*100,2)}%', x=0.5, y=0.5, font={'size':20}, showarrow=False,
                       xref="x domain",
                        yref="y domain",
                        font_family="Arial")

    return fig

@callback(
    Output("alert-fade", "is_open"),
    [Input("alert-toggle-fade", "n_clicks")],
    [State("alert-fade", "is_open")],
)
def toggle_alert(n, is_open):
    if n:
        return not is_open
    return is_open