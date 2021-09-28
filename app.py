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

if __name__ == '__main__':
    app.run(debug = True)