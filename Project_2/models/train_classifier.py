# import libraries
import sys
import re
from unidecode import unidecode
import pandas as pd
import numpy as np

from sqlalchemy import create_engine

import nltk
nltk.download(['stopwords', 'wordnet', 'punkt'])
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.externals import joblib

from matplotlib import pyplot as plt
import seaborn as sns

def load_data(database_filepath):
    """used to load data from DB and return it as
    ready to train/test dataset"""

    engine = create_engine(f'sqlite:///{database_filepath}')
    df = pd.read_sql_table('message_category', con=engine)

    engine.dispose()

#     df.drop(columns=['child_alone'], inplace=True)
    category_names = list(df.columns[3:])

    X = df.message.values
    Y = df.iloc[:, 3:].values

    return X, Y, category_names

# set necessary variables for tokenizer func
lemmatizer = WordNetLemmatizer()
regex_punct = r"[^\w\s]"
regex_url = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
eng_stopwords = stopwords.words('english')

def tokenize(text, lemmatizer=lemmatizer, stopwords=eng_stopwords):
    """used to preprocess text so that it's ready for training"""

    # convert any accented char
    text = unidecode(text)
    
    # convert any URL
    detected_urls = re.findall(regex_url, text)
    for url in detected_urls:
        text = text.replace(url, "urlplaceholder")
    
    # remove any punct
    text = re.sub(regex_punct, ' ', text)
    text = re.sub(r"\s+", " ", text)
    
    tokens = word_tokenize(text)
    
    # uncase & lemmatize each token
    clean_tokens = []
    for tok in tokens:
        if tok not in stopwords:
            uncased_tok = tok.lower().strip()
            clean_tok = lemmatizer.lemmatize(uncased_tok)
            if clean_tok == uncased_tok:
                clean_tok = lemmatizer.lemmatize(clean_tok, pos='a')
            if clean_tok == uncased_tok:
                clean_tok = lemmatizer.lemmatize(clean_tok, pos='v')
            clean_tokens.append(clean_tok)
            
    return clean_tokens

def build_model():
    """used to create a classifier model"""

    # instantiate models
    random_forest = RandomForestClassifier(random_state=1)
    xgboost = GradientBoostingClassifier(random_state=1)

    # define pipeline
    pipeline = Pipeline([
        ('count', CountVectorizer(tokenizer=tokenize)),
        ('tfidf', TfidfTransformer()),
        ('classifier', MultiOutputClassifier(random_forest))
#         ('classifier', MultiOutputClassifier(xgboost))
    ])

    # set CV parameters
    parameters = {
#         'count__ngram_range': ((1, 1), (1, 2)),
#         'count__lowercase': (True, False),
#         'count__max_df': (0.5, 1.0, 2.0),
#         'count__max_features': (None, 5000, 10000),
        'tfidf__use_idf': (True, False)
#         'tfidf__smooth_idf': (True, False)
    }

    # define grid search
    cv = GridSearchCV(pipeline, param_grid=parameters)

    return cv

def evaluate_model(model, X_test, Y_test, category_names,):
    """used to evaluate given model by using
    confusion matrix and classification report"""

    y_pred = model.predict(X_test)

    for j in range(y_pred.shape[1]):
        print('TARGET: ', category_names[j])
        print('\t\t---- CONFUSION MATRIX----')

        classes = np.unique(Y_test[:, j]) #sorted(df[category_names[j]].unique())
        print(confusion_matrix(Y_test[:, j],
                               y_pred[:, j],
                               labels=classes))

        print('\t\t----REPORT----')
        print(classification_report(Y_test[:, j],
                                    y_pred[:, j],
                                    labels=classes))
        print('===========================================', end='\n\n')

def save_model(model, model_filepath):
    """used to save a trained model in given path"""
    # Save the model as a pickle in a file
    joblib.dump(model, model_filepath)

def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')

if __name__ == '__main__':
    main()