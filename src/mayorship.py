import traceback
from utils import _attr_warn
from base_object import BaseObject


class Mayorship(BaseObject):
    def __init__(self, soup):
        BaseObject.__init__(self, soup)

        self.venue_name = ''
        self.venue_location = ''
        self.venue_url = ''

        self._extract_attrs()


    def _extract_attrs(self):
        with _attr_warn: self.venue_name = self._soup.h3.a.string
        with _attr_warn: self.venue_location = self._soup.p.string.strip()
        with _attr_warn: self.venue_url = self._soup.h3.a['href']

