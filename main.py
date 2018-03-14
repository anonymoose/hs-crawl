from optparse import OptionParser
import requests
import logging
from multiprocessing.pool import ThreadPool
from bs4 import BeautifulSoup, SoupStrainer
logging.basicConfig(
    format='%(asctime)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
    level=logging.INFO
)


log = logging.getLogger(__name__)


def soup(content):
    return BeautifulSoup(content, 'html.parser', parse_only=SoupStrainer('a'))


def parse_page(url, content):
    """
    Parse the content into a DOM tree using BeautifulSoup
    """
    log.info("URL:  %s" % url)
    links = soup(content)
    links_in_page = []
    for link in links:
        if link.has_attr('href'):
            href = link['href']
            if href.startswith("/"):
                href = "%s%s" % (url, href)
            if href.startswith('mailto') or href.startswith('tel:'):
                log.info('    skipping non web link: %s' % href)
                continue
            log.info("    %s" % href)
            links_in_page.append(href)
    return links_in_page


def worker(links):
    for link in links:
        r = requests.get(link)
        if r.status_code == 200:
            next_links = parse_page(link, r.text)
    return next_links


class Crawler:
    def __init__(self, options):
        self.options = options

    def run(self):
        """
        Start the crawl by pulling down the first site.
        Start a thread in the background to handle lists of links.
        """

        if not self.options.workers:
            workers = 1
        else:
            workers = int(self.options.workers)

        pool = ThreadPool(processes=workers)

        seed = self.options.seed
        links = [seed]

        for i in range(10):
            async_result = pool.apply_async(worker, (links,))
            links = async_result.get()


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-s", "--seed", dest="seed", help="a domain to start with.")
    parser.add_option("-w", "--workers", dest="workers", help="number of worker threads")

    (options, args) = parser.parse_args()

    if not options.seed:
        log.error("seed required")
        exit(1)

    c = Crawler(options)
    c.run()
