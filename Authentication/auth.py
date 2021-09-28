from models.user import user
from Secrets.Keys import MongoClientId
from typing import List
import pymongo
from pymongo import MongoClient
from flask import session, jsonify
import bcrypt
import json


def error_handler_register(data):

    checkList = ['email', 'name', 'state', 'city', 'password', 'interests']
    
    for check in checkList:
        if check not in data:
            print(check)
            return False

    if type(data['interests']) != List and len(data['interests']) == 0:
        return False

    return True

def error_handler_login(data):

    checkList = ['email' , 'password']

    for check in checkList:
        if check not in data:
            print(check)
            return False
    
    return True

def check_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password, hashed_password)

def Login_User(data):
    
    if error_handler_login(data) == False:
        to_return = {"error" : "Fill Every Field"}
        return jsonify(to_return)

    cluster = MongoClient(MongoClientId)
    db = cluster['UserProfileDatabase']
    collection = db['user']

    user_exists = collection.find_one({'email' : data['email']})

    if user_exists:
        encodedPass = data['password'].encode('utf-8')
        if check_password(encodedPass, user_exists['password']):
            
            User = user(user_exists)

            to_return = {
                "error" : "Success",
                "message" : "Login Successful",
                "key" : str(user_exists.get('_id')),
                "data" : User.__dict__
                }
            return jsonify(to_return)
        else:
            to_return = {"error" : "Email or Password is wrong"}
            return jsonify(to_return)

    to_return = {"error" : "No User Exists for this Email Id kindly register first"}
    return jsonify(to_return)

def Register_User(data):

    if error_handler_register(data) == False:
        to_return = {"error" : "Fill Every Field"}
        return jsonify(to_return)


    cluster = MongoClient(MongoClientId)
    db = cluster['UserProfileDatabase']
    collection = db['user']
    
    existing_user = collection.find_one({'email' : data['email']})

    if existing_user is None:
        hashpass = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

        collection.insert({
            "email" : data['email'],
            "password" : hashpass,
            "state" : data['state'],
            "city" : data['city'],
            "name" : data['name'],
            "interests" : data['interests']
            })

        to_return = {"error" : "Success", "message" : "Register Completed"}
        return jsonify(to_return)
    
    to_return = {"error" : "Account connected to this username already exsists"}
    return jsonify(to_return)