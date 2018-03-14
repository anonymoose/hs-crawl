from optparse import OptionParser
import requests
import logging
logging.basicConfig(
    format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
    level=logging.INFO
)


log = logging.getLogger(__name__)


def run(options):
    seed = options.seed

    r = requests.get(seed)
    if r.status_code == 200:
        print("ok")



if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-s", "--seed", dest="seed", help="a domain to start with.")

    (options, args) = parser.parse_args()

    if not options.seed:
        log.error("seed required")
        exit(1)

    run(options)
