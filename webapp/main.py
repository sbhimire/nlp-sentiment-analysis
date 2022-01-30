import dash
from dash.dependencies import Input, Output, State
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], title="Movie Review Sentiment")

# make a reuseable navitem for the different examples
nav_item = dbc.NavItem(dbc.NavLink("GitHub", href="https://github.com/sbhimire"))

# this example that adds a logo to the navbar brand
logo = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src='/assets/logo.jpeg', height="50px")),
                        dbc.Col(dbc.NavbarBrand("Movie Review Sentiment", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="/",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler2", n_clicks=0),
            dbc.Collapse(
                dbc.Nav(
                    [nav_item],
                    className="ms-auto",
                    navbar=True,
                ),
                id="navbar-collapse2",
                navbar=True,
            ),
        ],
    ),
    color="dark",
    dark=True,
    className="mb-5",
)

jumbotron = html.Div(
    dbc.Container(
        [ html.P(
                "Natural Language Processing (NLP) model that predicts the overall sentiment of a movie review (positive or negative).",
                className="lead",
            ),
          dbc.Textarea(id="textarea-state-example", className="mb-3", placeholder="Type your own review here.",
          size='md', rows=8),
          dbc.Button('Run Model', color="dark" ,id='textarea-state-example-button', n_clicks=0),
          html.Div(id='textarea-state-example-output', style={'whiteSpace': 'pre-line'}),
        ],
        fluid=True,
        className="py-3",
    ),
    className="p-3 bg-light rounded-3",
)

row =  dbc.Row(
            [
                dbc.Col(html.Div(), md=3),
                dbc.Col(jumbotron, md=6),
                dbc.Col(html.Div(), md=3),
            ]
)

app.layout = html.Div([logo, row])

@app.callback(
    Output('textarea-state-example-output', 'children'),
    Input('textarea-state-example-button', 'n_clicks'),
    State('textarea-state-example', 'value')
)
def update_output(n_clicks, value):
    if n_clicks > 0:
        return 'You have entered: \n{}'.format(value)

if __name__ == '__main__':
    app.run_server(debug=True)

