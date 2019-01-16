
_LOCATION_OBJECT = 'location_object'
_LISTING_TYPE = 'listing_type'
_PROPERTY_TYPE = 'property_type'
_MIN_PRICE = 'min_price'
_MAX_PRICE = 'max_price'


class Parser(object):
    parser = {
        _LOCATION_OBJECT: None,
        _LISTING_TYPE: -1,
        _PROPERTY_TYPE: -1,
        _MIN_PRICE: None,
        _MAX_PRICE: None
    }

    def __init__(self, residue=None):
        self.residue = residue
        if self.is_residue_empty():
            pass

    @staticmethod
    def remove_words_from_string(words, subject):
        """Remove words from string.
        The removal will replace every matched word with string `-`.
        :param words: String containing words.
        :param subject: String to be searched for replacing.
        :return string with replaced words.
        """
        replace = ('; ' * (words.strip().count(' ') + 1)).strip()
        return subject.replace(words, replace, 1)

    def is_residue_empty(self):
        """
        :return boolean
        """
        residue = self.residue
        without_dash = residue.replace(";", "")
        without_space = without_dash.replace(" ", "").strip()
        return len(without_space) == 0

    def remove_words_by_regex(self, regex, subject):
        """Remove words in string based on regex.
        The removal will replace every words matched by the regex with string `-`
        :param regex: The regex object.
        :param subject: The string to substitute.
        :return tuple of string result and boolean whether there is substitution or not.
        """
        result = regex.search(subject)
        if result is None:
            return tuple([subject, False])
        replaced = self.remove_words_from_string(result.group(0), subject)
        return tuple([replaced, True])

    def remove_words_from_residue(self, words):
        """Replaces words in the residue with '-'
        E.g. 'rumah dijual di bandung' against 'rumah dijual' will result in
        '- - di bandung'
        :param words: string containing words.
        """
        self.residue = self.remove_words_from_string(words, self.residue)

    def search_regex_in_residue(self, regex):
        """Search regex in residue
        :param regex: regex object
        :return regex result object
        """
        return regex.search(self.residue)

    def remove_regex_result_from_residue(self, result, group=0):
        # pylint: disable=invalid-name
        """Search regex in residue
        :param result: result object
        :param group: group
        :return regex result object
        """
        self.remove_words_from_residue(result.group(group))
