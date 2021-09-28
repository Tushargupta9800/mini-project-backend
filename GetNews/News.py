from enum import unique
from os import name
from typing import Sized
from pymongo import MongoClient
from models.newsModel import NewsAPIModel, NewsModel
from Secrets.Keys import GeneralNewsEndPoint, MongoClientId
import requests
import datetime
from flask import jsonify
from bson.objectid import ObjectId

def Get_General_News(n):

    cluster = MongoClient(MongoClientId)
    db = cluster['NewsDatabase']
    collection = db['NewsCollection']

    try: 
        connect = requests.get(GeneralNewsEndPoint)
        AllNews = connect.json()

        NewsToBeStored = []
        for news in AllNews['articles']:
            currentNews = NewsAPIModel(news) 
            NewsToBeStored.append(currentNews.__dict__)

        collection.insert_many(NewsToBeStored)

    except Exception as e:
        # print(e)
        pass

    cursor = collection.find().sort('published_at', -1).limit(n)

    finalList = []
    for news in cursor:
        finalList.append(NewsModel(news).__dict__)

    return jsonify(finalList)

def Get_Specific_News(data, n):

    cluster = MongoClient(MongoClientId)
    db = cluster['UserProfileDatabase']
    collection = db['user']
    user = collection.find_one({'_id' : ObjectId(data['_id'])})

    db = cluster['NewsDatabase']
    collection = db['NewsCollection']

    try: 
        connect = requests.get(GeneralNewsEndPoint)
        AllNews = connect.json()

        NewsToBeStored = []
        for news in AllNews['articles']:
            currentNews = NewsAPIModel(news) 
            NewsToBeStored.append(currentNews.__dict__)

        collection.insert_many(NewsToBeStored)

    except Exception as e:
        # print(e)
        pass

    SearchList = []
    for interest in user['interests']:
        SearchList.append(interest)
    
    SearchList.append(user['state'])
    SearchList.append(user['city'])

    cursor = collection.find({'keyword' : {'$in' : SearchList}}).sort('published_at', -1).limit(n)

    finalList = []
    for news in cursor:
        finalList.append(NewsModel(news).__dict__)

    return jsonify(finalList)