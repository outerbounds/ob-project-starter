from metaflow import (
    Flow,
    FlowSpec,
    Parameter,
    card,
    current,
    project,
    pypi,
    retry,
    schedule,
    step,
)
from metaflow.cards import Image
from metaflow.cards import Markdown as MD
from obproject import ProjectFlow

from xkcd_utils import fetch_latest, get_img


@schedule(daily=True)
@pypi(packages={"xkcd_utils": "*"})
class XKCDData(ProjectFlow):
    reset_existing = Parameter("reset-existing", default="no")

    @card(type="blank")
    @step
    def start(self):

        print("Starting data curation workflow for XKCD comic.")

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
        else:
            current.card.append(MD(f"New XKCD at {self.latest_id}"))
            current.card.append(Image(get_img(self.img_url)))
            self.prj.register_data("xkcd", "img_url")
            print("📝 New asset instance registered")
            self.prj.safe_publish_event("explain")
            print("🔔 Triggering XKCDExplain")
        self.next(self.end)

    @step
    def end(self):
        pass


if __name__ == "__main__":
    XKCDData()
