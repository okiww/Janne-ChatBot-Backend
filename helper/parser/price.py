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
    _regexes = [compile_regex_member(x) for x in [
        {'value': 1000, 'regex': r'(\d+)\s*(ribuan|ribu|rb)\b'},
        {'value': 1000000, 'regex': r'(\d+)\s*(jutaan|juta|jtan|jt)\b'},
        {'value': 1000000000, 'regex': r'(\d+)\s*(miliaran|milyaran|miliar|milyar|mil)\b'}
    ]]

    _options_regex = [compile_regex_member(x) for x in [
        {'min_price': 100000000, 'max_price': 500000000, 'regex': r'(100 - 500jt)\b'},
        {'min_price': 500000000, 'max_price': 750000000, 'regex': r'(500 - 750jt)\b'},
        {'min_price': 750000000, 'max_price': 1000000000, 'regex': r'(750 - 1mily)\b'},
        {'min_price': 1000000000, 'max_price': 5000000000, 'regex': r'(1mily - 5mily)\b'}
    ]]

    def __init__(self, residue):
        super().__init__(residue)
        self.residue_new = None
        self.parser[_MIN_PRICE] = None
        self.parser[_MAX_PRICE] = None

        self.remove_residue_price(residue)

    def remove_residue_price(self, residue):
        residue = self.remove_words_by_regex(self._ignore_price, residue)[0]
        self.residue_new = residue.replace(';', '')

    def parser_price(self):
        for line in self._options_regex:
            min_price, max_price = self.parse_options(line)
            if min_price is not None and max_price is not None:
                self.parser[_MIN_PRICE] = min_price
                self.parser[_MAX_PRICE] = max_price
                break

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

    def parse_options(self, item, result_group=1):
        """Get matching regex and value from list of regex
        :return the value
        """
        _regex = item['regex']
        _min_price = item['min_price']
        _max_price = item['max_price']
        result = self.search_regex_in_residue(_regex)
        if result:
            self.remove_regex_result_from_residue(result)
            return _min_price, _max_price
        return None, None
