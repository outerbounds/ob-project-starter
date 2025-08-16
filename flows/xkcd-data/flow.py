import re
from xml.etree import ElementTree

from metaflow import (
    card,
    FlowSpec,
    step,
    current,
    project,
    Flow,
    retry,
    schedule,
    Parameter,
)
from metaflow.cards import Markdown as MD, Image
from obproject import ProjectFlow

import requests

XKCD_RSS = "https://xkcd.com/rss.xml"


def fetch_latest():
    resp = requests.get(XKCD_RSS)
    resp.raise_for_status()
    root = ElementTree.fromstring(resp.text)
    latest_item = root.find("./channel/item")
    latest_id = latest_item.findtext("link")
    description_html = latest_item.findtext("description")
    img_url = re.search(r'src="([^"]+)"', description_html).group(1)
    print(f"Latest XKCD {latest_id} - image at {img_url}")
    return latest_id, img_url


def get_img(url):
    return requests.get(url).content


class SkipTrigger(Exception):
    pass


@schedule(daily=True)
class XKCDData(ProjectFlow):

    reset_existing = Parameter("reset-existing", default="no")

    @card(type="blank")
    @step
    def start(self):
        try:
            existing = Flow("XKCDData").latest_successful_run.data.latest_id
        except:
            print("No existing photos found - starting from scratch")
            existing = None
        if self.reset_existing != "no":
            print("Forgetting existing data")
            existing = None
        self.latest_id, self.img_url = fetch_latest()
        if self.latest_id == existing:
            print("No new XKCD available")
            raise SkipTrigger(
                "Not an error - failing this run on purpose "
                "to avoid triggering flows downstream"
            )
        else:
            current.card.append(MD(f"New XKCD at {self.latest_id}"))
            current.card.append(Image(get_img(self.img_url)))
            self.prj.register_data("xkcd", "img_url")
            print("New asset instance registered")
        self.next(self.end)

    @step
    def end(self):
        pass


if __name__ == "__main__":
    XKCDData()
