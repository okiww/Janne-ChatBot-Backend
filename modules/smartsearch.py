from elasticsearch import Elasticsearch

from helper.es import ElasticSearchHelper
from helper.parser.general import TextSearchParser


class SmartSearch(object):
    def __init__(self):
        config = self.get_elasticsearch_config()
        self.es_connection = Elasticsearch(**config)

    def get_message(self, message):
        ts_parser = TextSearchParser(self.es_connection, message)
        return ts_parser.parse()

    def get_property(self, **kwargs):
        es_helper = ElasticSearchHelper(self.es_connection)
        datas = es_helper.search_property(**kwargs)
        return datas

    def parser(self, message):
        model_search = self.get_message(message)
        return self.get_property(**model_search)

    @staticmethod
    def get_elasticsearch_config():
        return {
            'hosts': ['it.urbanindo.id'],
            'port': 9200,
            'use_ssl': False
        }
