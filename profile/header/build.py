"""Build the header for Velofy's GitHub organisation README.

The header is a set of SVG files. Each one holds a <foreignObject> with plain
HTML and CSS, so the layout can use grid, container queries and CSS animation
and still render through GitHub's image proxy. Every file is written twice,
once per colour scheme, and profile/README.md picks between them with <picture>
and prefers-color-scheme.

    main-{theme}.svg         the panel: lockup, intro and the commit grid
    link-{slug}-{theme}.svg  one text link each, in a row under the panel

The colours, type and shapes follow the Foundry system on velofy.co: a black
panel (warm paper in light mode), cream ink, one gold accent, Switzer for text
and Fragment Mono for small labels. An image cannot load anything from outside
itself, so both fonts are embedded as base64 data URIs.

The commit grid is real: one rounded square per day, lit by the number of
commits that day across the lab's public repositories, read from the GitHub
REST API. Run with a token in GITHUB_TOKEN (the scheduled workflow passes its
own):

    GITHUB_TOKEN=$(gh auth token) python3 profile/header/build.py

Only the standard library is used, so the workflow needs no install step.
"""

from __future__ import annotations

import base64
import datetime as dt
import html
import json
import math
import os
import pathlib
import re
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter

ORG = "velofy"
# Lab projects that live under the founder's account.
EXTRA_REPOS = ["anishfyi/curl_reap", "anishfyi/trove", "anishfyi/querion"]
OUT = pathlib.Path(__file__).resolve().parent
WEEKS = 53

# The intro, as on the velofy.co homepage. The second part is set in gold.
HEADLINE = ("Applied AI and security research", "for real work.")
LEDE = (
    "An applied AI and security lab in Delhi. We study how models find and fix "
    "vulnerabilities, build the tools agents run on, and publish what we measure."
)

# Text links in the row under the panel: slug, label, image width in pixels.
# Each width is the label set in Switzer at 15px, plus the arrow and a gap.
LINKS = [
    ("site", "velofy.co", 79),
    ("open-source", "Open source", 107),
    ("research", "Research", 85),
    ("bulletin", "Bulletin", 70),
    ("linkedin", "LinkedIn", 77),
    ("call", "Book a call", 92),
]
LINK_HEIGHT = 48  # a comfortable touch target when the row wraps on a phone
# The call to action is gold, as in the velofy.co navigation.
ACCENT_LINKS = {"call"}

# Foundry tokens. accent is an RGB triplet so the grid can use it at any opacity.
THEMES = {
    "dark": {
        "paper": "#000000",
        "ink": "#e6dec7",
        "accent": "200 173 134",
        "muted": "#9c9686",
        "line": "#2f2c27",
        "cell-fill": "#1d1b18",
    },
    "light": {
        "paper": "#f5efe0",
        "ink": "#17140e",
        "accent": "118 90 51",
        "muted": "#5f5849",
        "line": "#d6ccb4",
        "cell-fill": "#e8dfca",
    },
}
# Gold at rising opacity for commit levels 1 to 4.
LEVEL_ALPHA = [0.4, 0.6, 0.8, 1.0]

PANEL_HEIGHT = 364
# Grid cells grow to fill the panel's width, between these sizes in pixels. Below
# the smallest size the grid keeps its newest weeks and fades out on the left.
CELL_MIN, CELL_MAX, GAP = 10, 13, 3
PAD, PAD_NARROW = 28, 18
NARROW = 560  # container width below which the panel uses its phone layout
MONO_SIZE, MONO_TRACK = 11, 0.04
MONO_ADVANCE = 0.6  # Fragment Mono advance width, in ems

SWITZER_URL = "https://velofy.co/fonts/switzer/switzer-400.woff2"
SANS = '"Switzer",-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif'
MONO = '"Fragment Mono",ui-monospace,SFMono-Regular,Menlo,Consolas,monospace'


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


# ---------------------------------------------------------------- fonts


def font_face(family: str, data: str) -> str:
    if not data:
        return ""
    return (
        f'@font-face{{font-family:"{family}";font-weight:400;font-style:normal;'
        f'src:url(data:font/woff2;base64,{data}) format("woff2");}}'
    )


