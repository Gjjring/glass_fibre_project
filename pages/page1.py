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
from .utils import make_color


def layout():
    return html.Div(
        [
            dbc.Row(
                dbc.Col(
                    children = [
                        dcc.Tabs(
                            id ='seite1-tabs-interface',
                            value='seite1-tab-1-einleitung',
                            children=[
                                dcc.Tab(
                                    label='Einleitung',
                                    value='seite1-tab-1-einleitung',
                                    ),
                                dcc.Tab(
                                    label='Luft - Metal',
                                    value='seite1-tab-2-luft-metal'
                                ),
                                dcc.Tab(
                                    label='Luft - Glas',
                                    value='seite1-tab-3-luft-glass'
                                ),
                                dcc.Tab(
                                    label='Luft - Wasser',
                                    value='seite1-tab-4-luft-wasser'
                                ),
                                dcc.Tab(
                                    label='Glas - Luft',
                                    value='seite1-tab-5-glass-luft'
                                )
                            ]),
                        html.Div(id ='seite1-tabs-interface-content')
                    ],
                    width=8,
                    ),
                justify='center',
            ),

        ],
        className = 'container')



def plot_arc(figure, center, radius, start_angle, end_angle, color, name):
    phi = np.linspace(start_angle, end_angle, 100)
    r = np.ones(phi.shape)*radius
    x = r*np.cos(phi) + center[0]
    y = r*np.sin(phi) + center[1]

    figure.add_trace(go.Scatter(x=x, y=y,
                                mode='lines',
                                name=name + " {:.0f}".format(np.degrees(end_angle-start_angle)),
                                line=dict(color='rgba({}, {})'.format(color, 1.0), width=10., dash='dot'),
                                showlegend=False,
                                ))


@callback(Output('seite1-tabs-interface-content', 'children'),
              Input('seite1-tabs-interface', 'value'))
