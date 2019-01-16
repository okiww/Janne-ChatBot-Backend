from elasticsearch import Elasticsearch
from helper.parser.general import TextSearchParser


class SmartSearch(object):
    def __init__(self):
        config = self.get_elasticsearch_config()
        self.es_connection = Elasticsearch(**config)

    def get_message(self, message):
        ts_parser = TextSearchParser(self.es_connection, message)
        ts_parser.parse()

    @staticmethod
    def get_elasticsearch_config():
        return {
            'hosts': ['it.urbanindo.id'],
            'port': 9200,
            'use_ssl': False
        }
