import re
from helper.parser import Parser
from helper.es import ElasticSearchHelper
from helper.parser.price import PriceParser
from helper.parser.location import LocationParser
from helper.parser.listing_type import ListingTypeParser
from helper.parser.property_type import PropertyTypeParser


class TextSearchParser(Parser):
    """Parse text search.
    This is the general text search class to use.
    :field text is the string of original text search.
    :field residue is the string that contains latest text after parsing.
    """

    def __init__(self, elasticsearch, residue):
        super(TextSearchParser, self).__init__(residue)
        self.es_helper = ElasticSearchHelper(elasticsearch)

    @staticmethod
    def clean_text(text):
        """Clean text before parsing."""
        return re.sub(r'[^\w\d ]', '', text)

    def parse(self):
        """Runs the parsing sequence."""
        helper = self.es_helper
        self.residue = LocationParser(helper, self.residue).parse_locations_in_residue()
        self.residue = PropertyTypeParser(helper, self.residue).parse_property_type_in_residue()
        self.residue = ListingTypeParser(self.residue).parse_listing_type_in_residue()
        PriceParser(self.residue).parser_price()

        return self.parser
