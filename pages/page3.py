import dash
from dash import html
from dash import dcc
from dash import callback

import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import plotly.graph_objects as go
import plotly.express as px

import numpy as np
#from scipy import constants
import scipy.signal
from fibre.optics import *
from .utils import make_color

def layout():
    return html.Div(
        [
            dbc.Row(
                dbc.Col(
                    children = [
                        dcc.Tabs(
                            id='seite3-tabs-interface',
                            value='seite3-tab-1-einleitung',
                            children=[
                                dcc.Tab(
                                    label='Einleitung',
                                    value='seite3-tab-1-einleitung',
                                    ),
                                dcc.Tab(
                                    label='Wellen',
                                    value='seite3-tab-5-wellen',
                                    ),
                                dcc.Tab(
                                    label='Signale in Wellen',
                                    value='seite3-tab-2-amplitude_modulation'
                                ),
                                dcc.Tab(
                                    label='Digitale Signale',
                                    value='seite3-tab-3-digital_data'
                                ),
                                dcc.Tab(
                                    label='Digitale Nachrichten',
                                    value='seite3-tab-4-digital_messages'
                                ),
                            ]),
                        html.Div(id='seite3-tabs-interface-content')
                    ],
                    width=8,
                    ),
                justify='center',
            ),

        ],
        className = 'container')


word_input = dbc.Row(
                [
                    dbc.Col(
                        dcc.Input(
                            id='letter_input1',
                            placeholder="h",
                            maxLength =1,
                            size =1,
                            type='text',
                            className='form-control',
                        ),
                        width=2),
                    dbc.Col(
                        dcc.Input(
                            id='letter_input2',
                            placeholder="a",
                            maxLength =1,
                            size =1,
                            type='text',
                            className='form-control',
                        ),
                        width=2),
                    dbc.Col(
                        dcc.Input(
                            id='letter_input3',
                            placeholder="l",
                            maxLength =1,
                            size =1,
                            type='text',
                            className='form-control',
                            ),
                        width=2),
                    dbc.Col(
                        dcc.Input(
                            id='letter_input4',
                            placeholder="l",
                            maxLength =1,
                            size =1,
                            type='text',
                            className='form-control',
                            ),
                        width=2),
                    dbc.Col(
                        dcc.Input(
                            id='letter_input5',
                            placeholder="o",
                            maxLength =1,
                            size =1,
                            type='text',
                            className='form-control',
                        ),
                        width=2),
                ],
                justify='center'
            )

binary_input = dbc.Row(
                [
                    dbc.Col(
                        dbc.ButtonGroup(
                            [dbc.Button("000000", disabled=True, id='binary_input1'),
                             dbc.Button("000000", disabled=True, id='binary_input2'),
                             dbc.Button("000000", disabled=True, id='binary_input3'),
                             dbc.Button("000000", disabled=True, id='binary_input4'),
                             dbc.Button("000000", disabled=True, id='binary_input5'),
                             ],
                            size="md",
                            className="btn-secondary",
                        ),
                        width=9),
                ],
                style = {'marginTop':40, 'marginBottom':40},
                justify='center'
            )

binary_output = dbc.Row(
                [
                    dbc.Col(
                        dbc.ButtonGroup(
                            [dbc.Button("000000", disabled=True, id='binary_output1'),
                             dbc.Button("000000", disabled=True, id='binary_output2'),
                             dbc.Button("000000", disabled=True, id='binary_output3'),
                             dbc.Button("000000", disabled=True, id='binary_output4'),
                             dbc.Button("000000", disabled=True, id='binary_output5'),
                             ],
                            size="md",
                            className="btn-secondary",
                        ),
                        width=9),
                ],
                style = {'marginTop':40, 'marginBottom':40},
                justify='center'
            )

word_output = dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            id='letter_output1',
                            children='h',
                            style={'font-size':'large'},
                            className='badge bg-primary',
                        ),
                        width=2),
                    dbc.Col(
                        html.Div(
                            id='letter_output2',
                            children='a',
                            style={'font-size':'large'},
                            className='badge bg-primary',
                        ),
                        width=2),
                    dbc.Col(
                        html.Div(
                            id='letter_output3',
                            children='l',
                            style={'font-size':'large'},
                            className='badge bg-primary',
                        ),
                        width=2),
                    dbc.Col(
                        html.Div(
                            id='letter_output4',
                            children='l',
                            style={'font-size':'large'},
                            className='badge bg-primary',
                        ),
                        width=2),
                    dbc.Col(
                        html.Div(
                            id='letter_output5',
                            children='o',
                            style={'font-size':'large'},
                            className='badge bg-primary',
                        ),
                        width=2),
                ],
                justify='center'
            )

