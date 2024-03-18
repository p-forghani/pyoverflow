import json

def read_json(file_name):
    '''Reads from a json file'''
    with open(file_name, 'r') as f:
        return json.load(f)

def write_json(data, file_name, indent=2):
    '''Writes the data into the file_name'''
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=indent)
