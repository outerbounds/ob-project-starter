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
from xkcd_utils import fetch_latest, get_img


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
