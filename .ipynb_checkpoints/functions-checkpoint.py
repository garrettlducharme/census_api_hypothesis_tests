import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats

pd.set_option('display.float_format', lambda x: '%.2f' % x)

def api_call(url_head, variables, api_key):
    """
    Accepts a url header, variables, and an api_key for the US census API.
    Returns a response with data for the listed variables in a JSON format.
    """
    url = f"{url_head},{','.join(variables)}&for=state:*&key={api_key}"
    print(url)
    response = requests.get(url)
    
    return response

def json_to_pandas(api_response, col_names):
    """
    Accepts a response from a call to the US Census API.
    Returns a cleaned pandas dataframe with statistics on US states.
    """
    
    df = pd.DataFrame(api_response.json()[1:])
    df.drop(df.columns[-1], axis=1, inplace=True) #Drop the state codes
    df.columns = col_names #Give the variables meaningful column names
    df.set_index(keys='state', inplace=True) #Set the US states as an index
    df.drop(index = ['Puerto Rico', 'Hawaii', 'Alaska', 'District of Columbia'], inplace=True) #Drop PR, HI, AL, DC
    df = df.astype(float) #Everything to floats
    
    return df

def region_dfs(df):
    """
    Accepts a dataframe with demigraphic data by state from the US census API.
    Returns dataframes which are subset by the Northern and Southern US.
    """
    south_atlantic_US = ['Delaware', 'Florida', 'Georgia','Maryland',
                         'North Carolina','South Carolina','Virginia',
                         'West Virginia']
    east_south_US = ['Alabama','Kentucky','Mississippi','Tennessee']
    west_south_US = ['Arkansas','Louisiana','Oklahoma','Texas']
    south_US = south_atlantic_US + east_south_US + west_south_US
    
    df_south = df.loc[df.index.isin(south_US)]
    df_north = df.loc[~df.index.isin(south_US)]
    
    return df_south, df_north

def census_plotter(df_south, df_north, col_name, title, save_name):
    plt.figure(figsize=(14,8))
    sns.set_context('poster')
    sns.distplot(df_south[col_name], label='South', bins='auto')
    sns.distplot(df_north[col_name], label='North', bins='auto')
    plt.axvline(df_south[col_name].mean(), linestyle = '--', linewidth = 5)
    plt.axvline(df_north[col_name].mean(), linestyle = '--', linewidth = 5, color = 'orange')
    plt.legend()
    plt.title(title)
    plt.xlabel('Percentage')
    plt.savefig(f'./{save_name}')

