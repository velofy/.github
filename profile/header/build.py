"""Build the animated header for Velofy's GitHub organisation README.

Each section of the header is its own SVG. Inside every SVG is a <foreignObject>
holding plain HTML and CSS, so the layout can use grid, container queries and
CSS animation, and still render through GitHub's image proxy. Every section is
written twice, once per colour scheme, and profile/README.md picks between them
with <picture> and prefers-color-scheme.

The honeycomb is real: one cell per day, lit by the number of commits that day
across the lab's public repositories, read from the GitHub REST API. Run with a
token in GITHUB_TOKEN (the scheduled workflow passes its own):

    GITHUB_TOKEN=$(gh auth token) python3 profile/header/build.py

Only the standard library is used, so the workflow needs no install step.
"""

from __future__ import annotations

import datetime as dt
import html
import json
import math
import os
import pathlib
import re
import urllib.request
from collections import Counter

ORG = "velofy"
# Lab projects that live under the founder's account.
EXTRA_REPOS = ["anishfyi/curl_reap", "anishfyi/trove", "anishfyi/querion"]
OUT = pathlib.Path(__file__).resolve().parent
WEEKS = 53

INTRO = (
    "An applied AI lab in Delhi. We build the tools, frameworks and harnesses "
    "AI agents need to do real work, and publish every one in the open."
)

# Link buttons, in the order they stack down the left of the header.
LINKS = [
    ("site", "velofy.co"),
    ("open-source", "Open source"),
    ("research", "Research"),
    ("bulletin", "Bulletin"),
    ("linkedin", "LinkedIn"),
    ("call", "Book a call"),
]

# Black and white only, per the brand. Levels are one ink at rising opacity.
THEMES = {
    "light": {"ink": "0 0 0", "shine": "rgb(255 255 255 / 0.6)"},
    "dark": {"ink": "255 255 255", "shine": "rgb(0 0 0 / 0.55)"},
}
LEVEL_ALPHA = [0.07, 0.3, 0.52, 0.76, 1.0]

FONT = (
    '-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans",Helvetica,Arial,'
    'sans-serif,"Apple Color Emoji","Segoe UI Emoji"'
)


# ---------------------------------------------------------------- data


