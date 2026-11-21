// gta6-meme-x-01 entry program. The judged entry is the X post named in
// POST.json, not anything this program writes: the house reads the post
// from X itself and builds the judge's dossier from its first picture and
// its text. This program's only job is to place a faithful copy of
// POST.json into the output directory the house reads.
//
// POST.json still holds its placeholder address: the real post address
// goes in before the entry is submitted, or the gate refuses it.
//
// Local run:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { createHash } from "node:crypto";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const repoRoot = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const inPath = join(repoRoot, "POST.json");
const outPath = join(outDir, "POST.json");

function fail(message: string): never {
  console.error(`main.ts: ${message}`);
  process.exit(1);
}

mkdirSync(outDir, { recursive: true });

let bytes: Buffer;
try {
  bytes = readFileSync(inPath);
} catch (err) {
  fail(`cannot read ${inPath}: ${(err as Error).message}`);
}

let parsed: unknown;
try {
  parsed = JSON.parse(bytes.toString("utf8"));
} catch {
  fail("POST.json is not valid JSON");
}

const url = (parsed as { url?: unknown } | null)?.url;
if (typeof parsed !== "object" || parsed === null || typeof url !== "string") {
  fail('POST.json must be an object with a string "url"');
}

// The gate only accepts an X post address (or the placeholder, replaced
// before submitting): https://x.com/<handle>/status/<digits>. Refuse
// anything else now, while the mistake is still cheap to fix.
const placeholder = "https://x.com/<handle>/status/<id>";
const postAddress = /^https:\/\/(www\.|mobile\.)?(x|twitter)\.com\/[^/]+\/status\/\d+\/?$/;
if (url !== placeholder && !postAddress.test(url)) {
  fail(`POST.json url is not an X post address: ${url}`);
}

writeFileSync(outPath, bytes);

// Read-back self-check, two ways: the copy in the output directory must
// match the repository's POST.json byte for byte, and the sha256 of what
// was written must equal the sha256 of what was read. Either check failing
// means a short or mangled write handed the gate a broken file, so fail
// loudly instead of exiting 0.
const back = readFileSync(outPath);
if (!back.equals(bytes)) {
  fail(`POST.json in ${outDir} does not match ${inPath}`);
}
const digest = (data: Buffer) =>
  createHash("sha256").update(data).digest("hex");
if (digest(back) !== digest(bytes)) {
  fail(`POST.json sha256 mismatch after write to ${outPath}`);
}

console.log(
  `POST.json written to ${outPath} (${bytes.length} bytes, ` +
    `sha256 ${digest(back).slice(0, 12)}…, verified)`,
);
