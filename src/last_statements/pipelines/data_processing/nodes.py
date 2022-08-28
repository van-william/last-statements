"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.18.2
"""

from typing import Dict
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
from scipy.sparse import csr_matrix

from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer
from nltk import word_tokenize
from nltk.stem import PorterStemmer

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

def process_last_statements(df: pd.DataFrame, remove_statements) -> pd.DataFrame:
    """cleans up last statements.
    Args:
        Dataframe of last statements
    Returns:
        Cleaned Up Dataframe
    """

    # remove extra carriage returns:
    df['statement'] = df['statement'].str.replace(r'\\r','', regex=True)

    # filter out statements with errors / default statements
    df = df[~df.statement.isin(remove_statements)]

    # Sometimes statements are blank; filter these out as well
    df = df[df['statement'].notna()]

    return df

def transform_last_statements(df: pd.DataFrame) -> pd.DataFrame:
    """transforms last statements using tf-idf and other manipulations.
    Args:
        Processed DataFrame of Last Statements
    Returns:
        Transformed Matrix for Clustering
    """
    def text_process(text):
        '''
        Takes in a string of text, then performs the following:
        1. Remove all punctuation
        2. Remove all stopwords
        3. Return the cleaned text as a list of words
        4. Remove words
        '''
        stemmer = WordNetLemmatizer()
        nopunc = [char for char in text if char not in string.punctuation]
        nopunc = ''.join([i for i in nopunc if not i.isdigit()])
        nopunc =  [word.lower() for word in nopunc.split() if word not in stopwords.words('english')]
        return [stemmer.lemmatize(word) for word in nopunc]
    
    statement_list = list(df.statement)
    tfidfconvert = TfidfVectorizer(analyzer=text_process).fit(statement_list)
    transformed_statements = tfidfconvert.transform(statement_list)
    df_vocab = pd.DataFrame(index=None, data = zip(tfidfconvert.vocabulary_.keys(), tfidfconvert.vocabulary_.values()),columns=['word', 'index']).sort_values('index')
    
    df = pd.DataFrame(csr_matrix.todense(transformed_statements), columns=df_vocab.word)

    return df