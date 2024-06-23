import glob
import pandas as pd
import csv
import os
import json
import shutil
import logging



# Script to Merge the separate data tables into one file.

def load_params():
    with open('/Users/macbookpro/PycharmProjects/FootballDataScraping/parameters.json', 'r') as f:
        params = json.load(f)
    return params



def ensure_directories(paths):
    for path in paths:
        logging.info(f'crating paths: {path}')
        directory = os.path.dirname(path)
        os.makedirs(directory, exist_ok=True)

def write_data(params, csv_path, schema_path):
    file_paths = glob.glob(f'{params['data_paths']['temp_data']}*.csv')
    schema_paths = glob.glob(f'{params['data_paths']['temp_data']}*.json')

    # initiate a tracker to avoid adding headers multiple times
    data_frames = []
    for file in file_paths:
        df = pd.read_csv(file)
        data_frames.append(df)
    concatenated_df = pd.concat(data_frames, ignore_index=True, sort=False)
    logging.info(f'concatenated data frame: {concatenated_df.head()}')
    concatenated_df.to_csv(csv_path, index=False)

    """Find the schema with the most fields and save it."""
    schema = {}
    for path in schema_paths:
        with open(path, 'r') as file:
            current_schema = json.load(file)
        if len(current_schema) > len(schema):
            schema = current_schema
    with open(schema_path, 'w', newline='') as json_file:
        json.dump(schema, json_file, indent=2)

def clear_temp_data(params):
    # clear temp data
    shutil.rmtree(f'{params['data_paths']['temp_data']}')
    os.makedirs(f'{params['data_paths']['temp_data']}')


def merge_data(params):
    data = params['data_paths']['shoot_data']['csv']
    schema = params['data_paths']['shoot_data']['schema']
    logging.info(f'data path: {data}')
    logging.info(f'schema path: {schema}')
    ensure_directories([data, schema])
    write_data(params, data, schema)
    clear_temp_data(params)


def merge_defensive_data(params):
    data = params['def_data']['csv']
    schema = params['def_data']['schema']

    ensure_directories([data, schema])
    write_data(params, data, schema)
    clear_temp_data(params)





# merge opposition passes data
def merge_opp_pass_data(params):
    data = params['data_paths']['op_pass_data']['csv']
    schema = params['data_paths']['op_pass_data']['schema']

    ensure_directories([data, schema])
    write_data(params, data, schema)
    clear_temp_data(params)


# merge transfers_ data
def merge_transfers_data(params):
    data = params['data_paths']['tfr_data']['csv']
    ensure_directories([data])
    write_data(params, data, None)
    clear_temp_data(params)
