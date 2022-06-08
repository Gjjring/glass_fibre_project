import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import plotly.graph_objects as go
import plotly.express as px

import numpy as np
from scipy import constants
import scipy.optimize


def make_color(r,g,b):
    color_str = "{}, {}, {}".format(r,g,b)
    return color_str

def carrier_signal(frequency, time):
    return np.sin(2*np.pi*frequency*time)

def modulation_signal(frequency, time, modulation):
    phase = 0.
    signal = modulation*np.sin(2*np.pi*(frequency)*time+phase)
    return signal

def combine_signals(signal1, signal2):
    combined_signal = (1+signal2)*signal1
    return combined_signal

def add_noise(signal, noise_level):
    noise = np.random.normal(0, noise_level, signal.size).reshape(signal.shape)
    return signal+noise

def model_func(model_inputs):
    carrier = carrier_signal(model_inputs[0], model_inputs[2])
    signal = modulation_signal(model_inputs[1], model_inputs[2], model_inputs[3])
    combined_signal = combine_signals(carrier, signal)
    return combined_signal

def error_func(x, model_inputs, exp_data):
    model_inputs[3] = x
    model_data = model_func(model_inputs)
    return exp_data-model_data

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


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

#df = px.data.stocks()

app.layout = html.Div(
    [
        dbc.Row(
            dbc.Col(children = [
                html.H1(id = 'H1',
                        children = 'Amplitude Modulation of Light Waves',
                        style = {'textAlign':'center', 'marginTop':40, 'marginBottom':40})],
                width="auto",
                style={"border":"0px black solid"}),
                justify='center'),
        dbc.Row(
            [
                dbc.Col(dbc.ListGroup([
                            dbc.ListGroupItem("Mirror Reflection"),
                            dbc.ListGroupItem("Air - Glass Reflection"),
                            dbc.ListGroupItem("Glass - Air Reflection "),
                            dbc.ListGroupItem("Glass Fibre"),
                        ])
                        ,width=2,style={"border":"0px black solid"}),
                dbc.Col(
                    html.Div(children=[
                        dcc.Graph(id = 'carrier_wave', style={'height':300}),
                        dcc.Graph(id = 'signal_wave', style={'height':300}),
                        dcc.Graph(id = 'combined_wave', style={'height':300}),
                            ]),
                    width=5,
                    style={"border":"0px black solid"}),
                    dbc.Col(
                        html.Div(children=[
                            html.H3(id = 'CarrierFrequencyHeader',
                                    children = 'Carrier Frequency',
                                    style = {'textAlign':'center', 'marginTop':40, 'marginBottom':40}),
                            dcc.Slider(min=0.1, max=2., step=0.1,
                                      value = 1.0,
                                      marks=None,
                                      tooltip={"placement": "bottom", "always_visible": True},
                                      id = 'carrier_frequency',
                                      ),
                            html.H3(id = 'SignalFrequencyHeader',
                                    children = 'Signal Frequency',
                                    style = {'textAlign':'center', 'marginTop':40, 'marginBottom':40}),
                            dcc.Slider(min=0.01, max=0.5, step=0.01,
                                      value = 0.1,
                                      marks=None,
                                      tooltip={"placement": "bottom", "always_visible": True},
                                      id = 'signal_frequency',
                                      ),
                            html.H3(id = 'ModulationHeader',
                                    children = 'Modulation',
                                    style = {'textAlign':'center', 'marginTop':40, 'marginBottom':40}),
                            dcc.Slider(min=0, max=1., step=0.1,
                                      value = 0.5,
                                      marks=None,
                                      tooltip={"placement": "bottom", "always_visible": True},
                                      id = 'modulation',
                                      ),
                            html.H3(id = 'NoiseHeader',
                                    children = 'Noise',
                                    style = {'textAlign':'center', 'marginTop':40, 'marginBottom':40}),
                            dcc.Slider(min=0, max=1., step=0.1,
                                      value = 0.0,
                                      marks=None,
                                      tooltip={"placement": "bottom", "always_visible": True},
                                      id = 'noise',
                                      )
                                ]),
                        width=3,
                        style={"border":"0px black solid"}),
            ],
        justify='center'
        ),
    ],
    className = 'container')

