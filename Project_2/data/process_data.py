"""Copyright (c) 2021 Reza Dwi Utomo

This module executes the following tasks:
- load data from messages.csv and categories.csv
- clean both data
- save data to SQLite database
"""

import sys
import re
import pandas as pd
from sqlalchemy import create_engine

def load_data(messages_filepath, categories_filepath):
    """used to load messages and categories datasets"""

    # load message dataset
    messages = pd.read_csv(messages_filepath)
    messages.drop_duplicates(subset='message', inplace=True)
    messages.drop(columns=['original'], inplace=True)

    # load category dataset
    categories = pd.read_csv(categories_filepath)

    # message left join category
    df = messages.merge(categories, how='left', on='id')

    return df

def clean_data(df):
    """used to clean joint message & category dataset"""

    # get all 36 category names
    category_labels = [re.sub(r"\-[01]", "", cat) for cat in df.categories[0].split(';')]

    # set lambda func to get last digit
    get_digit = lambda row: row[-1]

    # expand the categories col so that it consists of 36 cols
    categories_expand = df.categories.str.split(';', expand=True)
    categories_expand.columns = category_labels # set correct col names

    # process each category so that its each row only contain number
    for col in categories_expand.columns:
        categories_expand.loc[:, col] = categories_expand[col].apply(get_digit).astype(int)

    # combine the expanded dataset to the original one
    df = pd.concat([df[['id', 'message', 'genre']], categories_expand], axis=1)
    df.drop_duplicates(subset='id', inplace=True)

    return df

def save_data(df, database_filename):
    """used to save given dataframe to SQLite database

    args:
    - df: dataframe
    - database_filename: SQLite DB name
    """

    table_name = 'message_category'

    # instantiate DB engine
    engine = create_engine(f'sqlite:///{database_filename}')
    connection = engine.raw_connection()

    # get DB cursor so that we can execute SQL query
    cursor = connection.cursor()
    query = f"DROP TABLE IF EXISTS {table_name}"
    cursor.execute(query)
    connection.commit() # commit the change

    # save DF to DB
    df.to_sql(table_name, engine, index=False)

    # shut down DB engine
    cursor.close()
    engine.dispose()

def main():
    """run the module"""
    # catch args inputted from CLI
    if len(sys.argv) == 4:
        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)

        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)

        print('Cleaned data saved to database!')

    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')

if __name__ == '__main__':
    main()
