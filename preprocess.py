import pandas as pd
from utils import convert_date
import yaml
from datetime import datetime
import argparse
import os

config = yaml.load(open("config.yml", "r"), yaml.SafeLoader)

def preprocess_csv(csv_year):
    if csv_year == '2015':
        dtype = {'Vehicle Expiration Date' : object,
                 'Violation Precinct' : float,
                 'Issuer Precinct' : float,
                 'Vehicle Year' : float}
    else:
        dtype = {'Vehicle Expiration Date' : float,
                 'Violation Precinct' : float,
                 'Issuer Precinct' : float,
                 'Vehicle Year' : float}        
    
    clean_data = pd.read_csv(config['Dataset'][csv_year], 
                             usecols=['Vehicle Expiration Date', 'Violation Precinct', 'Issuer Precinct', 'Vehicle Year'], 
                             dtype=dtype).dropna()
    
    clean_data['Vehicle Expiration Date'] = clean_data['Vehicle Expiration Date'].apply(convert_date)
    
    if not(os.path.isdir(config['clean_data']['dir'])):
        os.makedirs(config['clean_data']['dir'])

    clean_data.to_csv(config['clean_data'][csv_year], index=False)

if __name__ == "__main__":
    with Pool(6) as p:
        p.map(preprocess_csv, ['2013-14','2015','2016','2017'])