message_input = dbc.Row(
                [
                    dbc.Col(
                        dbc.Accordion(
                            [
                                dbc.AccordionItem(
                                    dcc.Textarea(
                                        id='message_input1',
                                        value = "",
                                        placeholder="Deine Nachricht",
                                        maxLength =500,
                                        #size =60,
                                        #type='text',
                                        className='form-control',
                                        rows=5
                                    ),
                                    title="Nachricht"
                                ),
                            ],
                            start_collapsed=True,
                        ),
                        width=12),
                ])

message_output = dbc.Row(
                [
                    dbc.Col(
                        children =[
                            html.H4("Deine Nachricht"),
                            html.Div(
                                id='message_output1',
                                children="",
                                style={'font-size':'large'}
                            ),
                        ],
                        width=12,
                        style={'marginBottom':100},
                    ),

                ])


@callback(Output('seite3-tabs-interface-content', 'children'),
              Input('seite3-tabs-interface', 'value'))
def render_content_page3(tab):
    if tab == 'seite3-tab-1-einleitung':
        return html.Div(
                    children=[
                        html.H4(children='Signale in Licht'),
                        html.P('Jetzt wissen wir, wie wir einen Lichtstrahl ans Ziel bringen können. '+
                                'Aber Licht alleine bringt uns nicht so weit. Wir müssen auch Information '+
                                'schicken können, wenn wir das Internet vor Ort bringen wollen. '),
                        html.P('Frage zu dieser Aufgabe:'),
                        html.P(
                            html.Ol(
                                children =[
                                    html.Li('Wie muss das Verhältnis von Modulierung zu Rauschen sein, damit das Signal gut ankommt?'),
                                    html.Li('Was ist ein digitales Signal?'),
                                    html.Li('Wenn es Rauschen in einem digitalen Signal gibt, warum kommt das falsche Ergebnis am Zielort an?'),
                                ]
                            )
                        )

                    ]
                )
    elif tab == 'seite3-tab-5-wellen':
        return html.Div(
                    children=[
                        html.P('Wusstest du, das Licht eigentlich eine Welle ist? Wir bilden Licht oft als einen Strahl ab, '+
                                'aber dieser Strahl besteht aus einem elektrischen Feld, das hin und her schwingt.'),
                        html.P('Das Signal von der Lichtwelle (Y-Achse) schwingt mit der Zeit (X-Achse).'+
                                ' Wir sagen, dass das Signal mit einer Frequenz schwingt. Je hoher die Frequenz '+
                                'desto öfter schwingt das Signal innerhalb einer Sekunde. Wie hoch und tief die Welle '+
                                'an den Spitzen kommt nennen wir die Amplitude.'),
                        html.H4(children='Welle Frequenz',
                                 style = {'textAlign':'center', 'marginTop':40, 'marginBottom':40}),
                        dcc.Slider(min=1, max=20., step=1,
                                  value = 10,
                                  marks=None,
                                  tooltip={"placement": "bottom", "always_visible": True},
                                  id = 'wave_frequency1',
                                  ),
                        html.H4(children = 'Welle Amplitude',
                                style = {'textAlign':'center', 'marginTop':40, 'marginBottom':40}),
                        dcc.Slider(min=0., max=1, step=0.1,
                                  value = 0.5,
                                  marks=None,
                                  tooltip={"placement": "bottom", "always_visible": True},
                                  id = 'wave_amplitude1',
                                  ),
                        html.Div(children=[
                            html.H4(children = "Lichtwelle",
                                    style = {'textAlign':'center', 'marginTop':30, 'marginBottom':5}),
                            dcc.Graph(id = 'light_wave1', style={'height':300}),
                        ])
                    ])
    elif tab == 'seite3-tab-2-amplitude_modulation':
        return html.Div(
                    children=[
                        html.P('Wie können wir die Information, die wir schicken wollen, in ein Signal einbauen, wenn das Signal ständig am Schwingen ist?'),
                        html.P('Eine Lösung ist, wir kombinieren zwei Lichtwellen mit unterschiedlichen Frequenzen. '+
                                'Die Welle mit höher Frequenz nennen wir den Träger. Der Träger wird mit dem Signal kombiniert, '+
                                'so dass die Amplitude vom Träger genau das Signal beschreibt.'),
                        html.P('Wir können das kombinierte Signal durch die Glasfaser schicken, und wenn es ankommt, '+
                                'können wir die Signale wieder trennen. So kann man z.B. Tonsignal durch eine Glasfaser schicken.'),
                        html.P('Man muss aufpassen, das nicht zu viel Rauschen in das kombinierte Signal reinkommt, '+
                                'sonst kann das Signal was man am Ende wieder rausbekommt völlig Quatsch sein!'),
                        html.H4(className='app-controls-name',
                                 children='Träger Frequenz',
                                 style = {'textAlign':'center', 'marginTop':40, 'marginBottom':40}),
                        dcc.Slider(min=10, max=100., step=10,
                                  value = 40,
                                  marks=None,
                                  tooltip={"placement": "bottom", "always_visible": True},
                                  id = 'carrier_frequency1',
                                  ),
                        html.H4(children = 'Signal Frequenz',
                                style = {'textAlign':'center', 'marginTop':40, 'marginBottom':40}),
                        dcc.Slider(min=1, max=15, step=1,
                                  value = 5,
                                  marks=None,
                                  tooltip={"placement": "bottom", "always_visible": True},
                                  id = 'signal_frequency1',
                                  ),
                        html.H4(children = 'Signal Amplitude (Modulierung)',
                                style = {'textAlign':'center', 'marginTop':40, 'marginBottom':40}),
                        dcc.Slider(min=0, max=1., step=0.1,
                                  value = 0.5,
                                  marks=None,
                                  tooltip={"placement": "bottom", "always_visible": True},
                                  id = 'modulation1',
                                  ),
                        html.H4(children = 'Rauschen',
                                style = {'textAlign':'center', 'marginTop':40, 'marginBottom':40}),
                        dcc.Slider(min=0, max=1., step=0.1,
                                  value = 0.0,
                                  marks=None,
                                  tooltip={"placement": "bottom", "always_visible": True},
                                  id = 'noise1',
                                  ),
                        html.Div(children=[
                            html.H4(children = "Trägerwelle",
                                    style = {'textAlign':'center', 'marginTop':30, 'marginBottom':5}),
                            dcc.Graph(id = 'carrier_wave1', style={'height':150}),
                            html.H4(children = "Signalwelle",
                                    style = {'textAlign':'center', 'marginTop':30, 'marginBottom':5}),
                            dcc.Graph(id = 'signal_wave1', style={'height':200}),
                            html.H4(children = "Signal und Träger Kombiniert",
                                    style = {'textAlign':'center', 'marginTop':30, 'marginBottom':5}),
                            dcc.Graph(id = 'combined_wave1', style={'height':200}),
                            html.H4(children = 'Detektiertes Signal',
                                    style = {'textAlign':'center', 'marginTop':40, 'marginBottom':40}),
                            dcc.Graph(id = 'demodulated_wave1', style={'height':200, 'marginBottom':60}),
                        ],
                        )
                    ])
    elif tab == 'seite3-tab-3-digital_data':
        return html.Div(
                    children=[
                        html.P('Eine andere Lösung wie man ein Signal schicken kann, ist „ein“ und „aus“ '+
                               'Signale zu schicken. So funktioniert z.B. das Morsecode. Wenn man weiß, '+
                               'dass kurz, lang, kurz ein „A“ bedeutet (und was alle andere Kombinationen bedeuten) '+
                               'kann man ein Signal nur mit „ein“ und „aus“ schicken. Das wird ein digitales Signal genannt.'),
                        html.P('Wir benutzen hier auch eine Trägerwelle, aber jetzt springt die Amplitude vom Signal '+
                                'einfach zwischen eins und null. Damit können wir Informationen im Signal codieren.'),
                        html.P('Wenn wir die Signale wieder trennen, muss man nur entscheiden können, '+
                                'ob gerade eine null oder eins geschickt wird. Deswegen hat Rauschen einen '+
                                'kleineren Einfluss bei digitalen Signalen. '),
                        html.H4(className='app-controls-name',
                                 children='Träger Frequenz',
                                 style = {'textAlign':'center', 'marginTop':40, 'marginBottom':40}),
                        dcc.Slider(min=10, max=100., step=10,
                                  value = 40,
                                  marks=None,
                                  tooltip={"placement": "bottom", "always_visible": True},
                                  id = 'carrier_frequency2',
                                  ),
                        html.H4(children = 'Signal Breite',
                                style = {'textAlign':'center', 'marginTop':40, 'marginBottom':40}),
                        dcc.Slider(min=0.1, max=0.5, step=0.1,
                                  value = 0.3,
                                  marks=None,
                                  tooltip={"placement": "bottom", "always_visible": True},
                                  id = 'digital_signal_width',
                                  ),
                        html.H4(children = 'Signal Amplitude (Modulierung)',
                                style = {'textAlign':'center', 'marginTop':40, 'marginBottom':40}),
                        dcc.Slider(min=0, max=1., step=0.1,
                                  value = 0.5,
                                  marks=None,
                                  tooltip={"placement": "bottom", "always_visible": True},
                                  id = 'modulation2',
                                  ),
                        html.H4(children = 'Rauschen',
                                style = {'textAlign':'center', 'marginTop':40, 'marginBottom':40}),
                        dcc.Slider(min=0, max=1., step=0.1,
                                  value = 0.0,
                                  marks=None,
                                  tooltip={"placement": "bottom", "always_visible": True},
                                  id = 'noise2',
                                  ),
                        html.Div(children=[
                            html.H4(children = "Trägerwelle",
                                    style = {'textAlign':'center', 'marginTop':30, 'marginBottom':5}),
                            dcc.Graph(id = 'carrier_wave2', style={'height':150}),
                            html.H4(children = "Signal",
                                    style = {'textAlign':'center', 'marginTop':30, 'marginBottom':5}),
                            dcc.Graph(id = 'signal_wave2', style={'height':200}),
                            html.H4(children = 'Signal und Träger Kombiniert',
                                    style = {'textAlign':'center', 'marginTop':40, 'marginBottom':40}),
                            dcc.Graph(id = 'combined_wave2', style={'height':200}),
                            html.H4(children = 'Detektiertes Signal',
                                    style = {'textAlign':'center', 'marginTop':40, 'marginBottom':40}),
                            dcc.Graph(id = 'demodulated_wave2', style={'height':200, 'marginBottom':60}),
                        ])
                    ])
    elif tab == 'seite3-tab-4-digital_messages':
        return html.Div(
                    children=[
                        html.P('Jetzt können wir digitale Signale schicken. Wir brauchen noch ein System, '+
                                'um festzulegen was die Folge von Einsen und Nullen bedeuten. Hier zeigen wir '+
                                'wie fünf Buchstaben in eine Binärzahl umgewandelt werden. Eine Binärzahl ist '+
                                'eine Zahl, die nur aus null und eins besteht. Sehr praktisch für digitale Signale.'),
                        html.P('Wenn alles gut läuft und es kein Rauschen im Signal gibt, kommt genau die gleiche '+
                                'Reihenfolge an Nullen und Einsen am Zielort an. Aber wenn das Rauschen dazu führt, '+
                                'dass die manche Nullen und Einsen vertauscht werden, kommt ein völlig anderer Buchstabe raus.'),
                        html.H4(className='app-controls-name',
                                 children='Nachricht',
                                 style = {'textAlign':'center', 'marginTop':40, 'marginBottom':40}),
                        word_input,
                        html.H4(className='app-controls-name',
                                 children='Buchstaben als Binärzahl',
                                 style = {'textAlign':'center', 'marginTop':40, 'marginBottom':40}),
                        binary_input,
                        html.H4(children = 'Rauschen',
                                style = {'textAlign':'center', 'marginTop':40, 'marginBottom':40}),
                        dcc.Slider(min=0, max=1., step=0.1,
                                  value = 0.0,
                                  marks=None,
                                  tooltip={"placement": "bottom", "always_visible": True},
                                  id = 'noise3',
                                  ),
                        html.H4(className='app-controls-name',
                                 children='Angekommene Binärzahl',
                                 style = {'textAlign':'center', 'marginTop':40, 'marginBottom':40}),
                        binary_output,
                        html.H4(className='app-controls-name',
                                 children='Angekommene Nachricht',
                                 style = {'textAlign':'center', 'marginTop':40, 'marginBottom':40}),
                        word_output,
                        html.P('Schreib hier eine Nachricht und schaue Mal, mit wie viel Rauschen du die Nachricht noch lesen und verstehen kannst!',
                               style = {'textAlign':'left', 'marginTop':60, 'marginBottom':0}),
                        html.H4(className='app-controls-name',
                                 children='Längere Nachricht',
                                 style = {'textAlign':'center', 'marginTop':20, 'marginBottom':40}),
                        message_input,
                        html.H4(className='app-controls-name',
                                 children='Angekommene Nachricht',
                                 style = {'textAlign':'center', 'marginTop':40, 'marginBottom':40}),
                        message_output,
                    ])
    else:
        raise ValueError("Unknown tab value: " + tab)


