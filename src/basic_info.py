import re
import traceback
from utils import _attr_warn
from base_object import BaseObject


class BasicInfo(BaseObject):
    def __init__(self, soup):
        BaseObject.__init__(self, soup)

        self.user_name = ''
        self.user_pic_url = ''
        self.user_location = ''
        self.days_out_count = 0
        self.check_ins_count = 0
        self.things_done_count = 0
        self.user_twitter_url = ''
        self.user_facebook_url = ''

        self._extract_attrs()


    def _extract_attrs(self):
        data_soup = self._soup.find('div', {'class': 'data'})
        pic_soup = self._soup.find('div', {'class': 'pic'})
        count_soup = data_soup.findAll('strong')
        links_soup = data_soup.find('div', {'class': 'links'}).findAll('a')
        user_links = dict([(re.findall(r'(?:twitter.com)|(?:facebook.com)', link['href'])[0], link['href']) \
                            for link in links_soup])

        with _attr_warn: self.user_name = data_soup.h1.string
        with _attr_warn: self.user_pic_url = pic_soup.a['href']
        with _attr_warn: self.user_location = data_soup.h2.string
        with _attr_warn: self.days_out_count = int(count_soup[0].string.replace(',', ''))
        with _attr_warn: self.check_ins_count = int(count_soup[1].string.replace(',', ''))
        with _attr_warn: self.things_done_count = int(count_soup[2].string.replace(',', ''))
        with _attr_warn: self.user_twitter_url = user_links['twitter.com']
        with _attr_warn: self.user_facebook_url = user_links['facebook.com']

