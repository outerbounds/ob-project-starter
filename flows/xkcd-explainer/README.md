
Explain the latest XKCD comic using a locally loaded visual language model, tracked as
[an `explainer-vlm` model asset](models).

**Note** by default, this flow runs on a small CPU instance, so it can take 3-5 minutes
to provide one explanation 🦥. You can get results much faster by using GPU instances (even
small ones).

Simply add a GPU compute pool and upgrade `@resources` in the flow code to have at least
`@resources(gpu=1)`.