def carrier_signal(frequency, time):
    return np.sin(2*np.pi*frequency*time)

def modulation_signal(frequency, time, modulation):
    phase = 0.
    signal = modulation*np.sin(2*np.pi*(frequency)*time+phase)
    return signal

def combine_signals(signal1, signal2):
    combined_signal = (1+signal2)*signal1
    return combined_signal

def combine_signals_digital(signal1, signal2):
    combined_signal = signal2*signal1
    return combined_signal

def add_noise(signal, noise_level):
    noise = np.random.normal(0, noise_level, signal.size).reshape(signal.shape)
    return signal+noise

def demodulate(combined_signal, carrier_frequency):
    combined_signal = np.abs(combined_signal)
    sos = scipy.signal.butter(10, carrier_frequency/2, 'lp', fs=1000, output='sos')
    filtered = scipy.signal.sosfilt(sos, combined_signal)
    return filtered

def model_func(model_inputs):
    carrier = carrier_signal(model_inputs[0], model_inputs[2])
    signal = modulation_signal(model_inputs[1], model_inputs[2], model_inputs[3])
    combined_signal = combine_signals(carrier, signal)
    return combined_signal

def error_func(x, model_inputs, exp_data):
    model_inputs[3] = x
    model_data = model_func(model_inputs)
    return exp_data-model_data

