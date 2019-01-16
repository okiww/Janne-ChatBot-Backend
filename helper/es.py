from elasticsearch import TransportError


_INDEX_SMARTSEARCH = 'smartsearch'
_TYPE_LOCATION = 'location'
_TYPE_KEYWORD = 'keyword'


def simplify_es_result_for_helper(result):
    """Convert ES result to simple dict.
    """
    source = result['_source']
    alias = None
    venue_id = None

    if 'alias' in source:
        alias_len = len(source['alias'])
        if alias_len > 0:
            alias = str(source['alias'])
    if 'venueId' in source:
        if isinstance(source['venueId'], int):
            venue_id = source['venueId']
        else:
            venue_id_len = len(source['alias'])
            if venue_id_len > 0:
                venue_id = int(source['venueId'])
    return {
        'text': str(source['text']),
        'province': str(source['province']) if 'province' in source else None,
        'city': str(source['city']) if 'city' in source else None,
        'sublocality1': str(source['sublocality1']) if 'sublocality1' in source else None,
        'sublocality2': str(source['sublocality2']) if 'sublocality2' in source else None,
        'alias': alias,
        'venueId': venue_id
    }


class ElasticSearchHelper(object):
    """Wraps general functions for Elastic search operations"""

    def __init__(self, elasticsearch):
        self.connection = elasticsearch

    def search_by_query(self, _index, doc_type, size, query_body):
        search = self.connection.search(
            index=_index,
            doc_type=doc_type,
            size=size,
            body=query_body
        )
        hits_len = len(search['hits']['hits'])

        if hits_len == 0:
            return None, hits_len

        return search['hits']['hits'], hits_len

    def is_exists(self, _id, index=_INDEX_SMARTSEARCH, doc_type=_TYPE_LOCATION):
        """Checks whether a location is already stored in elasticsearch
        :param _id: string of id to be checked.
        :param index: index in elasticsearch.
        :param doc_type: doc_type in elasticsearch.
        :return: boolean whether the location exists
        """
        try:
            return self.connection.exists(index=index, doc_type=doc_type, id=_id)
        except TransportError:
            return False

    def is_keyword_exists(self, keyword):
        """Checks whether a keyword is already stored in elasticsearch
        :param keyword: string of keyword to be checked.
        :return: boolean whether the keyword exists
        """
        try:
            return self.connection.exists(index=_INDEX_SMARTSEARCH, doc_type=_TYPE_KEYWORD, id=keyword)
        except TransportError:
            return False

    def is_location_exists(self, location):
        """Checks whether a location is already stored in elasticsearch
        :param location: string of location to be checked.
        :return: boolean whether the location exists
        """
        try:
            return self.connection.exists(index=_INDEX_SMARTSEARCH, doc_type=_TYPE_LOCATION, id=location)
        except TransportError:
            return False

    def search_province(self, province, size=1):
        """Get province in elasticsearch location
        :return list of dict of text and alias if exists
        """
        query_body = {
            "query": {
                "filtered": {
                    "query": {
                        "bool": {
                            "must": [
                                {
                                    "match": {
                                        "province": province
                                    }
                                },
                                {
                                    "match": {
                                        "text": province
                                    }
                                }
                            ]
                        }
                    },
                    "filter": {
                        "missing": {
                            "field": "city"
                        }
                    }
                }
            }
        }

        try:
            hits, hits_len = self.search_by_query(_INDEX_SMARTSEARCH, _TYPE_LOCATION, size, query_body)
            if hits_len == 0:
                return None
        except TransportError:
            return None

        return [simplify_es_result_for_helper(result) for result in hits]

    def search_city(self, city, province=None, size=10):
        """Get City by province (optional) & city in elasticsearch location
        :return list of dict of text and alias if exists
        """
        must = list()

        if province:
            must.append({"match": {"province": province}})

        must.append({"match": {"city": city}})
        must.append({"match": {"text": city}})

        query_body = {
            "query": {
                "filtered": {
                    "query": {
                        "bool": {
                            "must": must
                        }
                    },
                    "filter": {
                        "and": [
                            {
                                "missing": {
                                    "field": "sublocality1"
                                }
                            },
                            {
                                "missing": {
                                    "field": "district"
                                }
                            }
                        ]
                    }
                }
            }
        }
        try:
            hits, hits_len = self.search_by_query(_INDEX_SMARTSEARCH, _TYPE_LOCATION, size, query_body)
            if hits_len == 0:
                return None
        except TransportError:
            return None

        return [simplify_es_result_for_helper(result) for result in hits]

    def search_sublocality1(self, sublocality1, city=None, size=10):
        """Get Sublocality1 by city (optional) & sublocality1 in elasticsearch location
        :return list of dict of text and alias if exists
        """
        must = list()

        if city:
            must.append({"match": {"city": city}})

        must.append({"match": {"sublocality1": sublocality1}})

        query_body = {
            "query": {
                "filtered": {
                    "query": {
                        "bool": {
                            "must": must
                        }
                    }
                }
            }
        }
        try:
            hits, hits_len = self.search_by_query(_INDEX_SMARTSEARCH, _TYPE_LOCATION, size, query_body)
            if hits_len == 0:
                return None
        except TransportError:
            return None

        return [simplify_es_result_for_helper(result) for result in hits]