def switzer() -> str:
    """Switzer, base64 encoded.

    The font is not stored in this repository: its licence (the ITF Free Font
    License) lets the lab embed it in its own pages but not hand out the font
    file. velofy.co self-hosts it, so read it from there, and fall back to the
    copy embedded in the last build if the site cannot be reached.
    """
    try:
        request = urllib.request.Request(SWITZER_URL, headers={"User-Agent": "velofy-readme-header"})
        with urllib.request.urlopen(request, timeout=30) as response:
            data = response.read()
        if data[:4] == b"wOF2":
            return base64.b64encode(data).decode()
    except OSError as error:
        print(f"Could not fetch Switzer ({error}), reusing the last build's copy")
    pattern = re.compile(r'font-family:"Switzer";[^}]*?base64,([A-Za-z0-9+/=]+)\)')
    for path in sorted(OUT.glob("main-*.svg")):
        found = pattern.search(path.read_text())
        if found:
            return found.group(1)
    print("Switzer is unavailable, the header falls back to system fonts")
    return ""


def fragment_mono() -> str:
    # Fragment Mono is under the SIL Open Font License, so it ships here (fonts/).
    return base64.b64encode((OUT / "fonts" / "fragment-mono-400.woff2").read_bytes()).decode()


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
        '<span class="lockup">'
        f'<svg class="mark" viewBox="{mark_box}" xmlns="http://www.w3.org/2000/svg">{mark}</svg>'
        f'<svg class="word" viewBox="{word_box}" xmlns="http://www.w3.org/2000/svg">{word}</svg>'
        "</span>"
    )


