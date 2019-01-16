import re
from helper.parser import Parser

_MIN_PRICE = 'min_price'
_MAX_PRICE = 'max_price'


def compile_regex_member(line, prefix=None):
    """Compile the 'regex' component of a dict."""
    regex = line['regex']
    if prefix is not None:
        regex = prefix + regex
    line['regex'] = re.compile(regex)
    return line


class PriceParser(Parser):
    """Parse price from text search."""

    _ignore_price = re.compile(r'\b(harga)\b')
    _suffix = [
        {'value': 1000, 'regex': r'(\d+)\s*(ribuan|ribu|rb)\b'},
        {'value': 1000000, 'regex': r'(\d+)\s*(jutaan|juta|jtan|jt)\b'},
        {'value': 1000000000, 'regex': r'(\d+)\s*(miliaran|milyaran|miliar|milyar|mil)\b'}
    ]
    _regexes = [compile_regex_member(x) for x in [
        {'value': 1000, 'regex': r'(\d+)\s*(ribuan|ribu|rb)\b'},
        {'value': 1000000, 'regex': r'(\d+)\s*(jutaan|juta|jtan|jt)\b'},
        {'value': 1000000000, 'regex': r'(\d+)\s*(miliaran|milyaran|miliar|milyar|mil)\b'}
    ]]

    def __init__(self, residue):
        super().__init__(residue)
        self.residue_new = None
        self._max_regex = None
        self._min_regex = None
        self._exact_regex = None

        self.remove_residue_price(residue)

    def remove_residue_price(self, residue):
        residue = self.remove_words_by_regex(self._ignore_price, residue)[0]
        self.residue_new = residue.replace(';', '')

    def parser_price(self):
        # get min range
        for line in self._regexes:
            min_price = self.parse(line)
            if min_price is not None:
                self.parser[_MIN_PRICE] = min_price
                break

        # get max range
        for line in self._regexes:
            max_price = self.parse(line)
            if max_price is not None:
                self.parser[_MAX_PRICE] = max_price
                break

    def parse(self, item, result_group=1):
        """Get matching regex and value from list of regex
        :return the value
        """
        _regex = item['regex']
        multiplier = item['value']
        result = self.search_regex_in_residue(_regex)
        if result:
            self.remove_regex_result_from_residue(result)
            value = int(result.group(result_group)) * multiplier
            return value
        return None
