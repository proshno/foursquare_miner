from scraper_utils import *


def retrieve_user_urls_from_brand(brand_page_url, target_file):
    users_fd = open(target_file, 'w')

    uniq_users = {}
    consecutive_not_found_new = 0
    while True:
        raw_html = download_url(brand_page_url)
        soup = BeautifulSoup.BeautifulSoup(raw_html)

        users_soup = soup.find('table', {'class': 'user_grid'}). \
                          findAll('td')

        count_new = 0
        for user in users_soup:
            user_url = "%s%s" % (BASE_URL, user.find('a')['href'])
            user_name = user.find('img')['title']

            if not uniq_users.get(user_url):
                count_new += 1
                print "%d. %s" % (count_new, user_url)
                print >> users_fd, user_url
                uniq_users[user_url] = user_name

        if not count_new:
            print "No new user found"
            consecutive_not_found_new += 1
        else:
            users_fd.flush()
            os.fsync(users_fd)
            print "%d new users found" % count_new
            consecutive_not_found_new = 0

        if consecutive_not_found_new > MAX_RETRIES:
            print "No new user found after %d consecutive refresh attempts!" % MAX_RETRIES
            break
        else:
            wait_time = REFRESH_DELAY * (consecutive_not_found_new + 1)
            print "Will refresh to get new users in %d seconds" % wait_time
            wait_progress(wait_time, SLEEP_TIME_RES)

    users_fd.close()


def is_valid_file(target_file):
    if os.path.exists(target_file) and os.path.getsize(target_file):
        return True

    return False


if __name__ == '__main__':
    brand_file = "../%s.%s" % (BRAND_FILE, FILE_EXT)
    brand_fd = open(brand_file, 'r')

    for brand_page_url in brand_fd.readlines():
        brand_page_url = brand_page_url[:-1]
        if not brand_page_url:
            continue

        brand_title = brand_page_url[brand_page_url.rfind('/') + 1:]
        print "Process brand: %s" % brand_title
        brand_user_file = "../%s/%s.%s.%s" % (BRAND_USER_FILE_PREFIX, BRAND_USER_FILE_PREFIX, brand_title, FILE_EXT)
        try:
            if not is_valid_file(brand_user_file):
                retrieve_user_urls_from_brand(brand_page_url, brand_user_file)
            else:
                print "Valid user urls file %s already exists" % brand_user_file
        except:
            traceback.print_exc()

    print "Possible user urls for all the brands in %s have been downloded" % brand_file
    brand_fd.close()

