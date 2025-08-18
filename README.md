
# Outerbounds Project Starter Template 👋🌱

Use this repository as a starting point and inspiration for your own projects. Here's a high-level overview of the components included:

<img width="70%" src="https://raw.githubusercontent.com/outerbounds/ob-project-starter/539a40eaad2e275fef627f91d939a92c09740fdc/docs/XKCD%20diagram.png">

The project consists of two flows

  1. `XKCDData` - polls [xkcd.com](https://xkcd.com) periodically to fetch the latest comic,
     tracked as [**a data asset**, `xkcd`](data).

  2. `XKCDExplainer` - triggered by either `XKCDData` or the `XKCDViewer` app via an event.
     It uses a local visual language model, tracked as [**a model asset**, `explainer-vlm`](model),
     to explain a comic.

In addition to the flows, the project includes [an interactive (Steamlit) dashboard](deployments)

  - `XKCDViewer` which you can use to browse past comics and choose to trigger an explanation for one.

[Check out the code](https://github.com/outerbounds/ob-project-starter),
open a new branch, alter any parts of the system, push a pull request, and see what happens!
All changes take effect only in your personal branch, so you can experiment safely ⚗️

#### ➡️ For comprehensive documentation, see [the project section in the Outerbounds docs](https://docs.outerbounds.com)

