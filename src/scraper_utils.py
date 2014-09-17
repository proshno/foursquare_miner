import os
import re
import pdb
import sys
import time
import urllib
import urllib2
import traceback
import BeautifulSoup


FILE_EXT = 'tsv'
BRAND_FILE = 'brand_urls'
BRAND_USER_FILE_PREFIX = 'brand_user_urls'
SLEEP_TIME_RES = 2
REFRESH_DELAY = 3 * SLEEP_TIME_RES
MAX_RETRIES = 5
HTTP_USER_AGENT = 'ArifReseachTool/1.0 (Linux; Arif B Abdullah; proshno@gmail.com)'
BASE_URL = 'http://foursquare.com'
SEED_AGGREGATOR_URL = '%s/proshno' % BASE_URL
HTTP_TIMEOUT = 5

DUMMY_COOKIE = '__utma=51454142.898864399.1287922339.1289282057.1289289916.24; __utmz=51454142.1289218329.20.6.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=http%3A%2F%2Ffoursquare.com%2Fjefrrychandra; _chartbeat2=6n4nmlsvq4phx779; __utmc=51454142; XSESSIONID=w5~57i3e7qnkt111ba5ez05wrnp3; LOCATION="37.7749295::-122.4194155::San Francisco, CA"'


def wait_progress(wait_time, wait_res):
    while wait_time:
        print '.',
        sys.stdout.flush()
        os.fsync(sys.stdout)
        time.sleep(wait_res)
        wait_time -= wait_res

    print ''
 

def download_url(target_url):
    headers = {'User-Agent': HTTP_USER_AGENT, 'Cookie': DUMMY_COOKIE}
    data = urllib.urlencode({})
    request = urllib2.Request(target_url, data, headers)

    curr_retry = 0
    while True:
        response = None
        try:
            response = urllib2.urlopen(request, timeout=HTTP_TIMEOUT)
            html_page = response.read()
            return html_page
        except Exception, e:
            traceback.print_exc()
            print "Error occurred in downloading %s" % target_url

            if curr_retry < MAX_RETRIES and \
               not (isinstance(e, urllib2.HTTPError) and e.code == 404):
                curr_retry += 1
                wait_time = SLEEP_TIME_RES ** curr_retry
                print "Will retry in %d seconds" % wait_time
                wait_progress(wait_time, SLEEP_TIME_RES)
            else:
                raise Exception("Failed to download %s" % target_url)
        finally:
            if response:
                response.close()

