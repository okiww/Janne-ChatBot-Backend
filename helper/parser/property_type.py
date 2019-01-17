import re
from helper.parser import Parser

_PROPERTY_TYPE = 'property_type'

ANY_TYPE = -1
HOUSE = 0
APARTMENT = 1
RUKO = 2
VILLA = 3
COMMERCIAL = 4
LAND = 5
ROOM = 6
OFFICE_SPACE = 7
WAREHOUSE = 8
HOTEL = 9
KIOSK = 10
FACTORY = 11
MULTI_STOREY_BUILDING = 12
CONDOTEL = 13
STORE = 14


def compile_regex_member(line, prefix=None):
    """Compile the 'regex' component of a dict."""
    regex = line['regex']
    if prefix is not None:
        regex = prefix + regex
    line['regex'] = re.compile(regex)
    return line


class PropertyTypeParser(Parser):
    """Parse property type from regex rules"""

    _regexes = [compile_regex_member(x) for x in [
        {'value': HOUSE, 'regex': r'\b(rumah kostan|rumah kosan|rumah kost'
                                  r'|town house|rumah kos|townhouse|rumah'
                                  r'|rmh|perumahan)\b'},
        {'value': APARTMENT, 'regex': r'\b(apartement|apartment'
                                      r'|apartemen|apartmen)\b'},
        {'value': RUKO, 'regex': r'\b(ruko)\b'},
        {'value': VILLA, 'regex': r'\b(villa|vila)\b'},
        {'value': COMMERCIAL, 'regex': r'\b(komersial)\b'},
        {'value': LAND, 'regex': r'\b(tanah kavling|tanah kapling|'
                                 r'kapling|kavling|lahan|kebun|tanah|sawah|tnh)\b'},
        {'value': ROOM, 'regex': r'\b(koskosan|kostan|kosan|kos|kost)\b'},
        {'value': OFFICE_SPACE, 'regex': r'\b(kantor|perkantoran)\b'},
        {'value': WAREHOUSE, 'regex': r'\b(gudang)\b'},
        {'value': HOTEL, 'regex': r'\b(hotel)\b'},
        {'value': KIOSK, 'regex': r'\b(kios|kiosk)\b'},
        {'value': FACTORY, 'regex': r'\b(pabrik)\b'},
        {'value': MULTI_STOREY_BUILDING, 'regex': r'\b(gedung(\w+bertingkat)?)\b'},
        {'value': CONDOTEL, 'regex': r'\b(kondotel|condotel)\b'},
        {'value': STORE, 'regex': r'\btoko\b'},
    ]]

    _keyword_filters = [re.compile(regex) for regex in [r'\btanah \w+\b', r'\brumah \w+\b']]

    def __init__(self, eshelper, residue):
        """Constructor
        :param parser: TextSearchParser object to be parsed.
        :param eshelper: ElasticSearchHelper object to help finding keyword from ES.
        """
        super(PropertyTypeParser, self).__init__(residue)
        self.parser[_PROPERTY_TYPE] = -1
        self.filter_existing_keywords(eshelper)

    def filter_existing_keywords(self, eshelper):
        """Finds whether there is `tanah` or `rumah` in keyword, e.g. `tanah abang`
        """
        text = self.residue
        for keyword_regex in self._keyword_filters:
            for match in keyword_regex.findall(text):
                if eshelper.is_keyword_exists(match) or eshelper.is_location_exists(match):
                    self.remove_words_from_residue(match)

    def parse_property_type_in_residue(self):
        """Find the regexes and tag the type."""
        text = self.residue
        for type_regex in self._regexes:
            result = self.remove_words_by_regex(type_regex['regex'], text)
            if result[1]:
                self.parser[_PROPERTY_TYPE] = type_regex['value']
                self.residue = result[0]
                break
        return self.residue
