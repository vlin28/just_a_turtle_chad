import time
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from db import Database
from python.commentHandler import getTurtle
from python.getKey import getKey

database = Database("mongo", 65123)
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = getKey()

def update(maxResults=50):
    if not database.commentData.count_documents({}):
        maxResults = 50
    
    youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.activities().list(
        part="contentDetails",
        channelId="UCz5C8kGBXSd3hRtxCwUQ3_Q",
        maxResults=maxResults
    )
    response = request.execute()
    activities = response.get("items", [])
    
    for activity in activities:
        uploadType = activity.get("contentDetails").get("upload", "")
        
        if uploadType:
            videoID = uploadType.get("videoId")
            comments = getTurtle(videoID)
            
            if comments:
                status = database.insert(videoID, comments)
                if status:
                    print("Successfully added", videoID)
                else:
                    print("Video id already exists in database", videoID)
            else:
                print("No comments found for", videoID)
    
if __name__ == "__main__":
    while True:
        update(maxResults=20)
        print("Updated")
        time.sleep(3600)