@app.callback(Output(component_id='carrier_wave', component_property= 'figure'),
              Output(component_id='signal_wave', component_property= 'figure'),
              Output(component_id='combined_wave', component_property= 'figure'),
              [Input(component_id='modulation', component_property= 'value'),
               Input(component_id='noise', component_property= 'value'),
               Input(component_id='carrier_frequency', component_property= 'value'),
               Input(component_id='signal_frequency', component_property= 'value')])

def graph_update(modulation, noise, carrier_frequency, signal_frequency):
    t_step = 1e-3
    t = np.arange   (0, 10+t_step, t_step)

    fig1, carrier = plot_carrier(carrier_frequency, t)
    fig2, signal = plot_signal(signal_frequency, t, modulation)
    fig3 = determine_signal(carrier_frequency, signal_frequency, t, modulation, noise, signal, carrier)
    return fig1, fig2, fig3

def plot_carrier(frequency, t):
    carrier = carrier_signal(frequency, t)

    fig = go.Figure()
    color1 =  make_color(127, 201, 127)
    alpha1 = 1.
    fig.add_trace(go.Scatter(x=t, y=carrier,
                        mode='lines',
                         line=dict(color='rgba({}, {})'.format(color1, alpha1),
                                  width=2.),
                        name='Carrier'))

    fig.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, plot_bgcolor='white',
                     xaxis_showticklabels=False, yaxis_showticklabels=False)

    fig.update_xaxes(range=[0., 10.], autorange=False)
    #fig.update_yaxes(range=[-2., 2.], autorange=False)
    return fig, carrier

def plot_signal(frequency, t, modulation):
    signal = modulation_signal(frequency, t, modulation)

    fig = go.Figure()
    color1 = make_color(190,174,212)
    alpha1 = 1.
    fig.add_trace(go.Scatter(x=t, y=signal,
                        mode='lines',
                         line=dict(color='rgba({}, {})'.format(color1, alpha1),
                                  width=2.),
                        name='Carrier'))

    fig.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, plot_bgcolor='white',
                     xaxis_showticklabels=False, yaxis_showticklabels=False)

    #fig.update_xaxes(range=[-0.5, 15.5], autorange=False)
    fig.update_xaxes(range=[0., 10.], autorange=False)
    fig.update_yaxes(range=[-1.1, 1.1], autorange=False)
    return fig, signal

def determine_signal(carrier_frequency, signal_frequency, t,
                     modulation, noise, signal, carrier):

    combined_signal = combine_signals(carrier, signal)
    noisy_signal = add_noise(combined_signal, noise)


    fig = go.Figure()
    color1 = make_color(253,192,134)
    alpha1 = 1.0
    fig.add_trace(go.Scatter(x=t, y=noisy_signal,
                        mode='lines',
                         line=dict(color='rgba({}, {})'.format(color1, alpha1),
                                  width=2.),
                        name='Noisy Signal'))

    exp_data = noisy_signal
    model_inputs = [carrier_frequency, signal_frequency, t, 0.0]

    res = scipy.optimize.least_squares(error_func, [0.0], args=(model_inputs, exp_data))
    reconstructed_signal =  modulation_signal(signal_frequency, t, res['x'])

    fig.add_trace(go.Scatter(x=t, y=1+reconstructed_signal,
                        mode='lines',
                         line=dict(color='black',
                                  width=2.),
                        name=''))

    fig.add_trace(go.Scatter(x=t, y=-(1+reconstructed_signal),
                        mode='lines',
                         line=dict(color='black',
                                  width=2.),
                        name=''))


    fig.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, plot_bgcolor='white',
                     xaxis_showticklabels=False, yaxis_showticklabels=False,
                     showlegend=False)
    fig.update_xaxes(range=[0., 10.], autorange=False)

    return fig



if __name__ == '__main__':
    app.run_server()
