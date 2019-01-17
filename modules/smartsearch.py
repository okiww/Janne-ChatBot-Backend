from elasticsearch import Elasticsearch
from helper.es import ElasticSearchHelper
from helper.parser.general import TextSearchParser

_PROPERTY_TYPE = 'property_type'
_LISTING_TYPE = 'listing_type'
_LOCATION_OBJECT = 'location_object'
_PROVINCE = 'province'
_CITY = 'city'
_SUB_LOCAL1 = 'sublocality1'
_SUB_LOCAL2 = 'sublocality2'


class SmartSearch(object):
    models = dict()

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
        if message == 'mohon maaf, tolong masukan informasi yang lebih spesifik lagi':
            return message

        msgs = self.get_message(message)

        # set self.model_search if None
        if not self.models:
            self.models.update(msgs)

        print("-------------------------------------------------------------------------------------------------------")
        print("[DEBUG] Message : {}".format(message))
        print("[DEBUG] Before msgs: {}".format(self.models))

        if 'min_price' in msgs and 'max_price' in msgs:
            if msgs['min_price'] and msgs['max_price']:
                # set location object
                if _LOCATION_OBJECT in msgs:
                    loc_object = msgs[_LOCATION_OBJECT]

                    if _PROVINCE in loc_object and loc_object[_PROVINCE] is not None:
                        self.models[_LOCATION_OBJECT][_PROVINCE] = msgs[_LOCATION_OBJECT][_PROVINCE]
                        self.models[_LOCATION_OBJECT][_CITY] = msgs[_LOCATION_OBJECT][_CITY]
                        self.models[_LOCATION_OBJECT][_SUB_LOCAL1] = msgs[_LOCATION_OBJECT][_SUB_LOCAL1]
                        self.models[_LOCATION_OBJECT][_SUB_LOCAL2] = msgs[_LOCATION_OBJECT][_SUB_LOCAL2]
                    else:
                        msgs[_LOCATION_OBJECT][_PROVINCE] = self.models[_LOCATION_OBJECT][_PROVINCE]
                        msgs[_LOCATION_OBJECT][_CITY] = self.models[_LOCATION_OBJECT][_CITY]
                        msgs[_LOCATION_OBJECT][_SUB_LOCAL1] = self.models[_LOCATION_OBJECT][_SUB_LOCAL1]
                        msgs[_LOCATION_OBJECT][_SUB_LOCAL2] = self.models[_LOCATION_OBJECT][_SUB_LOCAL2]

                # set property type
                if _PROPERTY_TYPE in msgs and msgs[_PROPERTY_TYPE] is not None and msgs[_PROPERTY_TYPE] != -1:
                    self.models[_PROPERTY_TYPE] = msgs[_PROPERTY_TYPE]
                else:
                    msgs[_PROPERTY_TYPE] = self.models[_PROPERTY_TYPE]

                # set listing type
                if _LISTING_TYPE in msgs and msgs[_LISTING_TYPE] is not None and msgs[_LISTING_TYPE] != -1:
                    self.models[_LISTING_TYPE] = msgs[_LISTING_TYPE]
                else:
                    msgs[_LISTING_TYPE] = self.models[_LISTING_TYPE]
            else:
                self.models.update(msgs)

        print("[DEBUG] After msgs: {}".format(msgs))
        print("-------------------------------------------------------------------------------------------------------")

        return self.get_property(**msgs)

    @staticmethod
    def get_elasticsearch_config():
        return {
            'hosts': ['it.urbanindo.id'],
            'port': 9200,
            'use_ssl': False
        }
