import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class Song:
    """Represents a song and its audio/metadata attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float
    popularity: int = 50
    release_decade: int = 2020
    mood_tag: str = ""
    lyrics_language: str = "en"
    instrumentalness: float = 0.5

@dataclass
class UserProfile:
    """Represents a user's taste preferences for scoring."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    preferred_decade: int = 0
    preferred_mood_tags: list = field(default_factory=list)
    likes_instrumental: bool = False
    preferred_language: str = ""


# ---------------------------------------------------------------------------
# Challenge 2: Scoring modes (Strategy pattern)
# ---------------------------------------------------------------------------

SCORING_MODES = {
    "balanced": {
        "genre": 2.0, "mood": 1.0, "energy": 1.0, "acoustic": 0.5,
        "popularity": 0.3, "decade": 0.5, "mood_tag": 0.5,
        "instrumental": 0.3, "language": 0.2,
    },
    "genre-first": {
        "genre": 3.5, "mood": 0.5, "energy": 0.5, "acoustic": 0.25,
        "popularity": 0.15, "decade": 0.25, "mood_tag": 0.25,
        "instrumental": 0.15, "language": 0.1,
    },
    "mood-first": {
        "genre": 0.5, "mood": 3.0, "energy": 0.5, "acoustic": 0.25,
        "popularity": 0.15, "decade": 0.25, "mood_tag": 1.5,
        "instrumental": 0.15, "language": 0.1,
    },
    "energy-focused": {
        "genre": 0.5, "mood": 0.5, "energy": 3.0, "acoustic": 0.25,
        "popularity": 0.15, "decade": 0.25, "mood_tag": 0.25,
        "instrumental": 0.15, "language": 0.1,
    },
}


# ---------------------------------------------------------------------------
# CSV loader
# ---------------------------------------------------------------------------

def load_songs(csv_path: str) -> List[Dict]:
    """Read songs from a CSV file and return a list of dicts with numeric fields cast."""
    songs = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            row["popularity"] = int(row.get("popularity", 50))
            row["release_decade"] = int(row.get("release_decade", 2020))
            row["instrumentalness"] = float(row.get("instrumentalness", 0.5))
            songs.append(row)
    return songs


# ---------------------------------------------------------------------------
# Scoring (functional interface)
# ---------------------------------------------------------------------------

def score_song(
    user_prefs: Dict, song: Dict, mode: str = "balanced"
) -> Tuple[float, List[str]]:
    """Score a single song against user preferences using a named scoring mode."""
    w = SCORING_MODES[mode]
    score = 0.0
    reasons: List[str] = []

    # Genre match
    if song["genre"] == user_prefs.get("favorite_genre", ""):
        pts = w["genre"]
        score += pts
        reasons.append(f"genre match (+{pts:.2f})")

    # Mood match
    if song["mood"] == user_prefs.get("favorite_mood", ""):
        pts = w["mood"]
        score += pts
        reasons.append(f"mood match (+{pts:.2f})")

    # Energy similarity (scaled by weight)
    target_energy = user_prefs.get("target_energy", 0.5)
    energy_pts = w["energy"] * (1.0 - abs(song["energy"] - target_energy))
    score += energy_pts
    reasons.append(f"energy similarity (+{energy_pts:.2f})")

    # Acoustic bonus
    if user_prefs.get("likes_acoustic", False) and song["acousticness"] > 0.6:
        pts = w["acoustic"]
        score += pts
        reasons.append(f"acoustic bonus (+{pts:.2f})")

    # --- Challenge 1: Advanced features ---

    # Popularity (scaled 0-1 from 0-100, then multiplied by weight)
    pop_pts = w["popularity"] * (song.get("popularity", 50) / 100.0)
    score += pop_pts
    reasons.append(f"popularity (+{pop_pts:.2f})")

    # Decade match
    preferred_decade = user_prefs.get("preferred_decade", 0)
    if preferred_decade and song.get("release_decade") == preferred_decade:
        pts = w["decade"]
        score += pts
        reasons.append(f"decade match (+{pts:.2f})")

    # Mood tag match
    preferred_tags = user_prefs.get("preferred_mood_tags", [])
    song_tag = song.get("mood_tag", "")
    if preferred_tags and song_tag in preferred_tags:
        pts = w["mood_tag"]
        score += pts
        reasons.append(f"mood tag '{song_tag}' (+{pts:.2f})")

    # Instrumental bonus
    if user_prefs.get("likes_instrumental", False) and song.get("instrumentalness", 0) > 0.6:
        pts = w["instrumental"]
        score += pts
        reasons.append(f"instrumental bonus (+{pts:.2f})")

    # Language match
    preferred_lang = user_prefs.get("preferred_language", "")
    if preferred_lang and song.get("lyrics_language", "") == preferred_lang:
        pts = w["language"]
        score += pts
        reasons.append(f"language match (+{pts:.2f})")

    return score, reasons