@callback(Output(component_id='light_wave1', component_property= 'figure'),
              [Input(component_id='wave_frequency1', component_property= 'value'),
               Input(component_id='wave_amplitude1', component_property= 'value'),
               ])

def page3_wave_graph_update(frequency, amplitude):
    t = np.linspace(0, 1., 1000, False)
    fig1, signal = plot_signal(frequency, t, amplitude)
    return fig1

@callback(Output(component_id='carrier_wave1', component_property= 'figure'),
              Output(component_id='signal_wave1', component_property= 'figure'),
              Output(component_id='combined_wave1', component_property= 'figure'),
              Output(component_id='demodulated_wave1', component_property= 'figure'),
              [Input(component_id='modulation1', component_property= 'value'),
               Input(component_id='noise1', component_property= 'value'),
               Input(component_id='carrier_frequency1', component_property= 'value'),
               Input(component_id='signal_frequency1', component_property= 'value')])

def page3_graph_update(modulation, noise, carrier_frequency, signal_frequency):
    t = np.linspace(0, 1., 1000, False)

    fig1, carrier = plot_carrier(carrier_frequency, t)
    fig2, signal = plot_signal(signal_frequency, t, modulation)
    fig3, fig4 = demodulate_signal(carrier_frequency, t, noise, signal, carrier)

    return fig1, fig2, fig3, fig4


