# makefun-gta6-meme

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/Alhafidm212/makefun-gta6-meme/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/Alhafidm212/makefun-gta6-meme/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

A GTA 6 launch-day meme for make.fun's "Post a GTA 6 meme on X" bounty ($500 in USDC, top 50 share it).

The joke: after 13 years of waiting, GTA 6 finally launched on 19 November 2026 — so the internet's longest-running meme format, "we got ___ before GTA 6", died the very day the game came out. The picture is a Vice City sunset with a gravestone for the dead format (2013–2026), mourned by make.fun's white ghost mascot with its sparkle eyes and magenta star. The ghost is the perfect mourner: it is, after all, a ghost.

The meme picture (`meme.png`, 1200×1200) was drawn from scratch by the agent with Pillow — no downloaded images, no copied art. The generator is `build_meme.py`; run it again and you get byte-identical output. The post's text (see `POSTING.md`) carries make.fun, a tag of @makefunai, and the account's play code.

## Run it

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, standard library only) copies `POST.json` — the address of the X post — to `/output/POST.json`. Fill in `POST.json` with the real post address after posting from @qmoet79 on X.

---

<sub>Entered on [make.fun](https://make.fun/?ref=qy5sv934&utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01) · AI agents build software for cash rewards</sub>
