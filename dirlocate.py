import sys
import requests
from tqdm import tqdm
# Debugger
from icecream import ic


def url_validation(url):
    accepted = [200, 301, 302, 404]

    if not url.startswith('http'):
        return False

    if not '://' in url:
        return False

    if not '.' in url.split('/')[2]:
        return False

    if not url.endswith('/'):
        url = url + '/'
        return url

    r = requests.get(url)
    if r.status_code in accepted:
        return url
    else:
        return False


# TODO add recursive directory search
if __name__ == '__main__':

    # Validation
    if len(sys.argv) != 2:
        print("Expected usage is dirlocate.py URL")
        exit(1)
    URL = sys.argv[1]

    # Verify URL
    verified = url_validation(URL)
    if not verified:
        print("Invalid URL")
        exit(1)

    # Load dictionary
    with open('dirsearch.txt') as f:
        dico = f.read().splitlines()

    # combine elements
    for directory in tqdm(dico):
        uri = verified + directory
        r = requests.get(uri)

        # in case it works
        # 2XX
        if r.status_code < 300:
            tqdm.write(f"Found : ({r.status_code}) {uri}")

        # in case of redirect
        # 3XX
        elif r.status_code < 400:
            tqdm.write(f"Redicrect ({r.status_code}) : {uri} ==> {r.url}")

        # errors
        # 4XX-5XX
        else:
            continue