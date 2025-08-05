import json
import os
import sys


def load_env_config():
    app_env = os.getenv('ETL_APP_ENV', 'dev1')
    try:
        with open(f'env/{app_env}.json', 'r') as file:
            return json.load(file) # to json to py object / dict
    except FileNotFoundError:
        print(f"Error: app env file for {app_env} not found.")
        sys.exit(1)


def load_etl_config(etl_name: str):
    # Load configuration for the given etl_name
    try:
        with open(f'config/{etl_name}-config.json', 'r') as file:
            return json.load(file) # to json to py object / dict
    except FileNotFoundError:
        print(f"Error: Configuration file for {etl_name} not found.")
        sys.exit(1)