from models.voteModel import voteModel
from bson.objectid import ObjectId
from pymongo import MongoClient
from Secrets.Keys import GeneralNewsEndPoint, MongoClientId

def allUserVotes(data):
    cluster = MongoClient(MongoClientId)
    db = cluster['UserProfileDatabase']
    collection = db['Vote']

    VoteBlock = collection.find_one({"_id" : ObjectId(data)})
    return voteModel(VoteBlock).__dict__