@callback(Output(component_id='carrier_wave2', component_property= 'figure'),
              Output(component_id='signal_wave2', component_property= 'figure'),
              Output(component_id='combined_wave2', component_property= 'figure'),
              Output(component_id='demodulated_wave2', component_property= 'figure'),
              [Input(component_id='modulation2', component_property= 'value'),
               Input(component_id='noise2', component_property= 'value'),
               Input(component_id='carrier_frequency2', component_property= 'value'),
               Input(component_id='digital_signal_width', component_property= 'value')])

def page3_graph_update(modulation, noise, carrier_frequency, signal_width):
    t = np.linspace(0, 1., 1000, False)

    fig1, carrier = plot_carrier(carrier_frequency, t)
    fig2, signal = plot_digital_signal(t, modulation, signal_width)
    fig3, fig4 = demodulate_signal(carrier_frequency, t, noise, signal, carrier, digital=True)

    return fig1, fig2, fig3, fig4



@callback(Output(component_id='binary_input1', component_property= 'children'),
          Output(component_id='binary_input2', component_property= 'children'),
          Output(component_id='binary_input3', component_property= 'children'),
          Output(component_id='binary_input4', component_property= 'children'),
          Output(component_id='binary_input5', component_property= 'children'),
          Output(component_id='binary_output1', component_property= 'children'),
          Output(component_id='binary_output2', component_property= 'children'),
          Output(component_id='binary_output3', component_property= 'children'),
          Output(component_id='binary_output4', component_property= 'children'),
          Output(component_id='binary_output5', component_property= 'children'),
          Output(component_id='letter_output1', component_property= 'children'),
          Output(component_id='letter_output2', component_property= 'children'),
          Output(component_id='letter_output3', component_property= 'children'),
          Output(component_id='letter_output4', component_property= 'children'),
          Output(component_id='letter_output5', component_property= 'children'),
          Output(component_id='letter_output1', component_property= 'className'),
          Output(component_id='letter_output2', component_property= 'className'),
          Output(component_id='letter_output3', component_property= 'className'),
          Output(component_id='letter_output4', component_property= 'className'),
          Output(component_id='letter_output5', component_property= 'className'),
          Output(component_id='message_output1', component_property= 'children'),
        [Input(component_id='letter_input1', component_property= 'value'),
       Input(component_id='letter_input2', component_property= 'value'),
       Input(component_id='letter_input3', component_property= 'value'),
       Input(component_id='letter_input4', component_property= 'value'),
       Input(component_id='letter_input5', component_property= 'value'),
       Input(component_id='noise3', component_property= 'value'),
       Input(component_id='message_input1', component_property= 'value')])
