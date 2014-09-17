import sys
import pdb
import traceback
from Queue import Queue
from optparse import OptionParser
from urllib2 import HTTPError

from scraper_utils import *
from pg_escaper import escape_row
from user_profile import UserProfile
from lib.break_handler import BreakHandler


class ProfileRetriever(object):
    def __init__(self, urls_file_path):
        self.urls_file_path = urls_file_path

        self.urls_queue_file_path = "%s.queue" % urls_file_path
        self.urls_done_file_path = "%s.done" % urls_file_path
        self.profiles_file_path = "%s.profiles" % urls_file_path
        self.friends_file_path = "%s.friends" % urls_file_path
        self.badges_file_path = "%s.badges" % urls_file_path
        self.mayorships_file_path = "%s.mayorships" % urls_file_path
        self.tips_file_path = "%s.tips" % urls_file_path
        self.queue_fd = None
        self.done_fd = None
        self.profiles_fd = None
        self.friends_fd = None
        self.badges_fd = None
        self.mayorships_fd = None
        self.tips_fd = None

        self.urls_queue = Queue()
        self.urls_done = {}


    def retrieve_queue_urls(self):
        self.queue_fd.seek(0)
        for queue_url in self.queue_fd:
            self.urls_queue.put(queue_url[:-1], block=False)


    def store_queue_url(self, url_data):
        print >> self.urls_queue, url_data
        self.urls_queue.put(url_data, block=False)


    def sync_queue_urls(self):
        fd = open(self.urls_queue_file_path, 'wt')
        while not self.urls_queue.empty():
            queue_url = self.urls_queue.get(block=False)
            print >> fd, queue_url
        fd.close()


    def retrieve_done_urls(self):
        self.done_fd.seek(0)
        for done_url in self.done_fd:
            self.urls_done[done_url[:-1]] = True


    def store_done_url(self, url_data):
        print >> self.done_fd, url_data
        self.urls_done[url_data] = True


    def sync_done_urls(self):
        fd = open(self.urls_done_file_path, 'wt')
        for done_url in self.urls_done:
            print >> fd, done_url
        fd.close()


    def retrieve_seed_urls(self):
        fd = open(self.urls_file_path, 'rt')
        for seed_url in fd:
            self.urls_queue.put(seed_url[:-1], block=False)
        fd.close()


    def open_data_files(self):
        self.queue_fd = open(self.urls_queue_file_path, 'a+')
        self.done_fd = open(self.urls_done_file_path, 'a+')
        self.profiles_fd = open(self.profiles_file_path, 'a')
        self.friends_fd = open(self.friends_file_path, 'a')
        self.badges_fd = open(self.badges_file_path, 'a')
        self.mayorships_fd = open(self.mayorships_file_path, 'a')
        self.tips_fd = open(self.tips_file_path, 'a')

        print "Retrieving previously queued user urls..."
        self.retrieve_queue_urls()

        print "Retrieving already downloaded user urls..."
        self.retrieve_done_urls()


    def close_data_files(self):
        self.queue_fd.close()
        self.done_fd.close()
        self.profiles_fd.close()
        self.friends_fd.close()
        self.badges_fd.close()
        self.mayorships_fd.close()
        self.tips_fd.close()


    def store_user_data(self, profile):
        if profile.basic_info:
            escaped_profile_row = escape_row([
                    profile.user_profile_url, \
                    profile.basic_info.user_name, \
                    profile.basic_info.user_pic_url, \
                    profile.basic_info.user_location, \
                    profile.basic_info.days_out_count, \
                    profile.basic_info.check_ins_count, \
                    profile.basic_info.things_done_count,
                    profile.badges_count, \
                    profile.mayorships_count, \
                    profile.friends_count, \
                    profile.basic_info.user_twitter_url, \
                    profile.basic_info.user_facebook_url])
            self.profiles_fd.write(escaped_profile_row)
        else:
            print "No basic info found to store!"

        if profile.friends:
            for friend in profile.friends:
                escaped_friend_row = escape_row([
                        profile.user_profile_url, \
                        friend.friend_name, \
                        friend.friend_url])
                self.friends_fd.write(escaped_friend_row)
        else:
            print "No friend info found to store!"


        if profile.badges:
            for badge in profile.badges:
                escaped_badge_row = escape_row([
                        profile.user_profile_url, \
                        badge.badge_name, \
                        badge.badge_url])
                self.badges_fd.write(escaped_badge_row)
        else:
            print "No badge info found to store!"


        if profile.mayorships:
            for mayorship in profile.mayorships:
                escaped_mayorship_row = escape_row([
                        profile.user_profile_url, \
                        mayorship.venue_name, \
                        mayorship.venue_location, \
                        mayorship.venue_url])
                self.mayorships_fd.write(escaped_mayorship_row)
        else:
            print "No mayorship info found to store!"


        if profile.tips:
            for tip in profile.tips:
                escaped_tip_row = escape_row([
                        profile.user_profile_url, \
                        tip.venue_name, \
                        tip.venue_url, \
                        tip.tip_text, \
                        tip.actions_count, \
                        tip.action_url, \
                        tip.action_date, \
                        tip.action_location])
                self.tips_fd.write(escaped_tip_row)
        else:
            print "No tip info found to store!"



    def start_retrieval(self):
        print "Initializing the data files..."
        self.open_data_files()

        if self.urls_queue.empty():
            print "Retrieving the seed user urls..."
            self.retrieve_seed_urls()

        bh = BreakHandler()
        bh.enable()
        try:
            while not self.urls_queue.empty():
                curr_uri = self.urls_queue.get(block=False)
                curr_url = curr_uri if curr_uri.startswith(BASE_URL) \
                                    else BASE_URL + curr_uri

                if not self.urls_done.has_key(curr_uri):
                    print "Retrieving the user url: %s" % curr_url
                    try:
                        profile = self.retrieve_user_profiles(curr_url)

                        if profile.is_valid():
                            print "Storing the user profile date..."
                            self.store_user_data(profile)
                        else:
                            print "URL doesn't contain valid profile data!"

                        self.store_done_url(curr_uri)
                    except Exception, e:
                        traceback.print_exc()
                else:
                    print "The user url %s is already downloaded" % curr_url

                if bh.trapped:
                    print "*** Aborting by user request ***"
                    break
        finally:
            print "Finalizing the data files..."
            self.sync_queue_urls()
            self.close_data_files()

            bh.disable()


    def retrieve_user_profiles(self, user_profile_url):
        raw_html = download_url(user_profile_url)
        profile_soup = BeautifulSoup.BeautifulSoup(raw_html, convertEntities=BeautifulSoup.BeautifulSoup.HTML_ENTITIES)
        user_profile = UserProfile(profile_soup, user_profile_url)

        for friend in user_profile.friends:
            self.urls_queue.put(friend.friend_url, block=False)

        return user_profile


if __name__ == '__main__':
    profile_retriever = ProfileRetriever(sys.argv[1])

    stdout_backup = sys.stdout
    sys.stdout = sys.stderr
    try:
        profile_retriever.start_retrieval()
    finally:
        sys.stdout = stdout_backup
