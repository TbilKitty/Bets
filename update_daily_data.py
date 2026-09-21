"""Optional GitHub Actions updater.

Uses permitted API endpoints and records source metadata. It intentionally does
not scrape article pages or convert a headline into a confirmed injury status.
"""
from __future__ import annotations

import csv
import datetime as dt
import json
import os
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def fetch_json(url: str) -> dict:
    request = Request(url, headers={"User-Agent": "GameEdgeTracker/1.0"})
    with urlopen(request, timeout=20) as response:  # nosec B310: configured HTTPS endpoint
        return json.loads(response.read().decode("utf-8"))


def odds_rows() -> list[dict]:
    key = os.environ.get("ODDS_API_KEY")
    if not key:
        return []
    query = urlencode({"apiKey": key, "regions": "us", "markets": "h2h", "oddsFormat": "american"})
    events = fetch_json(f"https://api.the-odds-api.com/v4/sports/basketball_nba/odds/?{query}")
    rows = []
    today = dt.date.today().isoformat()
    for event in events:
        commence = event.get("commence_time", "")
        rows.append({
            "game_date": commence[:10] or today,
            "start_time_et": commence,
            "away_team": event.get("away_team", ""),
            "home_team": event.get("home_team", ""),
            "market_implied_home_win_prob": "",
            "availability_edge": 0,
            "availability_note": "Confirm against official injury report",
            "news_confirmed": "no",
            "rest_edge": 0,
            "travel_edge": 0,
            "net_rating_edge": 0,
        })
    return rows


def write_daily(rows: list[dict]) -> None:
    fields = ["game_date", "start_time_et", "away_team", "home_team", "market_implied_home_win_prob", "availability_edge", "availability_note", "news_confirmed", "rest_edge", "travel_edge", "net_rating_edge"]
    with (DATA / "daily_game_inputs.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def append_log(message: str) -> None:
    path = DATA / "source_log.csv"
    with path.open("a", newline="", encoding="utf-8") as file:
        csv.writer(file).writerow([dt.datetime.now(dt.UTC).isoformat(), "API", "NBA", "", message, "https://the-odds-api.com/", "API source", "no"])


if __name__ == "__main__":
    rows = odds_rows()
    if rows:
        write_daily(rows)
        append_log(f"Loaded {len(rows)} NBA events; enter injury and factor values before use.")
    else:
        append_log("No update: configure ODDS_API_KEY to load an NBA slate.")
