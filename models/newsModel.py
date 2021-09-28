import hashlib

class NewsAPIModel:
    def __init__(self, data):
        self._id = hashlib.sha256(data['url'].encode('utf-8')).hexdigest()
        self.title = data['title']
        self.description = data['description']
        self.published_at = data['publishedAt']
        self.news_url = data['url']
        self.img_url = data['urlToImage']
        self.keyword = "Aligarh"
        self.fake_percentage = 0.00
        self.upvotes = 0
        self.downvotes = 0

class NewsModel:
    def __init__(self, data):
        self.title = data['title']
        self.description = data['description']
        self.news_url = data['news_url']
        self.img_Url = data['img_url']
        self.published_at = data['published_at']
        self._id = str(data.get('_id'))
        self.keyword = data['keyword']
        self.upvotes = data['upvotes']
        self.downvotes = data['downvotes']
        self.fake_percentage = data['fake_percentage']
