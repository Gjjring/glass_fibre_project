import dash
from dash import html
from dash import dcc
from dash import callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import plotly.graph_objects as go
import plotly.express as px

import numpy as np
from fibre.optics import *
from fibre.ray import RaySimulation
from .utils import make_color

def layout():
    return html.Div(
        [
            dbc.Row(
                dbc.Col(
                    children = [
                        dcc.Tabs(
                            id='seite2-tabs-interface',
                            value='seite2-tab-1-einleitung',
                            children=[
                                dcc.Tab(
                                    label='Einleitung',
                                    value='seite2-tab-1-einleitung',
                                    ),
                                dcc.Tab(
                                    label='Glasfaser',
                                    value='seite2-tab-2-glass_faser'
                                ),
                                dcc.Tab(
                                    label='Glasfaser + Verschmutzung',
                                    value='seite2-tab-3-glass_faser_mit_oel'
                                ),
                                dcc.Tab(
                                    label='Glasfaser + Cladding + Verschmutzung',
                                    value='seite2-tab-4-glass_faser_mit_cladding'
                                )
                            ]),
                        html.Div(id='seite2-tabs-interface-content')
                    ],
                    width=8,
                    ),
                justify='center',
            ),

        ],
        className = 'container')


@callback(Output('seite2-tabs-interface-content', 'children'),
              Input('seite2-tabs-interface', 'value'))
