import re
from helper.parser import Parser

VAR_PROVINCE = 'province'
VAR_CITY = 'city'
VAR_SUB_LOCAL1 = 'sublocality1'
VAR_SUB_LOCAL2 = 'sublocality2'
_LOCATION_OBJECT = 'location_object'


class LocationParser(Parser):
    def __init__(self, eshelper, residue):
        super(LocationParser, self).__init__(residue)
        self.eshelper = eshelper
        self.location_object = {
            VAR_PROVINCE: None,
            VAR_CITY: None,
            VAR_SUB_LOCAL1: None,
            VAR_SUB_LOCAL2: None
        }
        self._ignore_location = None

    def parse_locations_in_residue(self):
        # remove keyword 'cari'
        for _key in ['cari', 'mencari', 'carikan']:
            self.remove_words_from_residue(_key)

        # change symbol '?' to ''
        if '?' in self.residue:
            self.residue = self.residue.replace('?', '')

        if any(s in self.residue for s in self.list_special_city()):
            if self.residue:
                self.set_city_location_object()

            if self.residue:
                self.set_province_location_object()
        else:
            if self.residue:
                self.set_province_location_object()
            if self.residue:
                self.set_city_location_object(self.location_object.get('province'))

        if self.residue:
            self.set_subloc1_location_object(self.location_object.get('city'))

        self.parser[_LOCATION_OBJECT] = self.location_object
        return self.residue

    @staticmethod
    def list_special_city():
        """List special cities
        Special city is a city that contains the name of the province.
        :return list special city
        """
        return [line.rstrip('\n') for line in open('files/special_cities.txt')]

    def remove_ignored_locations(self):
        """remove ignored location"""
        self.residue = self.remove_words_by_regex(self._ignore_location, self.residue)[0]

    def ignore_remove_location(self, location):
        """
        Remove ignore location
        :param location : string location
        """
        # old regex : \b(((di\s)?(kota(?!\swisata)|kabupaten|kawasan|
        # kompleks|alamat|sekitar|daerah)?|di)\s{0}+)\b
        self._ignore_location = re.compile(r'\b(((di\s)?(kota(?!\swisata)'
                                           r'|kabupaten|kawasan|kompleks|alamat'
                                           r'|sekitar|daerah)'
                                           r'?|di){0}+)\b'.format(location))
        self.remove_ignored_locations()

    def set_province_location_object(self):
        """
        Set province in location object
        :return string
        """
        provinces = self.eshelper.search_province(self.residue)
        if provinces:
            province = provinces[0][VAR_PROVINCE]
            self.location_object[VAR_PROVINCE] = province
            self.ignore_remove_location(province)
            self.remove_words_from_residue(province)
            return province
        return None

    def set_city_location_object(self, province=None):
        """
        Set cities in location object
        :param province: province
        :return string
        """
        cities = self.eshelper.search_city(self.residue, province)
        if cities:
            city = cities[0][VAR_CITY]
            if province is None:
                self.location_object[VAR_PROVINCE] = cities[0][VAR_PROVINCE]
            self.location_object[VAR_CITY] = city
            self.ignore_remove_location(city)
            self.remove_words_from_residue(city)
            return city
        return None

    def set_subloc1_location_object(self, city=None):
        """
        Set sublocality1 in location object
        :param city: City
        :return string
        """
        sublocalites = self.eshelper.search_sublocality1(self.residue, city)
        if sublocalites:
            sublocality1 = sublocalites[0][VAR_SUB_LOCAL1]
            if city is None:
                self.location_object[VAR_PROVINCE] = sublocalites[0][VAR_PROVINCE]
                self.location_object[VAR_CITY] = sublocalites[0][VAR_CITY]
            self.location_object[VAR_SUB_LOCAL1] = sublocality1
            self.ignore_remove_location(sublocality1)
            self.remove_words_from_residue(sublocality1)
            return sublocality1
        return None
