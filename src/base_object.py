from BeautifulSoup import BeautifulSoup


class BaseObject(object):
    def __init__(self, soup):
        self._soup = soup


    def attrs(self):
        return dict(filter(lambda (k, v): not k.startswith('_'), self.__dict__.items()))

