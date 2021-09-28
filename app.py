from Authentication.auth import Login_User, Register_User
from flask import Flask, request

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    return Login_User(data = request.get_json())
    
@app.route('/register', methods=['POST'])
def register():
    return Register_User(data = request.get_json())

if __name__ == '__main__':
    app.run(debug = True)