def render_content_page1(tab):
    #print("displaying tab: {}".format(tab))
    if tab == 'seite1-tab-1-einleitung':
        return html.Div(
                    children=[
                        html.H4(children='Was macht einen Spiegel?'),
                        html.P('Wir nutzen alle täglich Spiegel um unser Aussehen zu kontrollieren. '+
                                'Andererseits, kennt man den Fall das irgendwas (z.B. Wasser) viel Sonnenlicht ' +
                                'reflektiert und uns blendet. Offensichtlich kann die Reflexion von Licht manchmal ' +
                                'hilfreich und manchmal nervig sein.'),
                        html.P('Jetzt untersuchen wir, in welchen Fällen welche Materialien für Spiegel geeignet sind.'),
                        html.P('Frage zu dieser Aufgabe:'),
                        html.P(
                            html.Ol(
                                children =[
                                    html.Li('Ein alltäglicher Spiegel besteht meistens aus einer Glasscheibe mit einer dünnen Schicht von Metall. Warum ist das eine gute Wahl?'),
                                    html.Li('Wäre ein Spiegel, der nur aus Glas besteht, gut um unser Aussehen zu kontrollieren?'),
                                    html.Li('Wenn man zwei Spiegeln parallel gegenüber voneinander stellt, kann das reflektiere '+
                                            'Licht zwischen den zwei Spiegeln hin und her laufen. Angenommen der Einfallswinkel kann '+
                                            'beliebig ausgesucht werden, welche der vier verschiedenen Fälle in dieser Aufgabe würde man '+
                                            'nehmen, damit das Licht ohne Verluste immer wieder hin und her läuft?'),
                                ]
                            )
                        )
                    ]
                )
    elif tab == 'seite1-tab-2-luft-metal':
        return html.Div(
                    title='Einfallswinkel anpassen',
                    children=[
                        html.P('Hier kannst du den Einfallswinkel von Licht (grüne Linie) ändern. '+
                                'Das Licht trifft die Grenzfläche zwischen Luft und Metall und wird '+
                                'reflektiert (lila Linie). '),
                        html.P('Es wird nicht immer das gesamte Licht reflektiert, sondern ein Teil kann auch '+
                                'transmittiert („durchgelassen“) und vom Material absorbiert („aufgenommen“) werden. '+
                                'Wie groß welcher Anteil ist, wird dir als Prozentzahl angezeigt. Das hängt von '+
                                'den Materialien aber auch vom Einfallswinkel ab.'),
                        html.P('Schau mal wie viel Licht bei kleinen Winkeln reflektiert wird, und wie viel '+
                                'Licht bei großen Winkeln reflektiert wird. Wird die Menge an reflektiertem '+
                                'Licht vom Einfallswinkel stark beeinflusst?'),
                        html.H4(children='Einfallswinkel',
                                 style={'text-align': 'Left'}),
                        dcc.Slider(
                            id ='seite1-inc_angle1',
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
                                            id ='reflection_report1',
                                            disabled=True,
                                            children=""
                                        ),
                                    ]
                                ),
                                dbc.Col(
                                    children = [
                                        dbc.Button(
                                            id ='transmission_report1',
                                            disabled=True,
                                            children=""
                                        ),
                                    ]
                                ),
                                dbc.Col(
                                    children = [
                                        dbc.Button(
                                            id ='absorption_report1',
                                            disabled=True,
                                            children="",
                                        )
                                    ]
                                )
                            ],
                            style = {'marginTop':10, 'marginBottom':10},
                            justify='evenly'
                        ),
                        dcc.Graph(id = 'air_metal_interface',
                                 style={'width':800, 'height':800}),
                    ])
    elif tab == 'seite1-tab-3-luft-glass':
        return html.Div(
                    title='Einfallswinkel anpassen',
                    children=[
                        html.P('Hier kannst du den Einfallswinkel von Licht (grüne Linie) ändern. '+
                                'Das Licht trifft die Grenzfläche zwischen Luft und Glas und wird '+
                                'reflektiert (lila Linie). Gleichzeitig wird ein Teil davon durch das '+
                                'Glas transmittiert (orangene Linie). '),
                        html.P('Das transmittierte Licht tritt unter einem bestimmten Winkel in das Glas ein, '+
                                'der zum Lot auf der Glasseite gemessen wird. Dieser wird auch „Brechungswinkel“ genannt. '+
                                'Die Änderung vom Winkel zum Lot, wenn man von einem transparenten Material zu '+
                                'einem anderen geht, heißt Brechung. '),
                        html.P('Wie stark das Licht gebrochen wird, hängt von dem „Brechungsindex“ der Materialien an '+
                                'der Grenzfläche ab. Wenn Licht von einem Material mit einem kleineren Brechungsindex in '+
                                'ein Material mit einem größeren Brechungsindex geht, dann ist der Brechungswinkel kleiner '+
                                'als der Einfallswinkel.'),
                        html.P('Luft hat ein Brechungsindex von 1.0 und Glas hat ein Brechungsindex von 1.5. Wasser z.B., '+
                                'hat einen Brechungsindex von nur 1.33, und das Licht wird deswegen schwächer gebrochen '+
                                '(d.h. der Brechungswinkel ist größer).'),
                        html.H4(className='app-controls-name',
                                 children='Einfallswinkel',
                                 style={'text-align': 'Left'}),
                        dcc.Slider(
                            id ='seite1-inc_angle2',
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
                                            id ='reflection_report2',
                                            disabled=True,
                                            children=""
                                        ),
                                    ]
                                ),
                                dbc.Col(
                                    children = [
                                        dbc.Button(
                                            id ='transmission_report2',
                                            disabled=True,
                                            children=""
                                        ),
                                    ]
                                ),
                                dbc.Col(
                                    children = [
                                        dbc.Button(
                                            id ='absorption_report2',
                                            disabled=True,
                                            children="",
                                        )
                                    ]
                                ),
                                dbc.Col(
                                    children = [
                                        dbc.Button(
                                            id ='angle_report2',
                                            disabled=True,
                                            children="",
                                        )
                                    ]
                                )
                            ],
                            style = {'marginTop':10, 'marginBottom':10},
                            justify='evenly'
                        ),
                        dcc.Graph(id = 'air_glass_interface',
                                  style={'width':800, 'height':800}),
                    ])
    elif tab == 'seite1-tab-4-luft-wasser':
        return html.Div(
                    title='Einfallswinkel anpassen',
                    children=[
                        html.P('Hier kannst du den Einfallswinkel von Licht (grüne Linie) ändern. '+
                                'Das Licht trifft die Grenzfläche zwischen Luft und Glas und wird '+
                                'reflektiert (lila Linie). Gleichzeitig wird ein Teil davon durch das '+
                                'Glas transmittiert (orangene Linie). '),
                        html.P('Das transmittierte Licht tritt unter einem bestimmten Winkel in das Glas ein, '+
                                'der zum Lot auf der Glasseite gemessen wird. Dieser wird auch „Brechungswinkel“ genannt. '+
                                'Die Änderung vom Winkel zum Lot, wenn man von einem transparenten Material zu '+
                                'einem anderen geht, heißt Brechung. '),
                        html.P('Wie stark das Licht gebrochen wird, hängt von dem „Brechungsindex“ der Materialien an '+
                                'der Grenzfläche ab. Wenn Licht von einem Material mit einem kleineren Brechungsindex in '+
                                'ein Material mit einem größeren Brechungsindex geht, dann ist der Brechungswinkel kleiner '+
                                'als der Einfallswinkel.'),
                        html.P('Luft hat ein Brechungsindex von 1.0 und Glas hat ein Brechungsindex von 1.5. Wasser z.B., '+
                                'hat einen Brechungsindex von nur 1.33, und das Licht wird deswegen schwächer gebrochen '+
                                '(d.h. der Brechungswinkel ist größer).'),
                        html.H4(className='app-controls-name',
                                 children='Einfallswinkel',
                                 style={'text-align': 'Left'}),
                        dcc.Slider(
                            id ='seite1-inc_angle4',
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
                                            id ='reflection_report4',
                                            disabled=True,
                                            children=""
                                        ),
                                    ]
                                ),
                                dbc.Col(
                                    children = [
                                        dbc.Button(
                                            id ='transmission_report4',
                                            disabled=True,
                                            children=""
                                        ),
                                    ]
                                ),
                                dbc.Col(
                                    children = [
                                        dbc.Button(
                                            id ='absorption_report4',
                                            disabled=True,
                                            children="",
                                        )
                                    ]
                                ),
                                dbc.Col(
                                    children = [
                                        dbc.Button(
                                            id ='angle_report4',
                                            disabled=True,
                                            children="",
                                        )
                                    ]
                                )
                            ],
                            style = {'marginTop':10, 'marginBottom':10},
                            justify='evenly'
                        ),
                        dcc.Graph(id = 'air_water_interface',
                                  style={'width':800, 'height':800}),
                    ])
    elif tab == 'seite1-tab-5-glass-luft':
        return html.Div(
                    title='Einfallswinkel anpassen',
                    children=[
                        html.P('Hier kannst du den Einfallswinkel von Licht (grüne Linie) ändern. '+
                                'Das Licht trifft die Grenzfläche zwischen Luft und Glas und wird '+
                                'reflektiert (lila Linie). Gleichzeitig wird ein Teil davon durch das '+
                                'Glas transmittiert (orangene Linie).'),
                        html.P('Das transmittierte Licht tritt unter einem bestimmten Winkel in das Glas ein, '+
                                'der zum Lot auf der Glasseite gemessen wird. Dieser wird auch „Brechungswinkel“ genannt. '+
                                'Die Änderung vom Winkel zum Lot, wenn man von einem transparenten Material zu '+
                                'einem anderen geht, heißt Brechung. '),
                        html.P('Hier gehen wir von einem Material mit einem höheren Brechungsindex zu einem mit kleineren Brechungsindex. Deswegen ist der Brechungswinkel sogar großer als den Einfallswinkel.'),
                        html.P('Wenn der Einfallswinkel über einem bestimmten Wert geht, dann wird das ganze Licht reflektiert. '+
                                'Das wird auch „Totalreflexion“ genannt.'),
                        html.H4(className='app-controls-name',
                                 children='Einfallswinkel',
                                 style={'text-align': 'Left'}),
                        dcc.Slider(
                            id ='seite1-inc_angle3',
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
                                            id ='reflection_report3',
                                            disabled=True,
                                            children=""
                                        ),
                                    ]
                                ),
                                dbc.Col(
                                    children = [
                                        dbc.Button(
                                            id ='transmission_report3',
                                            disabled=True,
                                            children=""
                                        ),
                                    ]
                                ),
                                dbc.Col(
                                    children = [
                                        dbc.Button(
                                            id ='absorption_report3',
                                            disabled=True,
                                            children="",
                                        )
                                    ]
                                ),
                                dbc.Col(
                                    children = [
                                        dbc.Button(
                                            id ='angle_report3',
                                            disabled=True,
                                            children="",
                                        )
                                    ]
                                )
                            ],
                            style = {'marginTop':10, 'marginBottom':10},
                            justify='evenly'
                        ),
                        dcc.Graph(id = 'glass_air_interface',
                                  style={'width':800, 'height':800}),
                    ])
    else:
        raise ValueError("Unknown tab value: " + tab)