def page3_binary_words_update(letter1, letter2, letter3, letter4, letter5, noise, message):
    #print("binary words update")
    #print("[{}],[{}],[{}],[{}],[{}],{},[{}]".format(letter1, letter2, letter3, letter4, letter5, noise, message))
    if letter1 is None or letter1 =="":
        letter1 = 'h'
    if letter2 is None or letter2 =="":
        letter2 = 'a'
    if letter3 is None or letter3 =="":
        letter3 = 'l'
    if letter4 is None or letter4 =="":
        letter4 = 'l'
    if letter5 is None or letter5 =="":
        letter5 = 'o'
    mystr = "".join((letter1, letter2, letter3, letter4, letter5))
    #print(mystr)
    binary_input = str_to_binary(mystr)

    binary_output = scramble(binary_input, noise)
    new_str = binary_to_str(binary_output)
    class_names = []
    for ii, letter in enumerate(new_str):
        if letter == mystr[ii]:
            class_names.append("badge bg-primary")
        else:
            class_names.append("badge bg-secondary")
    #print(*binary_input, *binary_output, *new_str)
    if message is not None:
        blanks = detect_blanks(message)
        binary_message = str_to_binary(message)
        binary_message = scramble(binary_message, noise, to_skip=blanks)
        output_message = "".join(binary_to_str(binary_message))
    else:
        output_message = ""
    return (*binary_input, *binary_output, *new_str, *class_names, output_message)

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
                     xaxis_showticklabels=True, yaxis_showticklabels=False)

    fig.update_xaxes(range=[0., 1.], autorange=False)
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10))
    fig.update_xaxes(title_text='Zeit (s)', title_font = {"size": 20})
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
                     xaxis_showticklabels=True, yaxis_showticklabels=False)
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10))
    #fig.update_xaxes(range=[-0.5, 15.5], autorange=False)
    fig.update_xaxes(range=[0., 1.], autorange=False)
    fig.update_yaxes(range=[-2.1, 2.1], autorange=False)
    fig.update_xaxes(title_text='Zeit (s)', title_font = {"size": 20})
    return fig, signal

def digital_signal(t, modulation, width):
    dsignal = np.zeros_like(t)
    dsignal[t>0.5-width*0.5] = modulation
    dsignal[t>0.5+width*0.5] = 0.
    return dsignal

def plot_digital_signal(t, modulation, width):
    signal = digital_signal(t, modulation, width)

    fig = go.Figure()
    color1 = make_color(190,174,212)
    alpha1 = 1.
    fig.add_trace(go.Scatter(x=t, y=signal,
                        mode='lines',
                         line=dict(color='rgba({}, {})'.format(color1, alpha1),
                                  width=2.),
                        name='Carrier'))

    fig.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, plot_bgcolor='white',
                     xaxis_showticklabels=True, yaxis_showticklabels=False)
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10))
    #fig.update_xaxes(range=[-0.5, 15.5], autorange=False)
    fig.update_xaxes(range=[0., 1.], autorange=False)
    fig.update_yaxes(range=[-0.5, 2.1], autorange=False)
    fig.update_xaxes(title_text='Zeit (s)', title_font = {"size": 20})
    return fig, signal

