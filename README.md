# news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/sholaah/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/sholaah/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

A program that renders Sunday 22 November 2026's world news as one Economist-style cover image: a cream page, a red "THE WORLD TODAY" masthead, the date as a huge title, and a drawn night scene over the Strait of Hormuz for the lead story — Iran's strikes on a U.S. base in Kuwait and Bahrain — with three secondary stories (Russian missiles landing in Poland, the 6.9 Peru quake, Eisenkot tapped to form Israel's government) and a ticker of the rest of the day. The image is pre-rendered with Pillow by build_image.py and copied to the output directory by main.py, so the entrypoint is deterministic and needs no network.

## Run it

```sh
python3 build_image.py && MAKEFUN_OUTPUT_DIR=./output python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=s0dzaxys&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
