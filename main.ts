// The World in One Day — Sunday 22 November 2026 (Team B entry).
//
// Node 22, standard library only. The image is entry.png beside this file;
// the program copies it to the output directory so the grader sees exactly
// the bytes this repository ships.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const source = new URL('./entry.png', import.meta.url);
copyFileSync(source, join(outDir, 'entry.png'));
