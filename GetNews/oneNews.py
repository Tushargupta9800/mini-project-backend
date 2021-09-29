from logging import fatal
from models.newsModel import NewsModel
from bson.objectid import ObjectId
from pymongo import MongoClient
from Secrets.Keys import MongoClientId
from flask import jsonify

def NewsIdExsists(data, id):

    for idx in data['upvotes']:
        if idx == id:
            return False
    
    for idx in data['downvotes']:
        if idx == id:
            return False
    
    return True

def getOneNews(n):
    cluster = MongoClient(MongoClientId)
    db = cluster['NewsDatabase']
    collection = db['NewsCollection']
    news = collection.find_one({'_id' : n})

    if news is not None:
        return NewsModel(news).__dict__
    else:
        to_return = {"error" : "No news found in the database"}
        return jsonify(to_return)

def oneNewsUpvote(data):
    try:
        cluster = MongoClient(MongoClientId)
        db = cluster['UserProfileDatabase']
        collection = db['Vote']

        VoteBlock = collection.find_one({"_id" : ObjectId(data['vote_id'])})

        if NewsIdExsists(data = VoteBlock, id = data['news_id']) == False:
            to_return = {"error" : "Action can't be performed"}
            return jsonify(to_return)

        filter = {"_id" : ObjectId(data['vote_id'])}
        newField = {"$push" : {"upvotes" : data['news_id']}}

        collection.update_one(filter, newField)

        db = cluster['NewsDatabase']
        collection = db['NewsCollection']

        filter = {"_id" : data['news_id']}
        newField = {"$inc" : {"upvotes" : 1}}

        collection.update_one(filter, newField)
    except Exception as e:
        to_return = {"error" : "Error Try Again"}
        return jsonify(to_return)

    to_return = {"error" : "Success"}
    return jsonify(to_return)

def oneNewsDownvote(data):
    try:
        cluster = MongoClient(MongoClientId)
        db = cluster['UserProfileDatabase']
        collection = db['Vote']

        VoteBlock = collection.find_one({"_id" : ObjectId(data['vote_id'])})

        if NewsIdExsists(data = VoteBlock, id = data['news_id']) == False:
            to_return = {"error" : "Action can't be performed"}
            return jsonify(to_return)

        filter = {"_id" : ObjectId(data['vote_id'])}
        newField = {"$push" : {"downvotes" : data['news_id']}}

        collection.update_one(filter, newField)

        db = cluster['NewsDatabase']
        collection = db['NewsCollection']

        filter = {"_id" : data['news_id']}
        newField = {"$inc" : {"downvotes" : 1}}

        collection.update_one(filter, newField)

    except Exception as e:
        to_return = {"error" : "Error Try Again"}
        return jsonify(to_return)

    to_return = {"error" : "Success"}
    return jsonify(to_return)
