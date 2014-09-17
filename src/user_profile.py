import re
import traceback

from scraper_utils import BASE_URL
from base_object import BaseObject
from basic_info import BasicInfo
from badge import Badge
from mayorship import Mayorship
from friend import Friend
from tip import Tip


class UserProfile(BaseObject):
    def __init__(self, soup, profile_url):
        BaseObject.__init__(self, soup)

        self.user_profile_url = profile_url[len(BASE_URL):]
        self.basic_info = None
        self.badges_count = 0
        self.mayorships_count = 0
        self.friends_count = 0
        self.badges = []
        self.mayorships = []
        self.friends = []
        self.tips = []

        self._extract_attrs()


    def _extract_attrs(self):
        print "Retrieving the basic profile info..."
        self.extract_basic_info()

        if not self.is_valid():
            print "Ignoring further parsing, " \
                  "since required profile info is not found!"
            return

        print "Retrieving the user basdges info..."
        self.extract_badges()

        print "Retrieving the user mayorships info..."
        self.extract_mayorships()

        print "Retrieving the user friends info..."
        self.extract_friends()

        print "Retrieving the user tips info..."
        self.extract_tips()


    def _build_items(self, items_soup, count_soup, Item):
        items_count_temp = re.findall(r'([,0-9]+)', count_soup.p.string) if count_soup else None
        items_count = int(items_count_temp[0].replace(',', '')) if items_count_temp else 0

        items = []
        for item_soup in items_soup:
            try:
                items.append(Item(item_soup))
            except:
                pass
 
        return items, items_count


    def is_valid(self):
        if self.basic_info:
            return True

        return False


    def is_empty(self):
        if self.basic_info or self.badges or self.mayorships or self.friends or self.tips:
            return False

        return True


    def extract_badges(self):
        try:
            container_soup = self._soup.find('div', {'class': 'badges top contentContainer'})
            items_soup = container_soup.find('div', {'class': 'grayBox flatTop minimizedBox'}).findAll('a')
            count_soup = container_soup.find('div', {'class': 'header'})

            self.badges, self.badges_count = self._build_items(items_soup, count_soup, Badge)
        except AttributeError, e:
            print "No badge info found!"
        except:
            traceback.print_exc()
            pass

    def extract_mayorships(self):
        try:
            container_soup = self._soup.find('div', {'class': 'top contentContainer mayorships'})
            items_soup = container_soup.find('div', {'class': 'grayBox flatTop minimizedBox'}). \
                                        findAll('div', {'class': 'content'})
            count_soup = container_soup.find('div', {'class': 'header'})

            self.mayorships, self.mayorships_count = self._build_items(items_soup, count_soup, Mayorship)
        except AttributeError, e:
            print "No mayorship info found!"
        except:
            traceback.print_exc()
            pass


    def extract_tips(self):
        try:
            container_soup = self._soup.find('div', {'id': 'tipsList'})
            items_soup = container_soup.find('div', {'class': 'tips'}). \
                                        findAll('div', {'class': 'content'})
            count_soup = None

            self.tips, _ = self._build_items(items_soup, count_soup, Tip) 
        except AttributeError, e:
            print "No tip info found!"
        except:
            traceback.print_exc()
            pass



    def extract_friends(self):
        try:
            container_soup = self._soup.find('div', {'class': 'top friends contentContainer'})
            items_soup = container_soup.find('div', {'class': 'grayBox flatTop'}). \
                                        findAll('span', {'class': 'friendName'})
            count_soup = container_soup.find('div', {'class': 'header'})

            self.friends, self.friends_count = self._build_items(items_soup, count_soup, Friend) 
        except AttributeError, e:
            print "No friend info found!"
        except:
            traceback.print_exc()
            pass



    def extract_basic_info(self):
        try:
            container_soup = self._soup.find('div', {'class': 'leftColumn'})
            item_soup = container_soup.find('div', {'id': 'userInfo'})

            self.basic_info = BasicInfo(item_soup)
            #return self._build_items(items_soup, count_soup, BasicInfo)       
        except AttributeError, e:
            print "No basic info found!"
        except:
            traceback.print_exc()
            pass