@callback(Output(component_id ='air_metal_interface', component_property= 'figure'),
              Output(component_id ='reflection_report1', component_property= 'children'),
              Output(component_id ='transmission_report1', component_property= 'children'),
              Output(component_id ='absorption_report1', component_property= 'children'),
              [Input(component_id ='seite1-inc_angle1', component_property= 'value')])
def graph1_update(inc_angle):
    #print("graph update with inc angle: {}".format(inc_angle))
    #inc_angle = 45.
    if np.isclose(inc_angle,90.0):
        inc_angle = 89.0

    fig, r,t,a, t_angle = interface_graph(inc_angle, 1., 0.1+3j*1., '#ffffff', '#ebebeb')
    reflection_text = 'Reflection {:.0f}%'.format(abs(r)*100.)
    transmission_text = 'Transmission {:.0f}%'.format(abs(t)*100.)
    absorption_text = 'Absorption {:.0f}%'.format(abs(a)*100.)
    #print("returning data: {}, {}, {}, {}".format(fig, reflection_text, transmission_text, absorption_text))
    return fig, reflection_text, transmission_text, absorption_text

@callback(Output(component_id ='air_glass_interface', component_property= 'figure'),
              Output(component_id ='reflection_report2', component_property= 'children'),
              Output(component_id ='transmission_report2', component_property= 'children'),
              Output(component_id ='absorption_report2', component_property= 'children'),
              Output(component_id ='angle_report2', component_property= 'children'),
              [Input(component_id ='seite1-inc_angle2', component_property= 'value')])
