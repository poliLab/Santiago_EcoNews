from pymongo import MongoClient

class DataCollector():

    def __init__(self, host, port, dbname):
        self.client = MongoClient(host, port)
        self.db = self.client[dbname]

    def addData(self, document, data):
        dataId = self.db[document].insert_one(data).inserted_id
        return dataId

#dt = DataCollector('localhost', 27017, 'pythontest')