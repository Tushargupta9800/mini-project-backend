class user():
    def __init__(self, data):
        self.name = data['name']
        self.state = data['state']
        self.city = data['city']
        self.interests = data['interests']
        self.voteId = str(data.get('voteId'))
