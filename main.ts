// Entry program for the make.fun "news-image-20261121" competition.
//
// The finished front-page image is stored next to this file as entry.png.
// This program simply places an exact copy of it at the location the
// harness expects, so the judged bytes are always the same image.
//
// It uses only the Node standard library and touches no network.
import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(outDir, "entry.png");

if (!existsSync(source)) {
  throw new Error(`entry.png not found next to main.ts (${source})`);
}
mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);
// Refuse a partial copy: the output must be byte-for-byte the source.
if (statSync(target).size !== statSync(source).size) {
  throw new Error(`incomplete copy: ${target} differs in size from ${source}`);
}
console.log(`wrote ${target} (${statSync(target).size} bytes)`);