# ---------------------------------------------------------------------------
# Challenge 3: Diversity penalty
# ---------------------------------------------------------------------------

def _apply_diversity(
    scored: List[Tuple[Dict, float, List[str]]], k: int
) -> List[Tuple[Dict, float, List[str]]]:
    """Greedily select top k songs, penalizing repeated artists (-1.0) and genres (-0.5)."""
    selected: List[Tuple[Dict, float, List[str]]] = []
    seen_artists: set = set()
    seen_genres: set = set()
    candidates = list(scored)

    while len(selected) < k and candidates:
        best_idx = 0
        best_adjusted = -float("inf")

        for i, (song, base_score, _reasons) in enumerate(candidates):
            adjusted = base_score
            if song["artist"] in seen_artists:
                adjusted -= 1.0
            if song["genre"] in seen_genres:
                adjusted -= 0.5
            if adjusted > best_adjusted:
                best_adjusted = adjusted
                best_idx = i

        song, base_score, reasons = candidates.pop(best_idx)
        penalty_reasons = list(reasons)
        if song["artist"] in seen_artists:
            penalty_reasons.append("artist repeat (-1.00)")
        if song["genre"] in seen_genres:
            penalty_reasons.append("genre repeat (-0.50)")

        selected.append((song, best_adjusted, penalty_reasons))
        seen_artists.add(song["artist"])
        seen_genres.add(song["genre"])

    return selected


# ---------------------------------------------------------------------------
# Recommendation (functional interface)
# ---------------------------------------------------------------------------

def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    mode: str = "balanced",
    diversity: bool = False,
) -> List[Tuple[Dict, float, str]]:
    """Score all songs, optionally apply diversity, return top k as (song, score, explanation)."""
    scored = []
    for song in songs:
        song_score, reasons = score_song(user_prefs, song, mode=mode)
        scored.append((song, song_score, reasons))

    scored.sort(key=lambda x: x[1], reverse=True)

    if diversity:
        top = _apply_diversity(scored, k)
    else:
        top = scored[:k]

    return [(song, sc, "; ".join(reasons)) for song, sc, reasons in top]


# ---------------------------------------------------------------------------
# OOP interface (used by tests/test_recommender.py)
# ---------------------------------------------------------------------------

def _score_song_obj(song: Song, user: UserProfile) -> float:
    """Score a Song dataclass against a UserProfile. Uses original 4-factor formula."""
    score = 0.0

    if song.genre == user.favorite_genre:
        score += 2.0

    if song.mood == user.favorite_mood:
        score += 1.0

    score += 1.0 - abs(song.energy - user.target_energy)

    if user.likes_acoustic and song.acousticness > 0.6:
        score += 0.5

    return score


def _build_explanation(song: Song, user: UserProfile) -> str:
    """Build a human-readable explanation string for a Song/UserProfile pair."""
    parts = []

    if song.genre == user.favorite_genre:
        parts.append("genre match (+2.0)")

    if song.mood == user.favorite_mood:
        parts.append("mood match (+1.0)")

    energy_score = 1.0 - abs(song.energy - user.target_energy)
    parts.append(f"energy similarity (+{energy_score:.2f})")

    if user.likes_acoustic and song.acousticness > 0.6:
        parts.append("acoustic bonus (+0.50)")

    return "; ".join(parts)


class Recommender:
    """OOP recommender that scores and ranks Song objects for a UserProfile."""
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs sorted by descending score."""
        scored = sorted(self.songs, key=lambda s: _score_song_obj(s, user), reverse=True)
        return scored[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation for why a song was recommended."""
        return _build_explanation(song, user)
