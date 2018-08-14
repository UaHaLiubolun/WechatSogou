from pymongo import MongoClient

class MongoUtil(object):

    def __init__(self):
        self.ip = "172.29.4.24"
        self.port = 27017
        self.client = MongoClient(self.ip, self.port)
        self.db = self.client.wei_xin

    def insertContent(self, content):
        collection = self.db.gzh_content
        collection.insert_one(content)