def get(url: str) -> tuple[list, str | None]:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise SystemExit("GITHUB_TOKEN is not set")
    request = urllib.request.Request(
        url,
        headers={"Authorization": f"bearer {token}", "Accept": "application/vnd.github+json"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        link = response.headers.get("Link") or ""
        following = re.search(r'<([^>]+)>;\s*rel="next"', link)
        return json.load(response), following.group(1) if following else None


def get_all(url: str) -> list:
    items: list = []
    while url:
        page, url = get(url)
        items += page
    return items


def repositories() -> list[str]:
    repos = get_all(f"https://api.github.com/orgs/{ORG}/repos?type=public&per_page=100")
    names = [r["full_name"] for r in repos if not r["fork"] and not r["archived"]]
    # The .github repository holds this header, so its own refresh commits would
    # count themselves. Leave it out.
    names = [n for n in names if n != f"{ORG}/.github"]
    return sorted(names) + EXTRA_REPOS


def commits_per_day(since: dt.date) -> Counter:
    days: Counter = Counter()
    for repo in repositories():
        url = f"https://api.github.com/repos/{repo}/commits?since={since.isoformat()}T00:00:00Z&per_page=100"
        for commit in get_all(url):
            author = commit.get("author") or {}
            if author.get("type") == "Bot":
                continue
            days[dt.date.fromisoformat(commit["commit"]["author"]["date"][:10])] += 1
    return days


def levels(days: Counter) -> dict[dt.date, int]:
    """Quartiles of the active days, the way GitHub shades its own graph."""
    counts = sorted(days.values())
    if not counts:
        return {}
    cut = [counts[min(len(counts) - 1, math.floor(len(counts) * q))] for q in (0.25, 0.5, 0.75)]
    return {day: 1 + sum(n > c for c in cut) for day, n in days.items()}


# ---------------------------------------------------------------- brand


def brand(name: str) -> tuple[str, str]:
    """Inner markup and viewBox of a brand SVG, recoloured to currentColor."""
    source = (OUT / "brand" / name).read_text()
    view_box = re.search(r'viewBox="([^"]+)"', source).group(1)
    inner = re.search(r"<svg[^>]*>(.*)</svg>", source, re.S).group(1)
    return inner.replace("#fff", "currentColor"), view_box


def lockup() -> str:
    mark, mark_box = brand("velofy-mark.svg")
    word, word_box = brand("velofy-wordmark.svg")
    return (
        f'<svg class="mark" viewBox="{mark_box}" xmlns="http://www.w3.org/2000/svg">{mark}</svg>'
        f'<svg class="word" viewBox="{word_box}" xmlns="http://www.w3.org/2000/svg">{word}</svg>'
    )


# ---------------------------------------------------------------- svg


BASE_CSS = """
:root {
  --default-delay: 0.6s;
  --default-duration: 1.4s;
  --default-stagger: 0.1s;
  --menu-delay: calc(var(--default-delay) + var(--default-stagger) * 0);
  --links-delay: calc(var(--default-delay) + var(--default-stagger) * 1);
  --count-delay: calc(var(--default-delay) + var(--default-stagger) * 5);
  --place-delay: calc(var(--default-delay) + var(--default-stagger) * 6);
  --copy-delay: calc(var(--default-delay) + var(--default-stagger) * 7);
  --hive-delay: calc(var(--default-delay) + var(--default-stagger) * 12);
}
*, *::before, *::after { box-sizing: border-box; }
p { margin: 0; }
.grid { display: grid; grid-template-columns: repeat(6, 1fr); }
.wrapper {
  contain: strict;
  block-size: calc(var(--size-height) * 1px);
  container-type: inline-size;
  position: relative;
  overflow: clip;
  font-family: FONT;
  color: rgb(var(--ink));
}
.label { font-size: 14px; font-weight: 600; }
.link { font-size: 14px; display: flex; gap: 4px; }
.fade-in {
  animation: fade-in var(--duration, var(--default-duration)) var(--ease, ease-out)
    var(--delay, var(--default-delay)) both;
}
@keyframes fade-in { from { opacity: 0; } to { opacity: 1; } }
.shine {
  background-color: rgb(var(--ink));
  background-image: linear-gradient(-75deg, transparent 0%, var(--color-shine) 15%, transparent 25%);
  background-size: 200%;
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: shine 14s infinite;
}
@keyframes shine { 0% { background-position: 200%; } 10%, 100% { background-position: 0%; } }
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation: none !important; }
}
""".replace("FONT", FONT)


def theme_css(theme: str) -> str:
    t = THEMES[theme]
    alphas = "".join(f"--a{i}: {a}; " for i, a in enumerate(LEVEL_ALPHA))
    return f":root {{ --ink: {t['ink']}; --color-shine: {t['shine']}; {alphas}}}"


def svg(theme: str, width: str, height: int, css: str, body: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" fill="none" width="{width}" height="{height}">'
        '<foreignObject width="100%" height="100%">'
        '<div xmlns="http://www.w3.org/1999/xhtml">'
        f"<style>{theme_css(theme)}{BASE_CSS}{css}</style>{body}"
        "</div></foreignObject></svg>\n"
    )


def top(theme: str, total: int) -> str:
    css = """
:root { --size-height: 20; }
.wrapper { align-items: center; }
.menu { --delay: var(--menu-delay); grid-area: 1 / 1 / span 1 / span 3; display: flex; align-items: center; gap: 7px; }
.mark { block-size: 18px; inline-size: 18px; }
.word { block-size: 11px; inline-size: 96px; }
.count { --delay: var(--count-delay); grid-area: 1 / 4 / span 1 / span 2; display: none; }
.place { --delay: var(--place-delay); grid-area: 1 / 4 / span 1 / span 3; text-align: right; }
@container (width > 550px) {
  .count { display: block; grid-area: 1 / 3 / span 1 / span 2; }
  .place { grid-area: 1 / 5 / span 1 / span 2; }
}
@container (width > 700px) {
  .count { grid-area: 1 / 4 / span 1 / span 2; }
  .place { grid-area: 1 / 6 / span 1 / span 1; }
}
"""
    body = (
        '<div class="wrapper grid label">'
        f'<div class="menu fade-in">{lockup()}</div>'
        f'<div class="count fade-in"><span class="shine">{total:,}</span> commits in the open</div>'
        '<div class="place fade-in">Delhi, India</div>'
        "</div>"
    )
    return svg(theme, "100%", 20, css, body)


def link(theme: str, label: str, index: int) -> str:
    css = f"""
:root {{ --size-height: 18; }}
.wrapper {{ display: flex; align-items: center; }}
.link {{ --delay: calc(var(--links-delay) + var(--default-stagger) * {index}); }}
"""
    body = (
        '<div class="wrapper">'
        f'<div class="link fade-in"><span class="shine">{html.escape(label)}</span><span>↗</span></div>'
        "</div>"
    )
    return svg(theme, "110", 18, css, body)


def letters(text: str) -> str:
    return "".join(
        f'<span class="fade-in" style="--i: {i};">{html.escape(ch)}</span>'
        for i, ch in enumerate(text)
    )


# Pointy-top hexagons, the same cut as the cells in the mark. Columns are weeks,
# rows are weekdays (Sunday on top), and odd rows sit half a step to the right.
HEX_W = 17
HEX_H = HEX_W * 2 / math.sqrt(3)
STEP_X = HEX_W + 3
STEP_Y = HEX_H * 0.75 + 2.5


def main(theme: str, today: dt.date, lit: dict[dt.date, int]) -> str:
    start = today - dt.timedelta(days=(today.isoweekday() % 7) + 7 * (WEEKS - 1))
    first = min(lit) if lit else today
    cells, order = [], 0
    for offset in range((today - start).days + 1):
        day = start + dt.timedelta(days=offset)
        column, row = divmod(offset, 7)
        x = column * STEP_X + (row % 2) * STEP_X / 2
        y = row * STEP_Y
        level = lit.get(day, 0)
        style = f"left: {x:.1f}px; top: {y:.1f}px;"
        classes = "hex"
        if day >= first:
            # Days since the lab's first public commit light up in order, so the
            # hive fills from that day to today.
            classes += f" hex--on hex--{level}"
            style += f" --o: {order};"
            order += 1
        if day == today:
            classes += " hex--today"
        cells.append(f'<div class="{classes}" style="{style}"></div>')
    hive_w = (WEEKS - 1) * STEP_X + STEP_X / 2 + HEX_W
    hive_h = 6 * STEP_Y + HEX_H
    first_x = ((first - start).days // 7) * STEP_X
    span = max(order, 1)
    css = f"""
:root {{ --size-height: 290; }}
.wrapper {{ align-items: end; grid-template-rows: 1fr auto; row-gap: 22px; }}
.intro {{ grid-area: 1 / 1 / span 1 / span 6; font-size: 18px; font-weight: 300; line-height: 1.35; }}
.intro span {{ --duration: 980ms; --delay: calc(var(--copy-delay) + var(--i) * 10ms); }}
@container (width > 550px) {{ .intro {{ grid-area: 1 / 3 / span 1 / span 4; font-size: 22px; }} }}
@container (width > 700px) {{ .intro {{ grid-area: 1 / 4 / span 1 / span 3; }} }}
.graph {{
  grid-area: 2 / 1 / span 1 / span 6;
  --delay: var(--hive-delay);
  position: relative;
  block-size: {hive_h + 26:.0f}px;
  -webkit-mask-image: linear-gradient(to right, transparent, #000 22%);
  mask-image: linear-gradient(to right, transparent, #000 22%);
}}
.hive {{ position: absolute; right: 0; top: 0; inline-size: {hive_w:.0f}px; block-size: {hive_h:.0f}px; }}
.hex {{
  position: absolute;
  inline-size: {HEX_W}px;
  block-size: {HEX_H:.2f}px;
  clip-path: polygon(50% 0, 100% 25%, 100% 75%, 50% 100%, 0 75%, 0 25%);
  background: rgb(var(--ink) / var(--a0));
}}
.hex--on {{ animation: fill 0.9s ease-out calc(var(--hive-delay) + 0.6s + var(--o) * {3.2 / span:.4f}s) both; }}
.hex--1 {{ --to: var(--a1); background: rgb(var(--ink) / var(--a1)); }}
.hex--2 {{ --to: var(--a2); background: rgb(var(--ink) / var(--a2)); }}
.hex--3 {{ --to: var(--a3); background: rgb(var(--ink) / var(--a3)); }}
.hex--4 {{ --to: var(--a4); background: rgb(var(--ink) / var(--a4)); }}
.hex--0 {{ --to: var(--a0); background: rgb(var(--ink) / var(--a0)); }}
@keyframes fill {{
  from {{ background: rgb(var(--ink) / var(--a0)); }}
  40% {{ background: rgb(var(--ink) / 1); }}
  to {{ background: rgb(var(--ink) / var(--to)); }}
}}
.hex--today {{ animation: fill 0.9s ease-out calc(var(--hive-delay) + 4s) both, pulse 2.8s ease-in-out calc(var(--hive-delay) + 5s) infinite; }}
@keyframes pulse {{ 50% {{ background: rgb(var(--ink) / 0.25); }} }}
.marks {{ position: absolute; right: 0; bottom: 0; inline-size: {hive_w:.0f}px; block-size: 18px; }}
.marks span {{ position: absolute; bottom: 0; font-size: 12px; font-weight: 600; white-space: nowrap; }}
.since {{ left: {first_x:.0f}px; }}
.now {{ right: 0; }}
@container (max-width: 550px) {{
  .since {{ display: none; }}
  .graph {{
    -webkit-mask-image: linear-gradient(to right, transparent, #000 10%);
    mask-image: linear-gradient(to right, transparent, #000 10%);
  }}
}}
"""
    body = (
        '<main class="wrapper grid">'
        f'<article class="intro"><p>{letters(INTRO)}</p></article>'
        '<article class="graph fade-in">'
        f'<div class="hive">{"".join(cells)}</div>'
        '<div class="marks">'
        f'<span class="since">First public commit, {first.strftime("%b %-d, %Y")}</span>'
        f'<span class="now">{today.strftime("%b %-d, %Y")}</span>'
        "</div></article></main>"
    )
    return svg(theme, "100%", 290, css, body)


def build(today: dt.date | None = None) -> None:
    today = today or dt.datetime.now(dt.timezone.utc).date()
    days = commits_per_day(today - dt.timedelta(days=7 * WEEKS + 7))
    lit = levels(days)
    total = sum(days.values())
    for theme in THEMES:
        (OUT / f"top-{theme}.svg").write_text(top(theme, total))
        for index, (slug, label) in enumerate(LINKS):
            (OUT / f"link-{slug}-{theme}.svg").write_text(link(theme, label, index))
        (OUT / f"main-{theme}.svg").write_text(main(theme, today, lit))
    print(f"{total} commits on {len(days)} days, written to {OUT}")


if __name__ == "__main__":
    build()
