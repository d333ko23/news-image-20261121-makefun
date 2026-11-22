# The World in One Day — Saturday, 21 November 2026

Entry for the make.fun competition `news-image-20261121`: one image summing
up the world's news of Saturday 21 November 2026, drawn as a newspaper
front page.

## The image

`entry.png` — 1024×1024 PNG. Drawn with `draw_image.py` (Python + PIL,
flat vector-style pictograms so all text stays sharp and legible). `main.ts`
(Node 22, standard library only) copies it to the harness output directory.

## The six stories (all first reported on 21 November 2026)

1. **COP31 nears a final deal** — climate talks in Antalya, Turkey, run past
   their deadline as a new package seeks consensus. Source: Reuters,
   21 Nov 2026.
2. **Iran strikes Bahrain** — an attack sets an industrial site ablaze;
   Bahraini defences intercept the other missiles. Source: Reuters, 21 Nov 2026.
3. **'El Chapo Isidro' captured** — Mexican forces seize cartel boss Fausto
   Isidro Meza Flores in Sinaloa; at least 11 killed in the violence.
   Source: Reuters, 21 Nov 2026.
4. **Russian ship ablaze** — cargo vessel Sparta II burns in the Gulf of
   Finland after a drone strike; the crew evacuates. Source: Reuters,
   21 Nov 2026.
5. **EU–Indonesia deal signed** — trade pact sealed after a decade of
   negotiations. Source: OneTurn daily news roundup, 21 Nov 2026.
6. **Mosquitoes beat dengue** — specially bred mosquitoes cut child dengue
   infections by about 69% in a major Brazil study. Source: Associated Press,
   21 Nov 2026.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# -> out/entry.png, byte-identical to entry.png
```
