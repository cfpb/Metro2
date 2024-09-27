import json

def get_json_file_contents(filepath: str):
    return json.loads(get_file_contents(filepath))

def get_file_contents(filepath: str):
    with open(filepath, "r") as f:
        return f.read()