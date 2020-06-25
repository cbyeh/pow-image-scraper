# Quick script to scrape masked images from picturesofwalls.com without regular expressions
# Dependencies: `pip install beautifulsoup4` `pip install requests`
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.request import urlretrieve

base = 'http://picturesofwalls.com/'
# As images are associated with a page and each image has a unique id
# we can set album to 0 and still load all images
extension = 'gallery.asp?album=0&id={0}'


# Check whether url can load
def _is_valid(url):
    parse = urlparse(url)
    return bool(parse.netloc) and bool(parse.scheme)


# As of June 2020, images before 142 are deprecated and latest is 16791
for i in range(278, 16792):
    url = base + extension.format(i)
    # Find image with id "main-image". We are only interested in the main photo in the Database
    response = requests.get(url)
    if _is_valid(url) and response.ok:
        soup = BeautifulSoup(response.content, 'html.parser')
        img_extension = soup.find(id='main-image')['src']
        img_url = base + img_extension  # Url of image
        # Write file
        if _is_valid(img_url) and (img_extension.endswith('.jpg') or img_extension.endswith('.jpeg') or img_extension.endswith('.png')):
            print('Downloading from id: ' + str(i) + ' at: ' + img_url)
            # Download with filename as id.{original filename}
            urlretrieve(img_url, 'out/' + str(i) + '.' + img_extension[19:])
