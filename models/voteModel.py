from bson.objectid import ObjectId

class voteModel():
    def __init__(self, data):
        self._id = str(data.get('_id'))
        self.user_id = str(data.get('user_id'))
        self.upvotes = data['upvotes']
        self.downvotes = data['downvotes']