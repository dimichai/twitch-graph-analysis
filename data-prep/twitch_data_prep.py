import json
import csv
import pandas as pd
import os


def read_json_from_file(filename):
    input_file = open(filename)
    json_data = json.load(input_file)
    return json_data


def extract_unique_followers(directory):
    """
    reads the followage relationships from the given directory and saves unique users in [id, name] .csv format
    :param directory: the directory to read the input from
    :return:
    """
    total_followage = pd.DataFrame(columns=['from_id', 'from_name', 'to_id', 'to_name', 'followed_at'])

    # Read all data - append it to total_followage
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            dataframe = pd.read_csv(os.path.join(directory, filename))
            total_followage = total_followage.append(dataframe)
            continue
        else:
            continue
    # Keep unique values
    total_followage = total_followage.drop_duplicates(subset='from_id')
    # drop unneeded labels
    total_followage = total_followage.drop(labels=['to_id', 'to_name', 'followed_at'], axis=1)
    # save to csv
    total_followage.to_csv(os.path.join(directory, 'unique_users.csv'), sep=',', header=['id', 'name'], index=False)
    pass


def scraped_to_csv(filename, field_names):
    """
    Converts twitch channel data scraped from twitch stats websites to csv.
    :param filename: filename input (.json)
    :param field_names: json property names
    :return: nothing
    """
    json_data = read_json_from_file(filename + '.json')

    with open(filename + '.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=field_names)
        writer.writeheader()

        for data in json_data:
            writer.writerow(data)
    pass


if __name__ == '__main__':
    # top streamers: from json to csv.
    scraped_to_csv('input/greek_streams.json', ['name', 'streamId', 'game'])
    # extract_unique_followers('data/greek_streamers')
