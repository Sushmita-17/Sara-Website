"""Extract public product images from facebook.com/saraorganics.np page HTML."""
from __future__ import annotations

import json
import re
from pathlib import Path

import httpx

FB_PAGES = (
    "https://mbasic.facebook.com/saraorganics.np/",
    "https://m.facebook.com/saraorganics.np/",
    "https://www.facebook.com/saraorganics.np/",
)
OUT_JSON = Path(__file__).resolve().parent / "sara_fb_images.json"

# Known product keywords -> image URL from page posts (alt text / visible content)
# Updated when fetch_facebook_images.py runs or from manual curation
FB_PRODUCT_HINTS = [
    ("henna powder", "Henna Powder"),
    ("moringa powder", "Moringa Powder"),
    ("black seed oil", "Black Seed Oil"),
    ("aloe vera", "Aloe Vera Gel"),
    ("rose water", "Rose Water"),
    ("shilajit", "Shilajit"),
    ("spirulina", "Spirulina Powder"),
    ("turmeric", "Wild Turmeric"),
    ("chia seed", "Chia Seed"),
    ("neem", "Neem Oil"),
    ("lavender", "Lavender Oil"),
    ("triphala", "Triphala Powder"),
    ("ashwagandha", "Ashwagandha Powder"),
]


def _upgrade_fb_image_url(url: str) -> str:
    """Prefer larger Facebook CDN variant when possible."""
    if "fbcdn.net" not in url and "scontent" not in url:
        return url
    return re.sub(r"stp=dst-jpg_s\d+x\d+[^&]*", "stp=dst-jpg_s960x960", url)


def _extract_image_urls(html: str) -> list[str]:
    pattern = r"https://scontent[^\"'\s<>]+?\.(?:jpg|jpeg|png)(?:\?[^\"'\s<>]*)?"
    found = re.findall(pattern, html, flags=re.IGNORECASE)
    urls = []
    seen = set()
    for u in found:
        if "_n." not in u and ".png" not in u.lower():
            continue
        if "static.xx.fbcdn" in u:
            continue
        key = u.split("?")[0]
        if key in seen:
            continue
        seen.add(key)
        urls.append(_upgrade_fb_image_url(u))
    return urls


def _extract_alt_product_map(html: str) -> dict[str, str]:
    """Map product-like phrases in alt text to nearby image URLs."""
    mapping: dict[str, str] = {}
    for m in re.finditer(
        r'alt="([^"]{10,300})"[^>]*src="(https://scontent[^"]+)"',
        html,
        flags=re.IGNORECASE | re.DOTALL,
    ):
        alt, img = m.group(1), _upgrade_fb_image_url(m.group(2))
        low = alt.lower()
        for needle, label in FB_PRODUCT_HINTS:
            if needle in low:
                mapping.setdefault(label, img)
    return mapping


def fetch_facebook_product_images() -> dict[str, str]:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }
    html = ""
    with httpx.Client(headers=headers, timeout=30, follow_redirects=True) as client:
        for page_url in FB_PAGES:
            try:
                r = client.get(page_url)
                if r.status_code == 200 and len(r.text) > len(html):
                    html = r.text
            except httpx.HTTPError:
                continue

    if not html:
        return _seed_images()

    by_alt = _extract_alt_product_map(html)
    urls = _extract_image_urls(html)

    pool = {f"fb_image_{i + 1}": u for i, u in enumerate(urls[:40])}
    pool.update(by_alt)
    return pool if pool else _seed_images()


def _seed_images() -> dict[str, str]:
    """Curated Sara Organics Facebook CDN images (from public page posts)."""
    return {
        "Henna Powder": "https://scontent-mxp1-1.xx.fbcdn.net/v/t39.30808-6/702604421_122217217298350145_8407654073845047177_n.jpg",
        "fb_image_1": "https://scontent-mxp1-1.xx.fbcdn.net/v/t39.30808-6/703136085_122217216140350145_1080256763847688340_n.jpg",
        "fb_image_2": "https://scontent-mxp2-1.xx.fbcdn.net/v/t39.30808-6/703456070_122217117530350145_2388126606243033628_n.jpg",
        "fb_image_3": "https://scontent-mxp1-1.xx.fbcdn.net/v/t39.30808-6/703449124_122217116804350145_6084101242014943_n.jpg",
        "fb_image_4": "https://scontent-mxp2-1.xx.fbcdn.net/v/t39.30808-6/701537587_122217002144350145_1239674504492532443_n.jpg",
        "fb_image_5": "https://scontent-mxp1-1.xx.fbcdn.net/v/t39.30808-6/702501949_122217000068350145_8530085172397341904_n.jpg",
        "fb_image_6": "https://scontent-mxp1-1.xx.fbcdn.net/v/t39.30808-6/702590165_122216998700350145_1920966941543162288_n.jpg",
        "fb_image_7": "https://scontent-mxp2-1.xx.fbcdn.net/v/t39.30808-6/702539163_122216894744350145_2554924921239231764_n.jpg",
        "fb_image_8": "https://scontent-mxp2-1.xx.fbcdn.net/v/t39.30808-6/702603708_122216893982350145_4912249063400638832_n.jpg",
    }


def main():
    images = fetch_facebook_product_images()
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(dict(sorted(images.items())), f, ensure_ascii=False, indent=2)
    print(f"Saved {len(images)} Facebook images -> {OUT_JSON}")


if __name__ == "__main__":
    main()
