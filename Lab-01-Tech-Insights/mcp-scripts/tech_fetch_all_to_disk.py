import json
import sys
import asyncio
import httpx
import feedparser
from pathlib import Path
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
import os

sys.stdout.reconfigure(encoding='utf-8')

BASE_PATH = Path(__file__).parent.parent
INPUT_FILE = BASE_PATH / "output" / "source_list.json"
OUTPUT_FILE = BASE_PATH / "output" / "raw_signals.json"


def _parse_published(entry) -> datetime | None:
    """Return UTC-aware datetime from feedparser entry, or None if unavailable."""
    t = entry.get("published_parsed") or entry.get("updated_parsed")
    if t:
        try:
            return datetime(*t[:6], tzinfo=timezone.utc)
        except Exception:
            pass
    return None


async def fetch_one(client, source, cutoff: datetime):
    try:
        print(f"正在抓取: {source['name']}...")
        resp = await client.get(source['url'], timeout=15.0)
        feed = feedparser.parse(resp.text)
        articles = []
        for e in feed.entries[:25]:
            published = _parse_published(e)
            # Keep article if within time window, or if no timestamp (can't filter)
            if published and published < cutoff:
                continue
            articles.append({
                "title": e.get("title", ""),
                "link": e.get("link", ""),
                "summary": e.get("summary", ""),
                "source_name": source['name'],
                "signal_level": source.get("signal_level", "B"),
                "published_at": published.isoformat() if published else None,
            })
        return articles
    except Exception as e:
        print(f"❌ {source['name']} 抓取失败: {e}")
        return []


async def main():
    load_dotenv(BASE_PATH / ".env")
    hours = int(os.environ.get("TIME_WINDOW_HOURS", "24"))
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    print(f"⏱  时间窗口: 最近 {hours} 小时（{cutoff.strftime('%Y-%m-%d %H:%M')} UTC 之后）")

    if not INPUT_FILE.exists():
        print(f"❌ 找不到 {INPUT_FILE}")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        sources = json.load(f)

    async with httpx.AsyncClient(follow_redirects=True) as client:
        tasks = [fetch_one(client, s, cutoff) for s in sources]
        results = await asyncio.gather(*tasks)

    all_articles = [a for sub in results for a in sub]
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_articles, f, indent=2, ensure_ascii=False)
    print(f"✅ 抓取完成，共 {len(all_articles)} 条信号（时间窗口内），已存至 raw_signals.json")

if __name__ == "__main__":
    asyncio.run(main())
