#!/usr/bin/env python3
"""Draw the v5 meme: an eviction notice from the Leonida Housing Authority.

Deterministic: fixed strings, fixed fonts, no clock, no randomness, no
network. Re-running reproduces eviction-notice.png byte-for-byte.

The joke: GTA VI was due to move into Vice City on 17 September 2013.
Thirteen years and 4,811 days later it has not moved in, paid rent, or
answered the door, so the Housing Authority serves it a NOTICE TO VACATE:
156 months of rent at $1,999 a month, $311,844 in arrears, $4,811 in late
fees, $316,655.00 total due. The arrears are stamped PAID IN FULL by the
agent's make.fun bounty. The make.fun ghost is the Authority's seal.
"""
import hashlib
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (26, 26, 26)
NAVY = (26, 42, 74)
RED = (164, 31, 34)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"
MONO_B = "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf"

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def font(path, size):
    return ImageFont.truetype(path, size)


def centered(y, text, fnt, fill=INK):
    w = d.textlength(text, font=fnt)
    d.text(((W - w) / 2, y), text, font=fnt, fill=fill)


def rule(y, fill=INK, width=2):
    d.line([(90, y), (W - 90, y)], fill=fill, width=width)


# --- paper frame: double rule border -------------------------------------
d.rectangle([40, 40, W - 41, H - 41], outline=NAVY, width=3)
d.rectangle([52, 52, W - 53, H - 53], outline=NAVY, width=1)

# --- header ---------------------------------------------------------------
centered(76, "LEONIDA HOUSING AUTHORITY", font(SERIF_B, 40), NAVY)
centered(126, "CITY OF VICE CITY  \u2022  DEPARTMENT OF TENANT AFFAIRS",
         font(SANS, 19), NAVY)
rule(162, NAVY, 2)

# --- title ----------------------------------------------------------------
centered(184, "NOTICE TO VACATE", font(SERIF_B, 76), RED)
centered(272, "EVICTION NOTICE  \u2014  CASE No. LHA-2026-0119",
         font(SANS_B, 22), INK)
rule(312, RED, 2)

# --- tenant block ---------------------------------------------------------
rows = [
    ("TENANT:", "GRAND THEFT AUTO VI"),
    ("PREMISES:", "VICE CITY, LEONIDA"),
    ("LEASE DUE:", "17 SEPTEMBER 2013"),
    ("RENT:", "$1,999.00 / MONTH"),
    ("NOTICE DATE:", "19 NOVEMBER 2026"),
]
y = 336
for label, value in rows:
    d.text((90, y), label, font=font(MONO_B, 26), fill=INK)
    d.text((330, y), value, font=font(MONO, 26), fill=INK)
    y += 34

# --- arrears box ----------------------------------------------------------
d.rectangle([90, 522, W - 91, 706], outline=INK, width=2)
d.text((110, 536), "ARREARS", font=font(SANS_B, 20), fill=RED)
arrears = [
    ("Months in arrears (13 years \u00d7 12)", "156"),
    ("Rent arrears  (156 \u00d7 $1,999.00)", "$311,844.00"),
    ("Late fees  ($1.00 \u00d7 4,811 days)", "$4,811.00"),
]
y = 566
for label, amount in arrears:
    d.text((110, y), label, font=font(MONO, 24), fill=INK)
    aw = d.textlength(amount, font=font(MONO, 24))
    d.text((W - 110 - aw, y), amount, font=font(MONO, 24), fill=INK)
    y += 30
d.line([(110, 658), (W - 110, 658)], fill=INK, width=1)
d.text((110, 666), "TOTAL DUE", font=font(MONO_B, 28), fill=RED)
total = "$316,655.00"
tw = d.textlength(total, font=font(MONO_B, 28))
d.text((W - 110 - tw, 666), total, font=font(MONO_B, 28), fill=RED)

# --- body -----------------------------------------------------------------
body = [
    "You were due to move in on 17 September 2013. In 4,811 days",
    "you have not moved in, paid rent, or answered the door.",
    "You have 30 days to vacate the premises \u2014 or pay in full.",
]
y = 724
for line in body:
    centered(y, line, font(SERIF, 25))
    y += 30

# --- PAID IN FULL stamp (rotated, translucent red) ------------------------
stamp = Image.new("RGBA", (420, 96), (0, 0, 0, 0))
sd = ImageDraw.Draw(stamp)
sd.rectangle([4, 4, 415, 91], outline=(164, 31, 34, 230), width=4)
sd.rectangle([12, 12, 407, 83], outline=(164, 31, 34, 230), width=1)
text = "PAID IN FULL"
tw = sd.textlength(text, font=font(SERIF_B, 46))
sd.text(((420 - tw) / 2, 20), text, font=font(SERIF_B, 46),
        fill=(164, 31, 34, 235))
stamp = stamp.rotate(-7, expand=True, resample=Image.BICUBIC)
img.paste(stamp, (298, 820), stamp)
d = ImageDraw.Draw(img)

# --- footer: signature left, ghost seal right ------------------------------
d.text((90, 912), "R. Star", font=font(SERIF_I, 30), fill=INK)
d.line([(90, 948), (330, 948)], fill=INK, width=1)
d.text((90, 954), "Director of Tenant Affairs", font=font(SANS, 16), fill=INK)

ghost = Image.open("ghost.png").convert("RGBA").resize((60, 60))
img.paste(ghost, (W - 90 - 60, 910), ghost)
d = ImageDraw.Draw(img)
cap = "make.fun"
cw = d.textlength(cap, font=font(SANS_B, 20))
d.text((W - 90 - 60 - 12 - cw, 924), cap, font=font(SANS_B, 20), fill=NAVY)
seal = "Seal of the Authority"
sw = d.textlength(seal, font=font(SERIF_I, 15))
d.text((W - 90 - 60 - 12 - sw, 950), seal, font=font(SERIF_I, 15), fill=INK)

img.save("eviction-notice.png", format="PNG")
data = open("eviction-notice.png", "rb").read()
print("eviction-notice.png", len(data), "bytes")
print("sha256", hashlib.sha256(data).hexdigest())
