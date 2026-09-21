"""NFL daily slate updater for GitHub Actions.

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
    events = fetch_json(f"https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds/?{query}")
    rows = []
    today = dt.date.today().isoformat()
    for event in events:
        commence = event.get("commence_time", "")
        home_probability = ""
        for bookmaker in event.get("bookmakers", []):
            if bookmaker.get("key") != "draftkings":
                continue
            market = next((item for item in bookmaker.get("markets", []) if item.get("key") == "h2h"), None)
            if not market:
                continue
            prices = {outcome.get("name"): outcome.get("price") for outcome in market.get("outcomes", [])}
            home_price, away_price = prices.get(event.get("home_team")), prices.get(event.get("away_team"))
            if isinstance(home_price, int) and isinstance(away_price, int):
                raw_home = (-home_price / (-home_price + 100)) if home_price < 0 else (100 / (home_price + 100))
                raw_away = (-away_price / (-away_price + 100)) if away_price < 0 else (100 / (away_price + 100))
                home_probability = f"{raw_home / (raw_home + raw_away):.4f}"
            break
        rows.append({
            "game_date": commence[:10] or today,
            "start_time_et": commence,
            "away_team": event.get("away_team", ""),
            "home_team": event.get("home_team", ""),
            "market_implied_home_win_prob": "",
            "availability_edge": 0,
            "availability_note": "Confirm against official NFL injury report",
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
        csv.writer(file).writerow([dt.datetime.now(dt.UTC).isoformat(), "API", "NFL", "", message, "https://the-odds-api.com/", "API source", "no"])


if __name__ == "__main__":
    rows = odds_rows()
    if rows:
        write_daily(rows)
        append_log(f"Loaded {len(rows)} NFL events; enter injury and factor values before use.")
    else:
        write_daily([])
        append_log("No update: configure ODDS_API_KEY to load the NFL slate.")