def arrow(external: bool = True) -> str:
    """The arrow from velofy.co's text links, turned up and right for external ones."""
    turn = ' transform="rotate(-45 6 6)"' if external else ""
    return (
        '<svg class="arrow" viewBox="0 0 12 12" xmlns="http://www.w3.org/2000/svg">'
        f'<path d="M1 6h9M6.5 2.5L10 6l-3.5 3.5"{turn} fill="none" stroke="currentColor" '
        'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    )


# ---------------------------------------------------------------- svg


BASE_CSS = """
*, *::before, *::after { box-sizing: border-box; }
p, h1 { margin: 0; font: inherit; }
.root { font-family: SANS; font-weight: 400; color: var(--ink); -webkit-font-smoothing: antialiased; }
.mono { font-family: MONO; font-size: MONO_SIZEpx; letter-spacing: MONO_TRACKem; text-transform: uppercase; line-height: 1; }
.fade { animation: fade 1.2s ease-out var(--delay, 0.3s) both; }
@keyframes fade { from { opacity: 0; } to { opacity: 1; } }
@keyframes rise { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation: none !important; }
}
""".replace("SANS", SANS).replace("MONO_SIZE", str(MONO_SIZE)).replace("MONO_TRACK", str(MONO_TRACK)).replace("MONO", MONO)


def theme_css(theme: str) -> str:
    t = THEMES[theme]
    return ":root{" + "".join(f"--{k}:{v};" for k, v in t.items()) + "}"


def svg(theme: str, width: str, height: int, css: str, body: str, fonts: str) -> str:
    document = (
        f'<svg xmlns="http://www.w3.org/2000/svg" fill="none" width="{width}" height="{height}">'
        f"<style>{fonts}</style>"
        '<foreignObject width="100%" height="100%">'
        '<div xmlns="http://www.w3.org/1999/xhtml">'
        f"<style>{theme_css(theme)}{BASE_CSS}{css}</style>{body}"
        "</div></foreignObject></svg>\n"
    )
    # An image that is not well-formed XML shows as a broken icon, so refuse to
    # write one. (A bare "<" in the CSS is the usual culprit.)
    ET.fromstring(document)
    return document


def mono_width(text: str) -> float:
    return len(text) * MONO_SIZE * (MONO_ADVANCE + MONO_TRACK)


def words(text: str, start: int) -> str:
    return " ".join(
        f'<span class="w" style="--i:{start + i}">{html.escape(word)}</span>'
        for i, word in enumerate(text.split())
    )


def cell_at(width: float, pad: int) -> float:
    """Cell size in a panel whose content box is `width` pixels wide (CSS clamp)."""
    return min(CELL_MAX, max(CELL_MIN, (width - 2 * pad - (WEEKS - 1) * GAP) / WEEKS))


def width_for(cell: float, pad: int) -> float:
    """Smallest panel width at which cells reach `cell` pixels."""
    return WEEKS * cell + (WEEKS - 1) * GAP + 2 * pad


def since_labels(first: dt.date, weeks_before: int, now_label: str) -> list[tuple[str, int]]:
    """The labels for the first column, longest first, each with the smallest
    panel width at which it fits between that column and the date on the right.
    """
    choices = [
        f"First public commit, {first:%b %-d, %Y}",
        f"First commit, {first:%b %-d, %Y}",
        f"First commit, {first:%b %-d}",
        f"{first:%b %-d, %Y}",
    ]
    fits = []
    for text in choices:
        # Room between the first column and the right-hand label grows with the
        # cell size: (WEEKS - weeks_before) * (cell + GAP) - GAP.
        need = mono_width(text) + mono_width(now_label) + 24 + GAP
        cell = need / (WEEKS - weeks_before) - GAP
        if cell <= CELL_MIN:
            fits.append((text, 0))
        elif cell <= CELL_MAX:
            fits.append((text, math.ceil(width_for(cell, PAD)) + 2))
    return fits


def main(theme: str, today: dt.date, days: Counter, fonts: str) -> str:
    lit = levels(days)
    start = today - dt.timedelta(days=(today.isoweekday() % 7) + 7 * (WEEKS - 1))
    total = sum(n for day, n in days.items() if start <= day <= today)
    active = sorted(day for day in days if day <= today)
    first = active[0] if active else today
    # Data is read from a week before the grid starts, so a first day inside the
    # grid really is the lab's first public commit.
    is_first = first > start

    cells, order = [], 0
    for offset in range((today - start).days + 1):
        day = start + dt.timedelta(days=offset)
        level = lit.get(day, 0)
        if day < first:
            cells.append('<i class="c c--before"></i>')
            continue
        classes = "c"
        style = ""
        if level:
            classes += f" c{level} on"
            style = f' style="--o:{order}"'
        if day == today:
            classes += " today"
        order += 1
        cells.append(f'<i class="{classes}"{style}></i>')
    span = max(order, 1)

    now_label = today.strftime("%b %-d, %Y")
    weeks_before = max(0, (first - start).days // 7) if is_first else 0
    if is_first:
        labels = since_labels(first, weeks_before, now_label)
    else:
        labels = [(start.strftime("%b %-d, %Y"), 0)]
    # The grid is anchored to the right. Below this panel width it is clipped on
    # the left, and the first-column label goes once its column is cut off.
    clip_at = math.ceil(width_for(CELL_MIN, PAD)) + 2
    narrow_grid = WEEKS * (CELL_MIN + GAP) - GAP
    since_at = math.ceil(narrow_grid - weeks_before * (CELL_MIN + GAP) + 2 * PAD) + 2
    since_spans = "".join(
        f'<span class="since s{i}">{html.escape(text)}</span>' for i, (text, _) in enumerate(labels)
    )
    # Show the shortest label by default and swap in longer ones as room allows.
    since_css = "".join(
        f"@container (min-width: {at}px) {{ .since {{ display: none; }} .s{i} {{ display: inline; }} }}\n"
        for i, (_, at) in reversed(list(enumerate(labels)))
        if i < len(labels) - 1
    )
    legend = "".join(f'<i class="c c{n}"></i>' if n else '<i class="c"></i>' for n in range(5))

    css = f"""
.panel {{
  position: relative;
  block-size: {PANEL_HEIGHT}px;
  background: var(--paper);
  border: 1px solid var(--line);
  border-radius: 4px;
  overflow: hidden;
  container-type: inline-size;
}}
.inner {{
  --pad: {PAD}px;
  block-size: 100%;
  display: grid;
  grid-template-columns: repeat(6, minmax(0, 1fr));
  grid-template-rows: auto auto auto 1fr;
  column-gap: 16px;
  padding: 0 var(--pad) 24px;
}}
.bar {{ grid-column: 1 / -1; display: flex; align-items: center; justify-content: space-between; block-size: 60px; --delay: 0.1s; }}
.lockup {{ display: flex; align-items: center; gap: 11px; color: var(--ink); }}
.mark {{ inline-size: 22px; block-size: 22px; }}
.word {{ inline-size: 100px; block-size: 11.5px; }}
.place {{ color: var(--muted); }}
.headline {{
  grid-column: 1 / span 4;
  grid-row: 2;
  align-self: end;
  margin-top: 22px;
  font-size: 35px;
  line-height: 1.06;
  letter-spacing: -0.026em;
  text-wrap: balance;
}}
.headline .w {{ display: inline-block; animation: rise 0.9s cubic-bezier(0.22, 1, 0.36, 1) calc(0.25s + var(--i) * 0.06s) both; }}
.gold {{ color: rgb(var(--accent)); }}
.lede {{
  grid-column: 5 / span 2;
  grid-row: 2;
  align-self: end;
  font-size: 14.5px;
  line-height: 1.38;
  color: var(--muted);
  text-wrap: pretty;
  --delay: 0.8s;
}}
.lede-short {{ display: none; grid-column: 1 / -1; grid-row: 3; margin-top: 12px; font-size: 14.5px; line-height: 1.38; color: var(--muted); --delay: 0.8s; }}
.graph {{
  grid-column: 1 / -1;
  grid-row: 4;
  align-self: end;
  --delay: 1s;
  --cell: clamp({CELL_MIN}px, calc((100cqw - 2 * var(--pad) - {(WEEKS - 1) * GAP}px) / {WEEKS}), {CELL_MAX}px);
  --step: calc(var(--cell) + {GAP}px);
}}
.head, .foot {{ display: flex; justify-content: space-between; align-items: center; }}
.head {{ margin-bottom: 12px; color: var(--muted); }}
.count {{ color: rgb(var(--accent)); }}
.legend {{ display: flex; align-items: center; gap: 3px; }}
.legend .c {{ inline-size: 11px; block-size: 11px; }}
.legend span {{ margin: 0 5px; }}
.window {{ position: relative; block-size: calc(7 * var(--step) - {GAP}px); overflow: hidden; }}
.cells, .marks {{ position: absolute; right: 0; inline-size: calc({WEEKS} * var(--step) - {GAP}px); }}
.cells {{
  top: 0;
  display: grid;
  grid-template-rows: repeat(7, var(--cell));
  grid-auto-columns: var(--cell);
  grid-auto-flow: column;
  gap: {GAP}px;
}}
.c {{ display: block; inline-size: var(--cell); block-size: var(--cell); border-radius: 2px; background: var(--cell-fill); }}
/* Days before the lab's first public commit: a quiet lattice of points. */
.c--before {{ background: radial-gradient(circle, var(--line) 0 1.6px, transparent 2.1px); }}
""" + "".join(
        f".c{n} {{ --to: rgb(var(--accent) / {a}); background: var(--to); }}\n"
        for n, a in enumerate(LEVEL_ALPHA, start=1)
    ) + f"""
.on {{ animation: fill 0.8s ease-out calc(1.5s + var(--o) * {2.6 / span:.4f}s) both; }}
@keyframes fill {{
  from {{ background: var(--cell-fill); }}
  45% {{ background: rgb(var(--accent)); }}
  to {{ background: var(--to); }}
}}
.today {{ box-shadow: 0 0 0 1px rgb(var(--accent)); animation: fill 0.8s ease-out 4.2s both, pulse 2.8s ease-in-out 5s infinite; }}
.today:not(.on) {{ animation: pulse 2.8s ease-in-out 5s infinite; }}
@keyframes pulse {{ 50% {{ box-shadow: 0 0 0 1px rgb(var(--accent) / 0.2); }} }}
.foot {{ position: relative; block-size: {MONO_SIZE}px; margin-top: 12px; overflow: hidden; color: var(--muted); }}
.marks {{ top: 0; block-size: {MONO_SIZE}px; }}
.marks span {{ position: absolute; top: 0; white-space: nowrap; }}
.since {{ display: none; left: calc({weeks_before} * var(--step)); }}
.s{len(labels) - 1} {{ display: inline; }}
{since_css}.now {{ right: 0; }}
@container (max-width: {clip_at - 1}px) {{
  .window {{
    -webkit-mask-image: linear-gradient(to right, transparent, #000 64px);
    mask-image: linear-gradient(to right, transparent, #000 64px);
  }}
}}
@container (max-width: 759px) {{
  .headline {{ grid-column: 1 / -1; font-size: 32px; }}
  .lede {{ display: none; }}
  .lede-short {{ display: block; }}
}}
@container (max-width: {NARROW - 1}px) {{
  .inner {{ --pad: {PAD_NARROW}px; padding-bottom: 20px; }}
  .bar {{ block-size: 56px; }}
  .headline {{ font-size: 28px; line-height: 1.08; margin-top: 12px; }}
}}
@container (max-width: 399px) {{
  .legend {{ display: none; }}
}}
@container (max-width: {since_at - 1}px) {{
  .marks .since {{ display: none; }}
}}
"""
    headline = (
        f"{words(HEADLINE[0], 0)} "
        f'<span class="gold">{words(HEADLINE[1], len(HEADLINE[0].split()))}</span>'
    )
    body = (
        '<div class="root panel"><div class="inner">'
        f'<div class="bar fade">{lockup()}<span class="place mono">Delhi, India</span></div>'
        f'<h1 class="headline">{headline}</h1>'
        f'<p class="lede fade">{html.escape(LEDE)}</p>'
        f'<p class="lede-short fade">{html.escape(LEDE.split(". ")[0])}.</p>'
        '<div class="graph fade">'
        f'<div class="head mono"><span><span class="count">{total:,}</span> commits in the open</span>'
        f'<span class="legend"><span>Less</span>{legend}<span>More</span></span></div>'
        f'<div class="window"><div class="cells">{"".join(cells)}</div></div>'
        f'<div class="foot mono"><div class="marks">{since_spans}'
        f'<span class="now">{html.escape(now_label)}</span>'
        "</div></div></div>"
        "</div></div>"
    )
    return svg(theme, "100%", PANEL_HEIGHT, css, body, fonts)


def link(theme: str, slug: str, label: str, width: int, index: int, fonts: str) -> str:
    css = f"""
.wrapper {{ block-size: {LINK_HEIGHT}px; display: flex; align-items: flex-start; padding-top: 12px; }}
.link {{
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 15px;
  line-height: 20px;
  letter-spacing: -0.005em;
  white-space: nowrap;
  --delay: {0.5 + index * 0.08:.2f}s;
}}
.link.gold {{ color: rgb(var(--accent)); }}
.arrow {{ inline-size: 12px; block-size: 12px; flex: none; }}
"""
    gold = " gold" if slug in ACCENT_LINKS else ""
    body = (
        '<div class="root wrapper">'
        f'<div class="link fade{gold}"><span>{html.escape(label)}</span>{arrow()}</div>'
        "</div>"
    )
    return svg(theme, str(width), LINK_HEIGHT, css, body, fonts)


def build(today: dt.date | None = None) -> None:
    today = today or dt.datetime.now(dt.timezone.utc).date()
    days = commits_per_day(today - dt.timedelta(days=7 * WEEKS + 7))
    sans = font_face("Switzer", switzer())
    both = sans + font_face("Fragment Mono", fragment_mono())
    for theme in THEMES:
        (OUT / f"main-{theme}.svg").write_text(main(theme, today, days, both))
        for index, (slug, label, width) in enumerate(LINKS):
            (OUT / f"link-{slug}-{theme}.svg").write_text(link(theme, slug, label, width, index, sans))
    print(f"{sum(days.values())} commits on {len(days)} days, written to {OUT}")


if __name__ == "__main__":
    build()
