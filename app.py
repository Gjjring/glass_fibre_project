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
from pages import page1 , page2 , page3



app = dash.Dash(external_stylesheets=[dbc.themes.MORPH])




def navigation_bar():
    return dbc.Row(
            dbc.Col(children = [
                dbc.NavbarSimple(
                    children=[
                        dbc.NavItem(children=dbc.NavLink(id='curret_page_link', children="Aufgabe 1", href="/aufgabe1")),
                        dbc.DropdownMenu(id='other_links_menu',
                            children=[
                                dbc.DropdownMenuItem("Mehr Aufgaben", header=True),
                                dbc.DropdownMenuItem(id='other_link_1',children="Aufgabe 2", href="/aufgabe2"),
                                dbc.DropdownMenuItem(id='other_link_2',children="Aufgabe 3", href="/aufgabe3"),
                            ],
                            nav=True,
                            in_navbar=True,
                            label="Mehr",
                        ),
                    ],
                    brand="Mintoring",
                    brand_href="#",
                    color="primary",
                    dark=True,
                    brand_style= {'font-size': 'large'},
                    style={'margin-bottom':40, 'height':60},
                )
            ]),
            justify='center',
        )

app.layout = html.Div([
    # represents the browser address bar and doesn't render anything
    dcc.Location(id='url', refresh=False),
    navigation_bar(),
    # content will be rendered in this element
    html.Div(id='page-content')
])


@callback(Output('curret_page_link', 'children'),
              Output('curret_page_link', 'href'),
              Output('other_link_1', 'children'),
              Output('other_link_1', 'href'),
              Output('other_link_2', 'children'),
              Output('other_link_2', 'href'),
              [Input('url', 'pathname')])
def update_links(pathname):
    if pathname == '/' or pathname == '/aufgabe1':
        current_page = 'Aufgabe 1'
        current_href = '/aufgabe1'
        other_link_1 = 'Aufgabe 2'
        other_href_1 = '/aufgabe2'
        other_link_2 = 'Aufgabe 3'
        other_href_2 = '/aufgabe3'
    elif pathname == '/aufgabe2':
        current_page = 'Aufgabe 2'
        current_href = '/aufgabe2'
        other_link_1 = 'Aufgabe 1'
        other_href_1 = '/aufgabe1'
        other_link_2 = 'Aufgabe 3'
        other_href_2 = '/aufgabe3'
    elif pathname == '/aufgabe3':
        current_page = 'Aufgabe 3'
        current_href = '/aufgabe3'
        other_link_1 = 'Aufgabe 1'
        other_href_1 = '/aufgabe1'
        other_link_2 = 'Aufgabe 2'
        other_href_2 = '/aufgabe2'
    return current_page, current_href, other_link_1, other_href_1, other_link_2, other_href_2

def blank_page():
    return html.Div(
        [
            html.H1("Blank Page")
        ])

@callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    #print("displaying content for page: {}".format(pathname))
    if pathname == '/' or pathname == '/aufgabe1':
        return page1.layout()
    elif pathname == '/aufgabe2':
        return page2.layout()
    elif pathname == '/aufgabe3':
        return page3.layout()
    else:
        raise ValueError("unknown path: [{}]".format(pathname))



if __name__ == '__main__':
    app.run_server()
