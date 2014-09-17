import traceback
from utils import _attr_warn
from base_object import BaseObject


class Badge(BaseObject):
    def __init__(self, soup):
        BaseObject.__init__(self, soup)

        self.badge_name = ''
        self.badge_url = ''
        #self.badge_img_url = ''

        self._extract_attrs()


    def _extract_attrs(self):
        with _attr_warn: self.badge_name = self._soup.img['alt']
        with _attr_warn: self.badge_url = self._soup['href']
        #with _attr_warn: self.badge_img_url = self._soup.a.img['src']

