from metaflow import FlowSpec, Parameter, current, step
from obproject import ProjectFlow

from highlight_card import highlight


class HighlightTester(ProjectFlow):
    style = Parameter(
        "style",
        default="animals",
        help="Choose a highlight style: animals, nyan, image, small_square, tall_image, wide_image, revenue, busy",
    )

    @highlight
    @step
    def start(self):
        getattr(self, self.style)()
        self.next(self.end)

    def nyan(self):
        import requests

        resp = requests.get(
            "https://www.icegif.com/wp-content/uploads/2024/08/nyan-cat-icegif-1.gif"
        )
        self.highlight.title = "nyan cat ftw! 🌈"
        self.highlight.set_image(resp.content)

    def image(self):
        import requests

        resp = requests.get("https://picsum.photos/400/200")
        self.highlight.title = "image"
        self.highlight.add_line("Here's a photo")
        self.highlight.set_image(resp.content)

    def small_square(self):
        import requests

        resp = requests.get("https://picsum.photos/100/100")
        self.highlight.title = "image"
        self.highlight.add_line("Here's a small 100x100 image")
        self.highlight.set_image(resp.content)

    def tall_image(self):
        import requests

        resp = requests.get("https://picsum.photos/300/600")
        self.highlight.title = "image"
        self.highlight.add_line("Here's a tall 300x600 image")
        self.highlight.set_image(resp.content)

    def wide_image(self):
        import requests

        resp = requests.get("https://picsum.photos/800/300")
        self.highlight.title = "image"
        self.highlight.add_line("Here's a wide 800x300 image")
        self.highlight.set_image(resp.content)

    def revenue(self):
        self.highlight.title = "Quarterly Revenue"
        self.highlight.add_column(
            big="$123,456,789", small="Revenue over the past three quarters"
        )

    def animals(self):
        self.highlight.title = "Zoo!"
        self.highlight.add_column(big="🦁", small="Roar")
        self.highlight.add_column(big="🦧", small="Grunt")
        self.highlight.add_column(big="🐈", small="Meow")
        self.highlight.add_column(big="🦄", small="ZIRP")

    def busy(self):
        self.highlight.add_label("product_xp")
        self.highlight.add_label("live")
        self.highlight.set_title("A/B Experiment: Blue vs. Green")
        for i, x in enumerate(["Blue variant", "Green variant", "Control"]):
            self.highlight.add_line(x, caption=f"Slot {i}")
        self.highlight.add_column("8%", "click rate")
        self.highlight.add_column("34%", "completion rate")

    @step
    def end(self):
        pass


if __name__ == "__main__":
    HighlightTester()
