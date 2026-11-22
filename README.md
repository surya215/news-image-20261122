# The World in One Day — Sunday 22 November 2026

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/surya215/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/surya215/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

A broadsheet front page that sums up the world's news of **Sunday, 22 November 2026** in a single image: a masthead naming the day, one big lead story with a schematic map of the Gulf, six story panels across regions and beats, and an "In Brief" strip.

## The stories in the image

- **Lead — The Gulf: Iran strikes U.S.-linked sites in Bahrain.** Missiles and drones hit targets overnight into Sunday. Iran's Revolutionary Guard says it destroyed two U.S. Patriot radars; Bahrain says an industrial facility was hit and caught fire, its defences intercepted other attacks, and no injuries were reported. U.S. officials say almost all incoming fire was intercepted. Claims from each side are attributed, not stated as settled fact.
- **Climate — COP31 talks deadlocked (Antalya, Turkey).** Negotiators run past their deadline with no deal: the draft drops all mention of fossil fuels and the $120bn adaptation-finance figure, and a final plenary is pushed into Sunday.
- **Israel — Eisenkot tapped to form government.** President Herzog asks former army chief Gadi Eisenkot to try to build the next government, bypassing sitting prime minister Benjamin Netanyahu.
- **Gaza — Four nations urge open aid access.** Australia, Canada, Italy and the UK jointly call on Israel to let aid reach flooded Gaza without restriction.
- **Disaster — Peru counts the cost of Friday's quake.** One dead, 16 hurt and 152 homes uninhabitable, officials say in updated tolls reported on Sunday.
- **Europe — Fourth weekend of cost-of-living protests in France.** A fourth straight weekend of nationwide demonstrations over rising living costs.
- **Sport — Alcaraz v Zverev for the ATP Finals title.** Carlos Alcaraz fights back past Ben Shelton to set up a decider against world No. 1 Alexander Zverev; France also reach the Nations Championship final.
- **In Brief:** a magnitude 4.1 quake in Myanmar; Norway's top court rules climate-disputed oil licences invalid; voting opens for Hong Kong's Election Committee; Al-Shabaab claims hundreds dead in an ambush on Somali troops; Ghana unveils new "Heritage Series" banknotes; the Ebola death toll in DR Congo passes 5,300, officials say.

Every story happened, or was first reported, on Sunday 22 November 2026. Sources are listed in [NEWS.md](NEWS.md).

## How to run

Render the image (Python 3 + Pillow, deterministic — no randomness, clock or network):

```sh
python3 draw.py
```

Copy it to the output directory (Node 22, standard library only):

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`draw.py` draws `entry.png` (1024×1024, RGB, under 1 MiB) from scratch; `main.ts` copies that file to `$MAKEFUN_OUTPUT_DIR/entry.png` (or `/output/entry.png`).

<sub>Entered on [make.fun](https://make.fun/?ref=vfpg0cj5&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
