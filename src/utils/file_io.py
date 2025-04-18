import os
import json
import csv
import numpy as np

def check_file_exists(file):
    return os.path.isfile(file)

def make_directory_for_file(full_name):
    os.makedirs(os.path.dirname(full_name), exist_ok=True)

def make_json_file(file_path, val=None):
    try:
        make_directory_for_file(file_path)

        with open(file_path, "w") as json_file:
            val = val if val is not None else {}
            json.dump(val, json_file, indent=4)

        return True

    except Exception as e:
        return False
    
def add_key_to_json(file_path, key, arr):

    try:
        make_directory_for_file(file_path)

        if os.path.exists(file_path):
            with open(file_path, "r") as json_file:
                try:
                    data = json.load(json_file)
                except json.JSONDecodeError:
                    data = {} 
        else:
            data = {}

        data[key] = arr if isinstance(arr, list) else list(arr)

        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)

        return True

    except Exception as e:
        return False


def save_array_to_json(file_path, arr, key):

    try:
        make_directory_for_file(file_path)

        data = {key: arr,}

        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)

        return data

    except Exception as e:
        return None

def get_json_content(filepath, key=None):
    try:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"JSON file not found: {filepath}")

        with open(filepath) as f:
            data = json.load(f)
        
        if key is not None:
            data = data.get(key)
        
        return data
    except Exception as e:
        return None

    
def create_or_replace_csv(file_path, headers=None):

    try:
        make_directory_for_file(file_path)

        with open(file_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            
            if headers:
                writer.writerow(headers)
        
        return True

    except Exception as e:
        return False
    
def append_row_to_csv(file_path, row_data):

    try:
        make_directory_for_file(file_path)

        with open(file_path, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(row_data)

        return True

    except Exception as e:
        return False
    
def rename_file(old_path, new_path, overwrite=True):

    try:
        if not os.path.exists(old_path):
            return False

        make_directory_for_file(new_path)

        if os.path.exists(new_path) and overwrite:
            os.remove(new_path)

        os.rename(old_path, new_path)
        return True

    except Exception as e:
        return False