def render_content_page2(tab):
    graph_width = 800
    graph_height = graph_width*(21/6)
    if tab == 'seite2-tab-1-einleitung':
        return html.Div(
                    children=[
                        html.H4(children='Die Glasfaser'),
                        html.P('Jetzt wollen wir das Internet mit Licht übertragen. '+
                                'Das heißt, wir wollen Licht von einem bestimmten Ort '+
                                'zu einem anderen schicken (z.B. von einer sozialen Medien '+
                                'Plattform zu deinem Laptop. Dazu brauchen wir eine Art Leitung, '+
                                'ähnlich wie wir Wasser in Rohren transportieren. Aber wie kann eine '+
                                'Leitung für Licht aussehen?'),
                        html.P('Wir wollen nicht, dass das Licht rauslaufen kann. Da klingt ein '+
                                'undurchlässiges Material wie Metall nicht schlecht. Gleichzeitig wird '+
                                'die Leitung sehr lange sein müssen. Wenn wir also Absorption in dem Material '+
                                'haben, auch wenn sie klein ist, kann das zu großen Verlusten führen – wie wenn '+
                                'man ein löchriges Rohr hat. Dann kommt gar kein Licht an. Wir brauchen also ein '+
                                'Material, das 100% vom Licht reflektiert. Weißt du aus Aufgabe 1 welches das sein könnte?'),
                        html.P('Frage zu dieser Aufgabe:'),
                        html.P(
                            html.Ol(
                                children =[
                                    html.Li('Wenn es keine Verschmutzung gibt, bis zu welchem Einfallswinkel funktioniert die Glasfaser?'),
                                    html.Li('Wenn es doch Verschmutzung gibt, bis zu welchem Einfallswinkel funktioniert die Glasfaser zuverlässig?'),
                                    html.Li('Wenn es Cladding und Verschmutzung gibt, bis zu welchem Einfallswinkel funktioniert die Glasfaser zuverlässig?'),
                                ]
                            )
                        )

                    ]
                )
    elif tab == 'seite2-tab-2-glass_faser':
        return html.Div(
                    title='Einfallswinkel anpassen',
                    children=[
                        html.P('Eine Glasfaser besteht hauptsächlich aus … Glas (große Überraschung). '+
                                'Hier kannst du den Einfallswinkel von der Glasfaser ändern. Weil die '+
                                'Seiten links und rechts ein anderes Lot haben als die Enden oben und unten, '+
                                'wird das Licht innerhalb der Glasfaser immer totalreflektiert! So lange das '+
                                'Licht in die Faser reinkommt, funktioniert die Glasfaser für jeden Einfallswinkel.'),
                        html.P('Wenn man zwei Spiegeln parallel gegenüber voneinander stellt, kann das reflektiere '+
                                'Licht zwischen den zwei Spiegeln hin und her laufen. Angenommen der Einfallswinkel '+
                                'kann beliebig ausgesucht werden, welche der vier verschiedenen Fälle in dieser '+
                                'Aufgabe würde man nehmen, damit das Licht ohne Verluste immer wieder hin und her läuft?'),
                        html.H4(className='app-controls-name',
                                 children='Einfallswinkel',
                                 style={'text-align': 'Left'}),
                        dcc.Slider(
                            id='seite2-inc_angle1',
                            min=1,
                            max=89,
                            step=1,
                            value=1,
                            marks=None,
                            tooltip={"placement": "bottom", "always_visible": True},
                        ),
                        dbc.Row(
                            children = [
                                dbc.Col(
                                    children = [
                                        dbc.Button(
                                            id='seite2-transmission_report1',
                                            disabled=True,
                                            children=""
                                        ),
                                    ]
                                ),
                            ],
                            style = {'marginTop':10, 'marginBottom':10},
                            justify='evenly'
                        ),
                        html.Div(
                            children = [
                                dcc.Graph(id = 'fibre_1',
                                        style={'width':graph_width,
                                                'height':graph_height}),
                            ],
                        )
                    ])
    elif tab == 'seite2-tab-3-glass_faser_mit_oel':
        return html.Div(
                    title='Einfallswinkel anpassen',
                    children=[
                        html.P('Nun haben wir leider ein bisschen Verschmutzung auf den Seiten von unserer Glasfaser. '+
                                'Dieses könnte Staub, Dreck oder Öl von unseren Händen sein. Was für ein Effekt hat '+
                                'die Verschmutzung auf unserer Glasfaser?'),
                        html.H4(className='app-controls-name',
                                 children='Einfallswinkel',
                                 style={'text-align': 'Left'}),
                        dcc.Slider(
                            id='seite2-inc_angle2',
                            min=1,
                            max=89,
                            step=1,
                            value=1,
                            marks=None,
                            tooltip={"placement": "bottom", "always_visible": True},
                        ),
                        dbc.Row(
                            children = [
                                dbc.Col(
                                    children = [
                                        dbc.Button(
                                            id='seite2-transmission_report2',
                                            disabled=True,
                                            children=""
                                        ),
                                    ]
                                ),
                            ],
                            style = {'marginTop':10, 'marginBottom':10},
                            justify='evenly'
                        ),
                        dcc.Graph(id = 'fibre_2',
                                  style={'width':graph_width,
                                         'height':graph_height}),
                    ])
    elif tab == 'seite2-tab-4-glass_faser_mit_cladding':
        return html.Div(
                    title='Einfallswinkel anpassen',
                    children=[
                        html.P('Wir wollen, dass unsere Glasfaser immer funktioniert, egal ob sie '+
                                'verschmutzt wird oder nicht. Deswegen machen wir eine extra Schicht '+
                                'um unsere Faser, die mit „Cladding“ bezeichnet wird. Dieses Cladding '+
                                'ist ein Material, das einen kleineren Brechungsindex hat als Glas. Wenn wir '+
                                'jetzt Licht durch die Faser schicken, und der Einfallswinkel klein genug ist, '+
                                'wird das Licht an der Grenzfläche zwischen Glaskern und dem Cladding Totalreflektiert. '+
                                'So können wir ganz ohne Verluste einen Lichtstrahl über eine sehr lange Distanz zum richtigen Ort schicken. '),
                        html.H4(className='app-controls-name',
                                 children='Einfallswinkel',
                                 style={'text-align': 'Left'}),
                        dcc.Slider(
                            id='seite2-inc_angle3',
                            min=1,
                            max=89,
                            step=1,
                            value=1,
                            marks=None,
                            tooltip={"placement": "bottom", "always_visible": True},
                        ),
                        dbc.Row(
                            children = [
                                dbc.Col(
                                    children = [
                                        dbc.Button(
                                            id='seite2-transmission_report3',
                                            disabled=True,
                                            children=""
                                        ),
                                    ]
                                ),
                            ],
                            style = {'marginTop':10, 'marginBottom':10},
                            justify='center'
                        ),
                        dbc.Row(
                            children = [
                                dbc.Col(
                                    children = [
                                        dcc.Graph(id = 'fibre_3',
                                                  style={'width':graph_width,
                                                         'height':graph_height}),
                                    ]
                                ),
                            ],
                            justify='center'
                        ),
                    ])
    else:
        raise ValueError("Unknown tab value: " + tab)



@callback(Output(component_id='fibre_1', component_property= 'figure'),
          Output(component_id='seite2-transmission_report1', component_property= 'children'),
              [Input(component_id='seite2-inc_angle1', component_property= 'value')])
def graph_update(inc_angle):
    #inc_angle = 45.
    if np.isclose(inc_angle,90.0):
        inc_angle = 89.0

    fig, t = fibre_optic_graph(inc_angle, 'Core')
    return fig, "Transmission {:.0f}%".format(abs(t)*100.)


@callback(Output(component_id='fibre_2', component_property= 'figure'),
          Output(component_id='seite2-transmission_report2', component_property= 'children'),
              [Input(component_id='seite2-inc_angle2', component_property= 'value')])
