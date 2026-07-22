#!/usr/bin/env python3
"""Fetch blog RSS/Atom feeds listed in config.json and write assets/writing.json.
Runs daily via GitHub Actions — no manual steps. Stdlib only."""
import json, re, html, sys, urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

CONFIG = "config.json"
OUT = "assets/writing.json"
UA = {"User-Agent": "Mozilla/5.0 (portfolio-sync)"}

def text(el):
    return (el.text or "").strip() if el is not None else ""

def strip_html(s, limit=180):
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(re.sub(r"\s+", " ", s)).strip()
    return (s[:limit].rsplit(" ", 1)[0] + "…") if len(s) > limit else s

def parse_date(s):
    if not s: return None
    try: return parsedate_to_datetime(s)
    except Exception: pass
    for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S.%f%z", "%Y-%m-%dT%H:%M:%SZ"):
        try:
            d = datetime.strptime(s.replace("Z", "+0000") if fmt.endswith("%z") else s, fmt)
            return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
        except Exception: continue
    return None

def parse_feed(xml_bytes, source_name):
    root = ET.fromstring(xml_bytes)
    ns = {"atom": "http://www.w3.org/2005/Atom", "content": "http://purl.org/rss/1.0/modules/content/"}
    posts = []
    # RSS 2.0
    for item in root.iter("item"):
        title = text(item.find("title"))
        link = text(item.find("link"))
        desc = text(item.find("description")) or text(item.find("content:encoded", ns))
        d = parse_date(text(item.find("pubDate")))
        if title and link:
            posts.append({"title": title, "link": link, "excerpt": strip_html(desc),
                          "date": d.strftime("%Y-%m-%d") if d else "", "ts": d.timestamp() if d else 0,
                          "source": source_name})
    # Atom
    if not posts:
        for entry in root.iter("{http://www.w3.org/2005/Atom}entry"):
            title = text(entry.find("atom:title", ns))
            link_el = entry.find("atom:link[@rel='alternate']", ns) or entry.find("atom:link", ns)
            link = link_el.get("href") if link_el is not None else ""
            desc = text(entry.find("atom:summary", ns)) or text(entry.find("atom:content", ns))
            d = parse_date(text(entry.find("atom:published", ns)) or text(entry.find("atom:updated", ns)))
            if title and link:
                posts.append({"title": title, "link": link, "excerpt": strip_html(desc),
                              "date": d.strftime("%Y-%m-%d") if d else "", "ts": d.timestamp() if d else 0,
                              "source": source_name})
    return posts

def main():
    cfg = json.load(open(CONFIG))
    feeds = [f for f in cfg.get("feeds", []) if f.get("url") and "REPLACE" not in f["url"]]
    all_posts = []
    for f in feeds:
        try:
            req = urllib.request.Request(f["url"], headers=UA)
            data = urllib.request.urlopen(req, timeout=30).read()
            posts = parse_feed(data, f.get("name", ""))
            all_posts.extend(posts)
            print(f"OK  {f['url']} -> {len(posts)} posts")
        except Exception as e:
            print(f"FAIL {f['url']}: {e}", file=sys.stderr)
    all_posts.sort(key=lambda p: p["ts"], reverse=True)
    for p in all_posts: p.pop("ts", None)
    out = {"updated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
           "posts": all_posts[: cfg.get("max_posts", 100)]}
    json.dump(out, open(OUT, "w"), ensure_ascii=False, indent=1)
    print(f"wrote {OUT}: {len(out['posts'])} posts")

if __name__ == "__main__":
    main()
