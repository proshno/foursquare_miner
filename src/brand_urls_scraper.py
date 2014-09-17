from scraper_utils import *


def retrieve_brand_pages_from_4square(target_file):
    brands_fd = open(target_file, 'w')
    print >> brands_fd, "Brand page URL\tBrand logo URL"

    page_urls = []
    img_urls = []
    consecutive_not_found_new = 0
    while True:
        raw_html = download_url(SEED_AGGREGATOR_URL)
        soup = BeautifulSoup.BeautifulSoup(raw_html)

        brands_soup = soup.find('div', {'id': 'brandsFooter'}). \
                           find('div', {'class': 'outsideContainer'}). \
                           find('ul'). \
                           findAll('li')

        count_new = 0
        for brand in brands_soup:
            page_url = "%s%s" % (BASE_URL, brand.find('a')['href'])
            img_url = "%s%s" % (BASE_URL, brand.find('img')['src'])

            if page_url not in page_urls:
                count_new += 1
                print "%d. %s" % (count_new, page_url)
                print >> brands_fd, "%s\t%s" % (page_url, img_url)
                page_urls.append(page_url)
                img_urls.append(img_url)

        if not count_new:
            print "No new brand found"
            consecutive_not_found_new += 1
        else:
            brands_fd.flush()
            os.fsync(brands_fd)
            print "%d new brands found" % count_new
            consecutive_not_found_new = 0

        if consecutive_not_found_new > MAX_RETRIES:
            print "No new brand found after 5 consecutive refresh attempts!"
            break
        else:
            wait_time = REFRESH_DELAY * (consecutive_not_found_new + 1)
            print "Will refresh to get new brands in %d seconds" % wait_time
            wait_progress(wait_time, SLEEP_TIME_RES)

    brands_fd.close()


def retrieve_brand_pages_from_about4square(target_file):
    raw_html = download_url('http://aboutfoursquare.com/foursquare-brands/')
    brand_urls = re.findall(r'"(%s/[^/]*?)"' % BASE_URL, raw_html)
    #soup = BeautifulSoup.BeautifulSoup(raw_html)
    #brands_soup = soup.findAll('a', {'href': re.compile(r'%s/[^/]*$' % BASE_URL)})

    brands_fd = open(target_file, 'w')

    uniq_brand_urls = {}
    for page_url in brand_urls:
        if uniq_brand_urls.get(page_url):
            print "*** %s already retrievd!!!" % page_url
        else:
            print page_url
            print >> brands_fd, page_url
            uniq_brand_urls[page_url] = page_url[page_url.rfind('/') + 1:]

    brands_fd.close()
    return uniq_brand_urls


if __name__ == '__main__':
    #brand_pages = retrieve_brand_pages_from_4square(BRAND_FILE)
    brand_pages = retrieve_brand_pages_from_about4square(BRAND_FILE)

