from flask import Flask, render_template, request, make_response, redirect
from python.getKey import *
from python.commentHandler import *
from db import Database

app = Flask(__name__, static_folder="static")
database = Database("mongo", 65123)

@app.route('/', methods=["GET"])
def index():
    comments = database.getComments()
    return render_template('index.html', comments=comments)

@app.route('/add')
def add():
    videoID = request.args.get("v")
    comments = getTurtle(videoID)
    if comments:
        status = database.insert(videoID, comments)
        
        if status:
            return redirect("/")
        return make_response("The video id already exists", 400)
    return make_response("Comment not found, either video id was invalid or the comment could not be found within the first 100 comments", 400)

@app.route('/update')
def update():
    try:
        startPoint = int(request.headers.get("value"))
        comments = database.getComments(startPoint, 10)
        
        if comments:
            return make_response(comments)
        return make_response({"error": "No comments found"}, 200)
    except Exception as e:
        print(e)
        return make_response({"error": "An error occured"}, 400)

@app.route("/youtubeLogo.png")
def logo(): 
    return app.send_static_file("youtubeLogo.png")

@app.route("/pfp.jpg")
def pfp():
    return app.send_static_file("pfp.jpg")

@app.route("/styles.css")
def style():
    return app.send_static_file("styles.css")

@app.route("/functions.js")
def js():
    return app.send_static_file("functions.js")

if __name__ == '__main__':
    app.run("0.0.0.0", 4242)
