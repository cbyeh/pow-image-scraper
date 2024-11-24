import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import quote
import threading
import time
from random import uniform

base = 'http://picturesofwalls.com/'
extension = 'gallery.asp?album=0&id={0}'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Referer': 'http://picturesofwalls.com/'
}
thread_semaphore = threading.Semaphore(10)

# Create output folder
if not os.path.exists('pow'):
    os.makedirs('pow')

session = requests.Session()
session.headers.update(HEADERS)

# Fetch cookies by visiting the base page
session.get(base, headers=HEADERS)

def _is_valid(url):
    try:
        request = session.head(url)
        return request.status_code == requests.codes.ok
    except requests.RequestException as e:
        print(f"Error checking URL {url}: {e}")
        return False

def _download(url, index):
    try:
        print(f'Downloading from id: {index} at: {url}')
        response = session.get(url, stream=True)
        if response.status_code == 200:
            with open(f'pow/{index}.jpg', 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"Successfully downloaded {url}")
        else:
            print(f"Failed to download {url}: HTTP {response.status_code}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

def _create_download_thread(url, index):
    def download_wrapper():
        with thread_semaphore:
            _download(url, index)
    download_thread = threading.Thread(target=download_wrapper)
    download_thread.start()

for i in range(142, 16848):
    url = base + extension.format(i)
    try:
        response = session.get(url)
        if _is_valid(url) and response.ok:
            soup = BeautifulSoup(response.content, 'html.parser')
            img_tag = soup.find(id='main-image')
            if img_tag and 'src' in img_tag.attrs:
                img_extension = quote(img_tag['src'])
                img_url = base + img_extension
                if _is_valid(img_url):
                    _create_download_thread(img_url, i)
        time.sleep(uniform(1, 3))  # Random delay
    except Exception as e:
        print(f"Error processing page {i}: {e}")
