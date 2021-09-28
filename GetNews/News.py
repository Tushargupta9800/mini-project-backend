from enum import unique
from os import name
from pymongo import MongoClient
from models.newsModel import NewsAPIModel, NewsModel
from Secrets.Keys import GeneralNewsEndPoint, MongoClientId
import requests
import datetime
from flask import jsonify

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

    cursor = collection.find().limit(n)

    finalList = []
    for news in cursor:
        finalList.append(NewsModel(news).__dict__)

    return jsonify(finalList)

def Get_Specific_News(data, n):
    return "Tushar"