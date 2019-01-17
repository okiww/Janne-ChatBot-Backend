import re
from helper.parser import Parser

_LISTING_TYPE = 'listing_type'

ANY_TYPE = -1
FOR_SALE = 0
FOR_RENT = 1


def compile_regex_member(line, prefix=None):
    """Compile the 'regex' component of a dict."""
    regex = line['regex']
    if prefix is not None:
        regex = prefix + regex
    line['regex'] = re.compile(regex)
    return line


class ListingTypeParser(Parser):
    # pylint: disable=too-few-public-methods
    """Parse listing type based on regex."""

    _regexes = [compile_regex_member(x) for x in [
        {'value': FOR_SALE, 'regex': r'\b(jual\s*beli)\b'},
        {'value': FOR_SALE, 'regex': r'\b((di)?\s*(jual|beli))\b'},
        {'value': FOR_RENT, 'regex': r'\b((di)?\s*(kontrak|sewa))(\s*(an|kan))?\b'},
        {'value': None, 'regex': r'\b(dicari|cari|butuh)\b'}
    ]]

    def __init__(self, residue):
        """Constructor
        :param residue: Residue.
        """
        super(ListingTypeParser, self).__init__(residue)
        self.parser[_LISTING_TYPE] = -1

    def parse_listing_type_in_residue(self):
        """
        :return listing type and residue
        """
        original_text = self.residue
        for line in self._regexes:
            result = line['regex'].subn(';', original_text)
            if result[1] > 0 and line['value'] is not None:
                self.parser[_LISTING_TYPE] = line['value']
                return result[0]
        return self.residue
