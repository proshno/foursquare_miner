import traceback
from utils import _attr_warn
from base_object import BaseObject


class Friend(BaseObject):
    def __init__(self, soup):
        BaseObject.__init__(self, soup)

        self.friend_name = ''
        self.friend_url = ''

        self._extract_attrs()


    def _extract_attrs(self):
        with _attr_warn: self.friend_name = self._soup.a.string
        with _attr_warn:  self.friend_url = self._soup.a['href']

