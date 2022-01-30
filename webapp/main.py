import dash
from dash.dependencies import Input, Output, State
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import plotly.express as px

import tensorflow as tf 
import numpy as np
from tensorflow.keras.preprocessing import sequence
import re

#load model
model = tf.keras.models.load_model('model')

# Map for readable classnames
class_names = ["Negative", "Positive"]

# Get the word index from the dataset
word_index = tf.keras.datasets.imdb.get_word_index()

# Ensure that "special" words are mapped into human readable terms 
word_index = {k:(v+3) for k,v in word_index.items()}
word_index["<PAD>"] = 0
word_index["<START>"] = 1
word_index["<UNKNOWN>"] = 2
word_index["<UNUSED>"] = 3

# The length of reviews
review_length = 500

def predict(review):
  review = re.sub(r'[^A-Za-z0-9 ]+', ' ', review.strip())

  review_encoded = np.array([word_index[word] if (word.isalnum() and word in word_index and word_index[word]<10000) else 2 for word in review.split(" ")])
  review_padded = sequence.pad_sequences(review_encoded[None, :], maxlen = review_length)

  raw_prediction = model.predict(review_padded)[0][0]

  return raw_prediction

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], title="Movie Review Sentiment")
server = app.server

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
      if value:
        raw_prediction = predict(value)*2-1

        if raw_prediction<-.67:
          color_name = 'indianred'
        elif raw_prediction<-0.33:
          color_name = 'lightcoral'
        elif raw_prediction<0:
          color_name = 'lightsalmon'
        elif raw_prediction<0.33:
          color_name = 'darkturquoise'
        elif raw_prediction<0.66:
          color_name = 'deepskyblue'
        else:
          color_name = 'dodgerblue'

        fig = px.bar(x=[raw_prediction], y=[''], orientation='h', height=200, title="Review Sentiment (-1: very bad, 1: very good)")
        fig.update_yaxes(title ='', visible=True, showticklabels=False)
        fig.update_xaxes(title ='', visible=True, showticklabels=True, range=[-1, 1], showgrid=True, showline=True, 
                          ticks='outside', linewidth=0.5, linecolor='black')
        fig.update_traces(width=0.75, marker_color=color_name)
        fig.update_layout({
          'plot_bgcolor': 'rgba(0, 0, 0, 0)',
          })
        chart = dcc.Graph(figure=fig, className="mt-5",)

        return chart
      else:
        return "Please provide a review."

if __name__ == '__main__':
    app.run_server(debug=False)


