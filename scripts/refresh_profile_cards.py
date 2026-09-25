#!/usr/bin/env python3
"""Refresh the profile cards, preserving each last good SVG on provider errors."""

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
COMMON = {
    "username": "FsKummer",
    "hide_border": "true",
    "title_color": "79E3D2",
    "icon_color": "79E3D2",
    "text_color": "C7D7E0",
    "bg_color": "0D1826",
    "border_radius": "12",
}
CARDS = {
    "stats": (
        "https://github-stats-extended.vercel.app/api?" + urlencode({
            **COMMON,
            "show_icons": "true",
            "hide": "stars",
            "hide_rank": "true",
            "include_all_commits": "false",
            "custom_title": "Public GitHub stats",
            "card_width": "430",
            "line_height": "30",
        }),
        ("Total Commits", "Total PRs"),
    ),
    "languages": (
        "https://github-stats-extended.vercel.app/api/top-langs/?" + urlencode({
            **COMMON,
            "layout": "compact",
            "langs_count": "8",
            "hide": "html,Tcl",
            "card_width": "360",
        }),
        ("Most Used Languages", "%"),
    ),
    "streak": (
        "https://streak-stats.demolab.com/?" + urlencode({
            "user": "FsKummer",
            "hide_border": "true",
            "background": "0D1826",
            "ring": "79E3D2",
            "fire": "79E3D2",
            "currStreakNum": "EAF4F8",
            "sideNums": "EAF4F8",
            "currStreakLabel": "79E3D2",
            "sideLabels": "C7D7E0",
            "dates": "91A8B6",
            "stroke": "294354",
            "border_radius": "12",
        }),
        ("Total Contributions", "Current Streak", "Longest Streak"),
    ),
    "trophies": (
        "https://trophy.ryglcloud.net/?" + urlencode({
            "username": "FsKummer",
            "theme": "algolia",
            "no-bg": "false",
            "no-frame": "true",
            "row": "1",
            "column": "6",
            "margin-w": "10",
            "title": "Commits,Repositories,PullRequest,Issues,Followers,Stars",
        }),
        ("Commits", "Repositories", "PullRequest"),
    ),
}


def validate_svg(data, labels):
    svg = ET.fromstring(data)
    if svg.tag != "{http://www.w3.org/2000/svg}svg":
        raise ValueError("Response is not an SVG")
    text = " ".join("".join(node.itertext()) for node in svg.iter()
                    if node.tag.rsplit("}", 1)[-1] == "text")
    if not all(label in text for label in labels):
        raise ValueError("Card is missing expected data labels")
    return b"\n".join(line.rstrip() for line in data.splitlines()).strip() + b"\n"


def download_card(name):
    url, labels = CARDS[name]
    request = Request(url, headers={"User-Agent": "FsKummer-profile-cards"})
    with urlopen(request, timeout=45) as response:
        data = response.read(1_000_001)
    if len(data) > 1_000_000:
        raise ValueError("Card response exceeds 1 MB")
    return validate_svg(data, labels)


def refresh_all(directory):
    directory.mkdir(parents=True, exist_ok=True)
    failures = 0
    with ThreadPoolExecutor(max_workers=4) as executor:
        pending = {name: executor.submit(download_card, name) for name in CARDS}
        for name, future in pending.items():
            path = directory / f"{name}.svg"
            try:
                data = future.result()
                if not path.exists() or path.read_bytes() != data:
                    temporary = path.with_suffix(".svg.tmp")
                    temporary.write_bytes(data)
                    temporary.replace(path)
                print(f"Verified {path.name}")
            except Exception as error:
                failures += 1
                print(f"::warning::{name}: {error}; previous card preserved", file=sys.stderr)
    return failures


if __name__ == "__main__":
    sys.exit(1 if refresh_all(ROOT / "assets") else 0)
