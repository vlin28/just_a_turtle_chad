import json

def getKey():
    with open('apiKey.json', 'r') as f:
        key = json.load(f)
    return key["key"]