import re
from xml.etree import ElementTree

import requests

XKCD_RSS = "https://xkcd.com/rss.xml"


def fetch_latest():
    resp = requests.get(XKCD_RSS)
    resp.raise_for_status()
    root = ElementTree.fromstring(resp.text)
    latest_item = root.find("./channel/item")
    latest_id = latest_item.findtext("link").split('/')[-2]
    description_html = latest_item.findtext("description")
    img_url = re.search(r'src="([^"]+)"', description_html).group(1)
    return latest_id, img_url


def get_img(url):
    return requests.get(url).content
