import sys
import re
import pandas as pd
from sqlalchemy import create_engine

def load_data(messages_filepath, categories_filepath):
    messages = pd.read_csv(messages_filepath)
    messages.drop_duplicates(subset='message', inplace=True)
    messages.drop(columns=['original'], inplace=True)

    categories = pd.read_csv(categories_filepath)

    df = messages.merge(categories, how='left', on='id')

    return df

def clean_data(df):
    category_labels = [re.sub(r"\-[01]", "", cat) for cat in df.categories[0].split(';')]

    get_digit = lambda row: row[-1]

    categories_expand = df.categories.str.split(';', expand=True)
    categories_expand.columns = category_labels

    for col in categories_expand.columns:
        categories_expand.loc[:, col] = categories_expand[col].apply(get_digit).astype(int)

    df = pd.concat([df[['id', 'message', 'genre']], categories_expand], axis=1)
    df.drop_duplicates(subset='id', inplace=True)

    return df

def save_data(df, database_filename):
    table_name = 'message_category'

    engine = create_engine(f'sqlite:///{database_filename}')

    connection = engine.raw_connection()

    cursor = connection.cursor()

    query = f"DROP TABLE IF EXISTS {table_name}"

    cursor.execute(query)

    connection.commit()

    df.to_sql(table_name, engine, index=False)

    cursor.close()
    engine.dispose()

def main():
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