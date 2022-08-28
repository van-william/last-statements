"""
This is a boilerplate pipeline 'data_extraction'
generated using Kedro 0.18.2
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import logging

remove_request_warning = requests.packages.urllib3.exceptions.InsecureRequestWarning


def extract_names(URL: str) -> pd.DataFrame:
    """Extracts the table of names and statement links and outputs a pandas dataframe of names.
    Args:
        URL: URL for Texas Offenders Last Statement Information.
    Returns:
        Dataframe of names to extract statements
    """
    requests.packages.urllib3.disable_warnings(remove_request_warning)
    page = requests.get(URL, verify = False)
    soup = BeautifulSoup(page.content, "html.parser")

    table_names = soup.find(title="Table showing list of executed inmates")
    df = pd.read_html(str(table_names))[0]
    df['last_first'] = df['Last Name'].apply(lambda row : row.lower()) + df['First Name'].apply(lambda row: row.lower())
    df['last_first'] = df['last_first'].str.replace(r'[^\w\s]+', '', regex=True)
    df['last_first'] = df['last_first'].str.replace(' ', '')

    return df



def extract_statements(df: pd.DataFrame) -> pd.DataFrame:
    """Extracts last statements from the name of offenders.
    Args:
        df: DataFrame of links to obtain last statements
    Returns:
        Dataframe of last statements
    """
    requests.packages.urllib3.disable_warnings(remove_request_warning)
    statement_list = []
    name_list = list(df['last_first'])
    for name in name_list:
        try:
            url_offender = f'https://www.tdcj.texas.gov/death_row/dr_info/{name}last.html'
            page_offender = requests.get(url_offender, verify = False)
            soup_offender = BeautifulSoup(page_offender.content, "html.parser")
            title = soup_offender.body.find(string=re.compile('Last Statement:'))
            statement = title.find_next('p')
            statement_list.append(statement.string)
        except:
            statement_list.append('ERROR')
    # for index, row in df.iterrows():
    #     name = row['last_first']
    # try:
    #     url_offender = f'https://www.tdcj.texas.gov/death_row/dr_info/{name}last.html'
    #     page_offender = requests.get(url_offender, verify = False)
    #     soup_offender = BeautifulSoup(page_offender.content, "html.parser")
    #     title = soup_offender.body.find(text=re.compile('Last Statement:'))
    #     statement = title.find_next('p')
    #     df.at[index, 'statement'] = statement.string
    # except:
    #     df.at[index, 'statement'] = 'ERROR'
    #df['length'] = df['statement'].map(lambda x: len(x))
    df['statement'] = statement_list

    return df

