from django.test import TestCase
from grantstorage.storage.mongo.mongostorage import *
from pymongo import MongoClient


class TestMongoStorage(TestCase):
    def get_db(self):
        mc = MongoClient('mongodb://localhost/hpcbursar')
        return mc['hpcbursar']

    def test_expected_collections(self):
        db = self.get_db()
        collection = db.list_collection_names()
        expected_collections = ["group", "user", "grant", "allocation_usages"]
        for col in collection:
            self.assertIn(col, expected_collections)