def demodulate(combined_signal, carrier_frequency):
    combined_signal = np.abs(combined_signal)
    sos = scipy.signal.butter(10, carrier_frequency-1, 'lp', fs=1000, output='sos')
    filtered = scipy.signal.sosfilt(sos, combined_signal)
    return filtered

def demodulate_signal(carrier_frequency, t,
                      noise, signal, carrier, digital=False):
    if digital:
        combined_signal = combine_signals_digital(carrier, signal)
    else:
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
    fig.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, plot_bgcolor='white',
                     xaxis_showticklabels=True, yaxis_showticklabels=False)
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10))
    fig.update_xaxes(range=[0., 1.], autorange=False)
    fig.update_xaxes(title_text='Zeit (s)', title_font = {"size": 20})
    if digital is False:
        fig.update_yaxes(range=[-3.1, 3.1], autorange=False)
    else:
        fig.update_yaxes(range=[-3.1, 3.1], autorange=False)
    demodulated_signal = demodulate(noisy_signal, carrier_frequency)

    fig2 = go.Figure()
    color1 = make_color(231,41,138)
    alpha1 = 1.0
    fig2.add_trace(go.Scatter(x=t, y=demodulated_signal,
                        mode='lines',
                         line=dict(color='rgba({}, {})'.format(color1, alpha1),
                                  width=2.),
                        name='Demodulated Signal'))
    fig2.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, plot_bgcolor='white',
                     xaxis_showticklabels=True, yaxis_showticklabels=False)
    fig2.update_layout(margin=dict(l=10, r=10, t=10, b=10))
    fig2.update_xaxes(range=[0., 1.], autorange=False)
    if digital is False:
        fig2.update_yaxes(range=[-2.1, 2.1], autorange=False)
    else:
        fig2.update_yaxes(range=[-0.5, 2.1], autorange=False)
    fig2.update_xaxes(title_text='Zeit (s)', title_font = {"size": 20})
    return fig, fig2

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
    model_inputs = [carrier_frequency, signal_frequency, t, 1.0]

    #res = scipy.optimize.least_squares(error_func, [1.0], args=(model_inputs, exp_data))
    #reconstructed_signal =  modulation_signal(signal_frequency, t, res['x'])
    reconstructed_signal =  modulation_signal(signal_frequency, t, modulation)

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


    #fig.update_yaxes(title_text='Value A')
    fig.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, plot_bgcolor='white',
                     xaxis_showticklabels=False, yaxis_showticklabels=False,
                     showlegend=False)
    fig.update_xaxes(range=[0., 10.], autorange=False)

    return fig, [modulation]


def str_to_binary(test_str):
    converted = list(f"{ord(i):08b}" for i in test_str)
    return converted

def binary_to_str(binary_text_list):
    decoded_letters = []
    for binary_text in binary_text_list:
        binary_as_int = int(binary_text, 2)
        byte_number = ( binary_as_int.bit_length() + 7 ) // 8
        plaintext_bytes_string = binary_as_int.to_bytes(byte_number, "big")
        unicodeTextString = plaintext_bytes_string.decode() # as UTF-8 standard
        #print(binary_as_int, byte_number, plaintext_bytes_string, unicodeTextString)
        decoded_letters.append(unicodeTextString)
    return "".join(decoded_letters)

def flip(letter):
    if letter == '0':
        return '1'
    elif letter == '1':
        return '0'

def detect_blanks(letters):
    is_blank = []
    for letter in letters:
        if letter == " ":
            is_blank.append(True)
        else:
            is_blank.append(False)
    return is_blank

def scramble(binary_text_list, noise, to_skip=None):
    scrambled_letters = []
    for ib, binary_text in enumerate(binary_text_list):
        if to_skip is not None:
            if to_skip[ib]:
                allow_scramble = False
            else:
                allow_scramble = True
        else:
            allow_scramble = True
        scrambled = ""

        for iletter, one_zero in enumerate(binary_text):
            if np.random.random() > 1-noise**4 and iletter > 4 and allow_scramble:
                one_zero = flip(one_zero)
            scrambled += one_zero
        scrambled_letters.append(scrambled)
    return scrambled_letters
