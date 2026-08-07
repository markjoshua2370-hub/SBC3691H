"""
Thin wrapper around the PandaScore API (pandascore.co).

Free tier: sign up at https://app.pandascore.co/signup (no credit card needed).
Gives schedules, results, and pre-match data (teams/tournaments) for free, at
1,000 requests/hour. Live in-progress scores need a paid plan, so this wrapper
sticks to upcoming and past matches, which the free tier covers.

Set your token as the PANDASCORE_TOKEN environment variable.
"""

import os
import requests

BASE_URL = "https://api.pandascore.co"

# Common game slugs PandaScore uses
GAMES = {
    "lol": "league-of-legends",
    "csgo": "csgo",
    "cs2": "csgo",  # PandaScore still uses the csgo slug for CS2 matches
    "dota2": "dota2",
    "valorant": "valorant",
}


def _headers() -> dict:
    token = os.environ["PANDASCORE_TOKEN"]
    return {"Authorization": f"Bearer {token}"}


def get_upcoming_matches(game_slug: str, per_page: int = 10) -> list[dict]:
    resp = requests.get(
        f"{BASE_URL}/{game_slug}/matches/upcoming",
        headers=_headers(),
        params={"per_page": per_page, "sort": "begin_at"},
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()


def get_past_matches(game_slug: str, per_page: int = 5) -> list[dict]:
    resp = requests.get(
        f"{BASE_URL}/{game_slug}/matches/past",
        headers=_headers(),
        params={"per_page": per_page, "sort": "-begin_at"},
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()


def get_match(match_id: int) -> dict:
    resp = requests.get(f"{BASE_URL}/matches/{match_id}", headers=_headers(), timeout=15)
    resp.raise_for_status()
    return resp.json()
