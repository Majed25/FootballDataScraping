import glob
import csv
import os
import json
import shutil


file_paths = glob.glob('temp_data/*.csv')
schema_paths = glob.glob('temp_data/*.json')


def merge_shooting_data():
    path1 = 'shooting_data/sd_17_24.csv'
    path2 = 'shooting_data/sd_09_10.csv'
    schema_path1 = 'shooting_data/sd_17_24_schema.json'
    schema_path2 = 'shooting_data/sd_09_10_schema.json'
    for path in [path1, path2, schema_path1, schema_path2]:
        directory = os.path.dirname(path)
        os.makedirs(directory, exist_ok=True)

    # initiate a tracker to avoid adding headers multiple times
    i, j = (0, 0)
    # open two files for each data tranche
    with open(path1, 'a', newline='') as d1, open(path2, 'a', newline='') as d2:
        csv_writer1 = csv.writer(d1)
        csv_writer2 = csv.writer(d2)

        for file in file_paths:
            with open(file, 'r') as f:
                csv_reader = csv.reader(f)
                header = next(csv_reader, [])
                header_len = len(header)
                print(header_len)
                if header_len == 27:
                    print(header)
                    if i == 0:
                        csv_writer1.writerow(header)
                    for row in csv_reader:
                        if len(row) != len(header):
                            print('error')
                        else:
                            csv_writer1.writerow(row)
                    i += 1

                else:
                    print(header)
                    if j == 0:
                        csv_writer2.writerow(header)
                    for row in csv_reader:
                        if len(row) != len(header):
                            print('error')
                        else:
                            csv_writer2.writerow(row)
                    j += 1
    # merge schemas
    is_schema_1 = False
    is_schema_2 = False
    for path in schema_paths:
        with open(path, 'r') as json_file:
            dict = json.load(json_file)
            if len(dict.keys()) == 27:
                if  not is_schema_1:
                    with open(schema_path1, 'w', newline='') as json_file:
                        json.dump(dict, json_file, indent=2)
                        is_schema_1 = True
            elif len(dict.keys()) == 21:
                if not is_schema_2:
                    with open(schema_path2, 'w', newline='') as json_file:
                        json.dump(dict, json_file, indent=2)
                        is_schema_1 = True
            else:
                print(f'inconsistent schema {dict}')

    # clear temp data
    shutil.rmtree('temp_data/')
    os.makedirs('temp_data/')


def merge_defensive_data():
    my_path = 'defensive_data/dd_2009_2024.csv'
    schema_path = 'defensive_data/dd_2009_2024_schema.json'
    for p in [my_path, schema_path]:
        directory = os.path.dirname(p)
        os.makedirs(directory, exist_ok=True)

    # initiate a tracker to avoid adding headers multiple times
    i = 0
    with open(my_path, 'a', newline='') as d:
        csv_writer = csv.writer(d)
        for file in file_paths:
            with open(file, 'r') as f:
                csv_reader = csv.reader(f)
                header = next(csv_reader, [])
                header_len = len(header)
                if i == 0:
                    csv_writer.writerow(header)
                for row in csv_reader:
                    if len(row) != len(header):
                        print('error')
                    else:
                        csv_writer.writerow(row)
                i += 1

    # merge schemas
    with open(schema_paths[0], 'r') as json_file:
        dict = json.load(json_file)
        with open(schema_path, 'w', newline='') as json_file:
            json.dump(dict, json_file, indent=2)

    # clear temp data
    shutil.rmtree('temp_data/')
    os.makedirs('temp_data/')





