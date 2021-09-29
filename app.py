from GetNews.Votes import allUserVotes
from GetNews.oneNews import getOneNews, oneNewsDownvote, oneNewsUpvote
from GetNews.News import Get_General_News, Get_Specific_News
from Authentication.auth import Login_User, Register_User
from flask import Flask, request

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    return Login_User(data = request.get_json())
    
@app.route('/register', methods=['POST'])
def register():
    return Register_User(data = request.get_json())

@app.route('/get/news/<int:n>', methods=['POST', 'GET'])
def getNews(n):
    if request.method == 'GET':
        return Get_General_News(n = n)
    else:
        return Get_Specific_News(data = request.get_json(), n = n)

@app.route('/one/news/<string:n>', methods=['GET'])
def oneNews(n):
    return getOneNews(n)

@app.route('/one/news/upvote', methods=['POST'])
def UpvoteNews():
    return oneNewsUpvote(data = request.get_json())

@app.route('/one/news/downvote', methods=['POST'])
def DownvoteNews():
    return oneNewsDownvote(data = request.get_json())

@app.route('/user/all/votes/<string:n>', methods=['GET'])
def allVotes(n):
    return allUserVotes(data=n)

if __name__ == '__main__':
    app.run(debug = True)