def graph2_update(inc_angle):
    #inc_angle = 45.
    if np.isclose(inc_angle,90.0):
        inc_angle = 89.0

    fig, r,t,a, t_angle = interface_graph(inc_angle, 1., 1.5, '#ffffff', '#c5f5f6')
    reflection_text = 'Reflection {:.0f}%'.format(abs(r)*100.)
    transmission_text = 'Transmission {:.0f}%'.format(abs(t)*100.)
    absorption_text = 'Absorption {:.0f}%'.format(abs(a)*100.)
    return fig, reflection_text, transmission_text, absorption_text, "gebrochene Winkel {:.1f}°".format(t_angle)

@callback(Output(component_id ='air_water_interface', component_property= 'figure'),
              Output(component_id ='reflection_report4', component_property= 'children'),
              Output(component_id ='transmission_report4', component_property= 'children'),
              Output(component_id ='absorption_report4', component_property= 'children'),
              Output(component_id ='angle_report4', component_property= 'children'),
              [Input(component_id ='seite1-inc_angle4', component_property= 'value')])
def graph2_update(inc_angle):
    #inc_angle = 45.
    if np.isclose(inc_angle,90.0):
        inc_angle = 89.0

    fig, r,t,a, t_angle = interface_graph(inc_angle, 1., 1.33, '#ffffff', '#4d73fa')
    reflection_text = 'Reflection {:.0f}%'.format(abs(r)*100.)
    transmission_text = 'Transmission {:.0f}%'.format(abs(t)*100.)
    absorption_text = 'Absorption {:.0f}%'.format(abs(a)*100.)
    return fig, reflection_text, transmission_text, absorption_text, "gebrochene Winkel {:.1f}°".format(t_angle)


