from metaflow import (
    card,
    FlowSpec,
    step,
    current,
    resources,
    pypi,
    Parameter,
    trigger_on_finish,
    profile,
    Flow,
)
from metaflow.cards import Markdown as MD, Image
from obproject import ProjectFlow, project_trigger, highlight
from xkcd_utils import get_img

MODEL = "HuggingFaceTB/SmolVLM-Instruct"
PROMPT = "Explain what is funny about this XKCD comic strip?"


def prompt(img_url):
    """
    This prompting example is from
    https://huggingface.co/HuggingFaceTB/SmolVLM-Instruct
    """

    import torch
    from transformers import AutoProcessor, AutoModelForVision2Seq
    from transformers.image_utils import load_image

    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

    image1 = load_image(img_url)

    with profile(f"Loading model"):
        processor = AutoProcessor.from_pretrained(MODEL)
        model = AutoModelForVision2Seq.from_pretrained(
            MODEL,
            torch_dtype=torch.bfloat16,
            _attn_implementation="flash_attention_2" if DEVICE == "cuda" else "eager",
        ).to(DEVICE)

    # Create input messages
    messages = [
        {
            "role": "user",
            "content": [{"type": "image"}, {"type": "text", "text": PROMPT}],
        },
    ]

    # Prepare inputs
    prompt = processor.apply_chat_template(messages, add_generation_prompt=True)
    inputs = processor(text=prompt, images=[image1], return_tensors="pt")
    inputs = inputs.to(DEVICE)

    # Generate outputs
    with profile("Prompting"):
        generated_ids = model.generate(**inputs, max_new_tokens=500)
        generated_texts = processor.batch_decode(
            generated_ids,
            skip_special_tokens=True,
        )

    return generated_texts[0]


@project_trigger(event="explain")
class XKCDExplainer(ProjectFlow):

    xkcd_url = Parameter("xkcd_url", help="Image url of an XKCD comic")

    @card(type="blank")
    @step
    def start(self):
        if self.xkcd_url and self.xkcd_url != "null":
            self.img_url = self.xkcd_url
            print(f"Using an image passed in as a parameter, {self.img_url}")
        else:
            self.img_url = self.prj.get_data("xkcd")
            print(f"Using an image from the latest data asset, {self.img_url}")

        print(self.prj.asset.consume_model_asset("explainer-vlm"))
        self.next(self.prompt_vlm)

    # ⬇️ add gpu=1 to @resources if you have GPU compute pools configured
    @resources(cpu=4, memory=16000)
    @card(type="blank", id="model", refresh_interval=2)
    @pypi(
        python="3.11.11",
        packages={"transformers": "4.55.2", "torch": "2.8.0", "pillow": "11.3.0"},
    )
    @highlight
    @step
    def prompt_vlm(self):
        msg = f"Starting model `{MODEL}`.. This may take 3-5 minutes! ⌛"
        title = MD(f"## {msg}")
        current.card["model"].append(title)
        current.card["model"].refresh()

        print(msg)
        explanation = prompt(self.img_url)
        print(explanation)
        print("🔍 See a card attached for the explanation in context")

        img = get_img(self.img_url)
        self.highlight.title = "Click to see an explanation of the comic"
        self.highlight.add_line(f"The latest XKCD comic")
        self.highlight.set_image(img)

        title.update("### ✅ Prompting done!")
        current.card["model"].append(
            MD(f"## 🤖 `{MODEL}`'s interpretation of the comic")
        )
        current.card["model"].append(Image(img))
        current.card["model"].append(MD(explanation))

        self.next(self.end)

    @step
    def end(self):
        pass


if __name__ == "__main__":
    XKCDExplainer()
