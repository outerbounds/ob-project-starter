from metaflow import FlowSpec, anaconda, secrets, step


class TestHuggingFacePrivate(FlowSpec):
    @secrets(sources=["outerbounds.anaconda-se-gtm01-read-only"])
    @anaconda(packages={"huggingface_hub": "1.33.0"})
    # @pypi(packages={"huggingface-hub": "0.26.2"})
    @step
    def start(self):
        import os

        from huggingface_hub import whoami

        hf_token = os.getenv("HF_TOKEN")
        try:
            user_info = whoami(hf_token)
            self.username = user_info["name"]
        except Exception as e:
            raise RuntimeError("Failed to authenticate.") from e

        print(f"Successfully authenticated as {self.username}.")
        print(hf_token)
        self.next(self.end)

    @step
    def end(self):
        pass


if __name__ == "__main__":
    TestHuggingFacePrivate()
