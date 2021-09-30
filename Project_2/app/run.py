"""Copyright (c) 2021 Reza Dwi Utomo
This module runs Flask back-end and Plotly front-end.
"""
import sys
import json
import pandas as pd

import nltk

from flask import Flask
from flask import render_template, request

import plotly
from plotly.graph_objs import Bar

from sklearn.externals import joblib

from sqlalchemy import create_engine

# check if NLTK data already installed
nltk_data = ['corpora/stopwords', 'corpora/wordnet', 'tokenizers/punkt']
for datum in nltk_data:
    try:
        nltk.data.find(datum)
    except LookupError:
        nltk.download(datum.split('/')[-1])

sys.path.append("..") # get access from parent dir
from models.train_classifier import tokenize

# instantiate Flask
app = Flask(__name__)

# load data
engine = create_engine('sqlite:///../data/DisasterResponse.db')
df = pd.read_sql_table('message_category', engine)

# load model
model = joblib.load("../models/classifier.pkl")

# index webpage displays cool visuals and receives user input text for model
@app.route('/')
@app.route('/index')
def index():
    """used to render homepage"""

    # extract data needed for visuals
    # TODO: Below is an example - modify to extract data for your own visuals
    genre_counts = df.groupby('genre').count()['message']
    genre_names = list(genre_counts.index)

    # get label proportions of each category
    res = {}
    for label, content in df.iloc[:, 3:].iteritems():
        res[label + '_1'] = df[content == 1].shape[0]
        res[label + '_0'] = df[content == 0].shape[0]
    label_0 = [v for k, v in res.items() if '0' in k]
    label_1 = [v for k, v in res.items() if '1' in k]
    category = [k[:-2] for k in res.keys()]
    category = list(dict(zip(category, range(len(category)))).keys())

    # create visuals
    # TODO: Below is an example - modify to create your own visuals
    graphs = [
        {
            'data': [Bar(x=genre_names, y=genre_counts)],
            'layout': {
                'title': 'Distribution of Message Genres',
                'yaxis': {
                    'title': "Count"
                },
                'xaxis': {
                    'title': "Genre"
                }
            }
        },
        {
            'data': [Bar(name='label 0', x=category, y=label_0),
                     Bar(name='label 1', x=category, y=label_1)],
            'layout': {
                'title': 'Label Proportions of Each Category',
                'yaxis': {
                    'title': "Count"
                },
                'xaxis': {
                    'title': "Category"
                }
            }
        }
    ]

    # encode plotly graphs in JSON
    ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    # render web page with plotly graphs
    return render_template('master.html', ids=ids, graphJSON=graphJSON)

# web page that handles user query and displays model results
@app.route('/go')
def go():
    """used to render classification results"""

    # save user input in query
    query = request.args.get('query', '')

    # use model to predict classification for query
    classification_labels = model.predict([query])[0]
    classification_results = dict(zip(df.columns[4:], classification_labels))

    # This will render the go.html Please see that file.
    return render_template('go.html',
                           query=query,
                           classification_result=classification_results)

def main():
    """run the module"""
    app.run(host='0.0.0.0', port=3001, debug=True)

if __name__ == '__main__':
    main()
