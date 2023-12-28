# -*- coding: utf-8 -*-

# Sample Python code for youtube.commentThreads.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import googleapiclient.discovery
import pytz
from python.getKey import *
from datetime import datetime

turtleDisplasyName = "@just_a_turtle_chad"
api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = getKey()

# Converts UTC zulu to EST
def convertTime(time):
    if time is None:
        return None
    
    zulu = datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
    local = zulu.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('US/Eastern'))  # replace with your timezone
    return local.strftime("%Y-%m-%d %H:%M:%S")

def getTurtle(video):
    try:
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey = DEVELOPER_KEY
        )

        response = youtube.commentThreads().list(
            part="snippet",
            maxResults=100,
            videoId=video,
            order="relevance"
        ).execute()
        
        comments = []
        for snippet in response.get("items", []):
            commentData = snippet.get("snippet").get("topLevelComment").get("snippet")
            if commentData.get("authorDisplayName") == turtleDisplasyName:
                text = commentData.get("textDisplay")
                time = convertTime(commentData.get("publishedAt"))
                
                comments.append({"textDisplay": text, "publishedAt": time, "videoID": video})
        
        return comments
    except Exception as e:
        print(e)
        return []