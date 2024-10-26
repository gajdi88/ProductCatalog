# utils.py
import requests
import random
import time
import csv
from config import HEADERS, DELAY_BETWEEN_REQUESTS

def get_html(url):
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrieve {url}")
        return None

def delay():
    time.sleep(random.uniform(*DELAY_BETWEEN_REQUESTS))

def save_to_csv(data, filename="emerson_products.csv"):
    if not data:
        print("No data to save.")
        return
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        dict_writer = csv.DictWriter(file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
