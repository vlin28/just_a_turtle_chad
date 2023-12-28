import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db import Database

database = Database("localhost")

def initDB():
    with open('db.comments.json', 'r', encoding="utf-8") as f:
        dbData = json.load(f)
    
    for data in dbData:
        database.insert(data["videoID"], data["comments"])
        
if __name__ == "__main__":
    initDB()
    print("Data inserted!")
    