@callback(Output(component_id ='glass_air_interface', component_property= 'figure'),
              Output(component_id ='reflection_report3', component_property= 'children'),
              Output(component_id ='transmission_report3', component_property= 'children'),
              Output(component_id ='absorption_report3', component_property= 'children'),
              Output(component_id ='angle_report3', component_property= 'children'),
              [Input(component_id ='seite1-inc_angle3', component_property= 'value')])
def graph3_update(inc_angle):
    #inc_angle = 45.
    if np.isclose(inc_angle,90.0):
        inc_angle = 89.0

    fig, r,t,a, t_angle= interface_graph(inc_angle, 1.5, 1., '#c5f5f6', '#ffffff')
    reflection_text = 'Reflection {:.0f}%'.format(abs(r)*100.)
    transmission_text = 'Transmission {:.0f}%'.format(abs(t)*100.)
    absorption_text = 'Absorption {:.0f}%'.format(abs(a)*100.)
    return fig, reflection_text, transmission_text, absorption_text, "gebrochene Winkel {:.1f}°".format(t_angle)


def interface_graph(inc_angle, n_inc, n_trans, color_a, color_b):
    #n_inc = 1.
    #n_trans = 1.5
    inc_angle = np.radians(inc_angle)
    trans_angle = snell(n_inc, inc_angle, n_trans)
    if trans_angle > np.pi*0.5:
        trans_angle = np.pi*0.5
    r_s = fresnel_r_s(n_inc, inc_angle, n_trans, trans_angle)
    r_p = fresnel_r_p(n_inc, inc_angle, n_trans, trans_angle)

    t_s = fresnel_t_s(n_inc, inc_angle, n_trans, trans_angle)
    t_p = fresnel_t_p(n_inc, inc_angle, n_trans, trans_angle)

    R = (np.abs(r_s)**2 + np.abs(r_p)**2)*0.5
    R = np.round(R, 5)

    #inc_angle = np.radians(inc_angle)
    #trans_angle = np.radians(trans_angle)

    T = (np.abs(t_s)**2 + np.abs(t_p)**2)*0.5* np.real(n_trans*np.cos(trans_angle)/(n_inc*np.cos(inc_angle)))
    if np.imag(n_trans)>0.:
        T = 0.
    T = np.round(T, 5)
    center_x = 0.
    center_y = 0.
    trans_angle = np.real(trans_angle)

    left_x = -np.cos(inc_angle)*2
    left_y_lower = -np.sin(inc_angle)*2
    left_y_upper = np.sin(inc_angle)*2

    right_x = np.cos(trans_angle)*2
    right_y = np.sin(trans_angle)*2

    x_inc = [left_x, center_x]
    y_inc = [left_y_lower, center_y]

    x_ref = [center_x, left_x]
    y_ref = [center_y, left_y_upper]

    x_trn = [center_x, right_x]
    y_trn = [center_y, right_y]

    color1 = make_color(127, 201, 127)
    color2 = make_color(190,174,212)
    color3 = make_color(253,192,134)
    alpha1 = 1.
    alpha2 = R
    alpha3 = T

    fig = go.Figure()
    fig.add_shape(type="rect",
        x0=-2, y0=-2, x1=0, y1=2,
        line=dict(
            color=color_a,
            width=0,
        ),
        layer="below",
        fillcolor=color_a,
    )

    fig.add_shape(type="rect",
        x0=0, y0=-2, x1=2, y1=2,
        line=dict(
            color=color_b,
            width=0,
        ),
        layer="below",
        fillcolor=color_b,
    )

    fig.add_trace(go.Scatter(x=x_inc, y=y_inc,
                        mode='lines',
                         line=dict(color='rgba({}, {})'.format(color1, alpha1),
                                  width=10.),
                                  showlegend=False,
                        name='Incident'))

    fig.add_trace(go.Scatter(x=x_ref, y=y_ref,
                        mode='lines',
                             line=dict(color='rgba({}, {})'.format(color2, alpha2),
                                       width=10.),
                                       showlegend=False,
                        name='Reflected: {:.2f}%'.format(alpha2*100)))
    if np.imag(n_trans) == 0:
        fig.add_trace(go.Scatter(x=x_trn, y=y_trn,
                            mode='lines',
                             line=dict(color='rgba({}, {})'.format(color3, alpha3),
                                  width=10.),
                            showlegend=False,
                            name='Transmitted: {:.2f}%'.format(alpha3*100)))

    fig.add_shape(type='line',
                    yref="y",
                    xref="x",
                    x0=0.,
                    y0=-2.,
                    x1=0.,
                    y1=2.,
                    line=dict(color='black', width=3))

    fig.add_shape(type='line',
                    yref="y",
                    xref="x",
                    x0=-2.,
                    y0=0.,
                    x1=2.,
                    y1=0.,
                    line=dict(color='black', width=3, dash='dash'))
    if np.isclose(np.real(n_inc), 1.0):
        index_text = "Brechungsindex Luft = 1."
    elif np.isclose(np.real(n_inc), 1.5):
        index_text = "Brechungsindex Glas = 1.5"
    else:
        index_text = None
    if index_text is not None:
        fig.add_annotation(x=-1.2, y=1.8,
                text=index_text,
                font=dict(
                    family="Helvetica",
                    size=20,
                ),
                align="left",
                showarrow=False)
    if np.isclose(np.real(n_trans), 1.0):
        index_text = "Brechungsindex Luft = 1."
    elif np.isclose(np.real(n_trans), 1.5):
        index_text = "Brechungsindex Glas = 1.5"
    elif np.isclose(np.real(n_trans), 0.1):
        index_text = "Metall"
    elif np.isclose(np.real(n_trans), 1.33):
        index_text = "Brechungsindex Wasser = 1.33"
    else:
        index_text = None
    if index_text is not None:
        fig.add_annotation(x=1.0, y=1.8,
                text=index_text,
                font=dict(
                    family="Helvetica",
                    size=20,
                ),
                align="left",
                showarrow=False)
    plot_arc(fig, (0,0), 0.5, np.pi, np.pi+inc_angle, color1, "Angle Inc.")
    plot_arc(fig, (0,0), 0.5, np.pi-inc_angle, np.pi, color2, "Ref.")
    if np.imag(n_trans) == 0.:
        plot_arc(fig, (0,0), 0.5, 0., np.real(trans_angle), color3, "Angle Trans.")

    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False, plot_bgcolor='white',
                     xaxis_showticklabels=False, yaxis_showticklabels=False)

    fig.update_xaxes(range=[-2., 2.], autorange=False)
    fig.update_yaxes(range=[-2., 2.], autorange=False)
    return fig, R, T, 1-R-T, np.degrees(trans_angle)
