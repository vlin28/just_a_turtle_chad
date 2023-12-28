import bleach
from pymongo import MongoClient

class Database:
    def __init__(self, type):
        self.allowedTags = ['br', 'strong', 'i', 'em', 'mark', 'small', 'del', 'ins', 'sub', 'sup']
        self.mongo = MongoClient(type)
        self.db = self.mongo['db']
        self.commentData = self.db['comments']
        self.htmlData = self.db['html']
        self.storedComments = self.db['stored']
        self.counter = self.db['counter']
    
    def dbCount(self):
        cur = self.counter.find_one({})
        if cur:
            newCount = cur.get("count",0)+1
            self.counter.update_one({}, {"$set": {"count": newCount}}, upsert=True)
            return newCount
        self.counter.insert_one({"count": 0})
        return 0
    
    def getAll(self):
        return self.commentData.find({})
    
    def getComments(self, start=0, amount=10):
        retrieved = []
        comments = self.commentData.find({"id": {"$gte": start}}).limit(amount)
        for comment in comments:
            retrieved.extend(comment.get("comments", []))
                
        return retrieved
    
    def getHtml(self):
        if self.htmlData.find_one({}):
            return self.htmlData.find_one({}).get("html", "")
        return ""
    
    def insert(self, videoID, comments: list[dict]):
        stored = self.storedComments.find_one({}).get("stored", []) if self.storedComments.find_one({}) else []
        curID = self.dbCount()
        bleachedComments = []
        # Comment: {"textDisplay": "I'm a turtle", "publishedAt": "2020-12-30T00:00:00Z", "videoID": "id"}
        for comment in comments:
            cleanedText = bleach.clean(comment["textDisplay"], tags=self.allowedTags)
            comment['textDisplay'] = cleanedText
            bleachedComments.append(comment)
        
        if videoID not in stored:
            stored.append(videoID)
            self.commentData.insert_one({"id": curID, "videoID": videoID, "comments": comments})
            self.storedComments.update_one({}, {"$set": {"stored": stored}}, upsert=True)
            
            return True
        return False