def graph_update(inc_angle):
    #inc_angle = 45.
    if np.isclose(inc_angle,90.0):
        inc_angle = 89.0

    fig, t = fibre_optic_graph(inc_angle, 'Core-Oil')
    return fig, "Transmission {:.0f}%".format(abs(t)*100.)

@callback(Output(component_id='fibre_3', component_property= 'figure'),
          Output(component_id='seite2-transmission_report3', component_property= 'children'),
              [Input(component_id='seite2-inc_angle3', component_property= 'value')])
def graph_update(inc_angle):
    #inc_angle = 45.
    if np.isclose(inc_angle,90.0):
        inc_angle = 89.0

    fig, t = fibre_optic_graph(inc_angle, 'Core-Cladding-Oil')
    return fig, "Transmission {:.0f}%".format(abs(t)*100.)

def plot_arc(figure, center, radius, start_angle, end_angle, color, name):
    phi = np.linspace(start_angle, end_angle, 100)
    r = np.ones(phi.shape)*radius
    x = r*np.cos(phi) + center[0]
    y = r*np.sin(phi) + center[1]

    figure.add_trace(go.Scatter(x=x, y=y,
                                mode='lines',
                                name=name + " {:.0f}".format(np.degrees(end_angle-start_angle)),
                                line=dict(color='rgba({}, {})'.format(color, 1.0), width=10., dash='dot'),
                                ))



def plot_segments(fig, obj, color):
    #for p0, p1 in pairwise(obj.exterior.coords):
    x, y = obj.exterior.xy
    fig.add_trace(go.Scatter(x=np.array(x), y=np.array(y),
                            mode='lines',
                            fill="toself",fillcolor=color,
                            line=dict(color='black', width=1.),showlegend=False))

def plot_ray(fig, ray, color):
    x = (ray.origin[0], ray.end_point[0])
    y = (ray.origin[1], ray.end_point[1])
    fig.add_trace(go.Scatter(x=x, y=y,
                            mode='lines',
                            line=dict(color='rgba({}, {:.2f})'.format(color, ray.intensity), width=2.),showlegend=False))

def fibre_optic_graph(inc_angle, geometry_selector):
    sim = RaySimulation()
    sim.init_ray(np.radians(inc_angle+270.))
    sim.init_background()
    if geometry_selector == 'Core-Oil':
        sim.add_oil(0.4, 0.7, 20., 0.15, 2)
    elif geometry_selector == 'Core-Cladding-Oil':
        sim.add_cladding(0.4, 0.5, 20.)
        sim.add_oil(0.5, 0.8, 20., 0.15, 2)
    #sim.add_oil(0.5, 0.8, 20., 0.1, 2)
    #sim.add_cladding(0.5, 0.8, 20.)
    fig = go.Figure()
    if geometry_selector == 'Core-Cladding-Oil':
        obj_colors = ['#c5f5f6', '#cce4ff', '#cce4ff', '#FFCC33', '#FFCC33']
    elif geometry_selector == 'Core-Oil':
        obj_colors = ['#c5f5f6', '#FFCC33', '#FFCC33']
    else:
        obj_colors = ['#c5f5f6']
    for iobj, obj in enumerate(sim.objects):
        color = obj_colors[iobj]
        plot_segments(fig, obj, color)
    #sim.find_intersection(sim.rays[0])
    sim.main()

    color1 = make_color(127, 201, 127)
    color2 = make_color(190,174,212)
    color3 = make_color(253,192,134)
    color4 = make_color(204, 0, 51)
    """
    fig.add_shape(type="rect",
        x0=-0.4, y0=-19.9, x1=0.4, y1=0.1,
        line=dict(
            color='#c5f5f6',
            width=0,
        ),
        layer="below",
        fillcolor='#c5f5f6',
    )
    if geometry_selector == 'Core-Cladding-Oil':
        fig.add_shape(type="rect",
            x0=-0.5, y0=-19.9, x1=-0.4, y1=0.1,
            line=dict(
                color='#cce4ff',
                width=0,
            ),
            layer="below",
            fillcolor='#cce4ff',
        )
        fig.add_shape(type="rect",
            x0=0.4, y0=-19.9, x1=0.5, y1=0.1,
            line=dict(
                color='#cce4ff',
                width=0,
            ),
            layer="below",
            fillcolor='#cce4ff',
        )
    """
    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False, plot_bgcolor='white',
                     xaxis_showticklabels=False, yaxis_showticklabels=False,
                     xaxis_zeroline=False,yaxis_zeroline=False)

    fig.update_xaxes(range=[-3., 3.], autorange=False)
    fig.update_yaxes(range=[-20.5, 0.5], autorange=False)


    for ray in sim.finished_rays:
        plot_ray(fig, ray, color4)


    return fig, sim.transmission
