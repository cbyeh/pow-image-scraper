# Quick script to scrape masked images from picturesofwalls.com without regular expressions
# Dependencies: `pip install beautifulsoup4` `pip install requests`
# Author: cbyeh
# License: MIT
import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
# For src images in id main-img text that contain invalids like ' ' and (1)
from urllib.parse import quote
# Multithreading for faster downloads
import threading

base = 'http://picturesofwalls.com/'
# As images are associated with a page and each image has a unique id
# we can set album to 0 and still load all images
extension = 'gallery.asp?album=0&id={0}'


# Check whether url can load
def _is_valid(url):
    request = requests.head(url)
    return request.status_code == requests.codes.ok


# Download with filename as id.{original filename}
def _download(url, index):
    print('Downloading from id: ' + str(index) + ' at: ' + img_url)
    urlretrieve(img_url, 'out/' + str(index) + '.' + img_extension[19:])


# Create thread for async downloads
def _create_download_thread(url, index):
    download_thread = threading.Thread(
        target=_download, args=(url, index))
    download_thread.start()


# Add all images to Queue. As of June 2020, images before 142 are deprecated and latest is 16791
for i in range(142, 16792):
    url = base + extension.format(i)
    # Find image with id "main-image". We are only interested in the main photo in the Database
    response = requests.get(url)
    if _is_valid(url) and response.ok:
        soup = BeautifulSoup(response.content, 'html.parser')
        img_extension = quote(soup.find(id='main-image')['src'])
        img_url = base + img_extension  # url of image
        # Write file
        if _is_valid(img_url):
            _create_download_thread(img_url, i)
