from collections import namedtuple
from logging import fatal
from models.newsModel import NewsModel
from bson.objectid import ObjectId
from pymongo import MongoClient
from Secrets.Keys import MongoClientId
from flask import jsonify

def NewsIdExsists(data, id):

    for idx in data['upvotes']:
        if idx == id:
            return 1
    
    for idx in data['downvotes']:
        if idx == id:
            return 2
    
    return 0

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

def getFakePercentage(data, name):
    upvotes = data['upvotes']
    downvotes = data['downvotes']
    if name == 0:
        upvotes = upvotes + 1
    else:
        downvotes = downvotes + 1
    percent = (downvotes)/(upvotes + downvotes)
    percent *= 76
    return percent
    

def oneNewsUpvote(data):
    try:
        cluster = MongoClient(MongoClientId)
        db = cluster['UserProfileDatabase']
        collection = db['Vote']
        
        db2 = cluster['NewsDatabase']
        collection2 = db2['NewsCollection']

        VoteBlock = collection.find_one({"_id" : ObjectId(data['vote_id'])})

        existInList = NewsIdExsists(data = VoteBlock, id = data['news_id'])
        if existInList != 0:
            name = "upvotes"
            if(existInList == 2):
                name = "downvotes"
            filter = {"_id" : ObjectId(data['vote_id'])}
            newField = {"$pull" : {name : {'$in' : [data['news_id']]}}}

            collection.update_one(filter, newField)
            filter = {"_id" : data['news_id']}
            newField = {"$inc" : {name : -1}}

            collection2.update_one(filter, newField)

        filter = {"_id" : ObjectId(data['vote_id'])}
        newField = {"$push" : {"upvotes" : data['news_id']}}

        collection.update_one(filter, newField)

        filter = {"_id" : data['news_id']}
        newsBlock = collection2.find_one(filter)
        newField = {"$inc" : {"upvotes" : 1}}

        collection2.update_one(filter, newField)
        newField = {'$set' : {"fake_percentage" : getFakePercentage(newsBlock, 0)}}
        collection2.update_one(filter, newField)
        
    except Exception as e:
        to_return = {"error" : "Error Try Again", "e" : str(e)}
        return jsonify(to_return)

    to_return = {"error" : "Success"}
    return jsonify(to_return)

def oneNewsDownvote(data):
    try:
        cluster = MongoClient(MongoClientId)
        db = cluster['UserProfileDatabase']
        collection = db['Vote']
        
        db2 = cluster['NewsDatabase']
        collection2 = db2['NewsCollection']

        VoteBlock = collection.find_one({"_id" : ObjectId(data['vote_id'])})

        existInList = NewsIdExsists(data = VoteBlock, id = data['news_id'])
        if existInList != 0:
            name = "upvotes"
            if(existInList == 2):
                name = "downvotes"
            filter = {"_id" : ObjectId(data['vote_id'])}
            newField = {"$pull" : {name : {'$in' : [data['news_id']]}}}

            collection.update_one(filter, newField)
            filter = {"_id" : data['news_id']}
            newField = {"$inc" : {name : -1}}

            collection2.update_one(filter, newField)

        filter = {"_id" : ObjectId(data['vote_id'])}
        newField = {"$push" : {"downvotes" : data['news_id']}}

        collection.update_one(filter, newField)

        filter = {"_id" : data['news_id']}
        newField = {"$inc" : {"downvotes" : 1}}
        newsBlock = collection2.find_one(filter)

        collection2.update_one(filter, newField)
        newField = {"$set": {"fake_percentage" : getFakePercentage(newsBlock, 1)}}
        collection2.update_one(filter, newField)

    except Exception as e:
        to_return = {"error" : "Error Try Again", "e" : str(e)}
        return jsonify(to_return)

    to_return = {"error" : "Success"}
    return jsonify(to_return)
