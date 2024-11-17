# utils.py
import requests
import random
import time
import csv
from config import HEADERS, DELAY_BETWEEN_REQUESTS
import ast

def concatenate_columns(df):
    def format_row(row):
        description = f"Description: {row['Description']}. "

        # Parse and format Specification
        try:
            spec_dict = ast.literal_eval(row['Specifications'])
            specifications = "Specifications: " + "; ".join(f"{k}: {v}" for k, v in spec_dict.items()) + "."
        except (ValueError, SyntaxError):
            specifications = "Specifications: Not available."

        # Parse and format Features
        try:
            features_list = ast.literal_eval(row['Features'])
            features = "Features: " + "; ".join(features_list) + "."
        except (ValueError, SyntaxError):
            features = "Features: Not available."

        return f"{description} {specifications} {features}"

    return df.apply(format_row, axis=1)

def get_html(url):
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrieve {url}")
        return None

def delay():
    time.sleep(random.uniform(*DELAY_BETWEEN_REQUESTS))

def save_to_csv(data, filename="emerson_products_10p.csv"):
    if not data:
        print("No data to save.")
        return
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        dict_writer = csv.DictWriter(file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
