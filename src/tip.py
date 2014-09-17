import traceback
from utils import _attr_warn
from base_object import BaseObject


class Tip(BaseObject):
    def __init__(self, soup):
        BaseObject.__init__(self, soup)

        self.venue_name = ''
        self.venue_url = ''
        self.tip_text = ''
        self.actions_count = 0
        self.action_url = ''
        self.action_date = ''
        self.action_location = ''

        self._extract_attrs()


    def _extract_attrs(self):
        with _attr_warn: self.venue_name = self._soup.h3.a.string
        with _attr_warn: self.venue_url = self._soup.h3.a['href']
        with _attr_warn: self.tip_text = self._soup.p.string[1:-1].strip()
        with _attr_warn: self.actions_count = int(self._soup.find('span', {'class': 'doneCount'}). \
                                                  span.string)
        with _attr_warn: self.action_url = self._soup.find('span', {'class': 'date'}).a['href']
        with _attr_warn: self.action_date = self._soup.find('span', {'class': 'date'}).a.string
        with _attr_warn: self.action_location = self._soup.find('span', {'class': 'location'}).string

