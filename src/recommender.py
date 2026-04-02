import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

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

@dataclass
class UserProfile:
    """Represents a user's taste preferences for scoring."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


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
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a single song against user preferences, returning (score, reasons)."""
    score = 0.0
    reasons = []

    # Genre match: +2.0
    if song["genre"] == user_prefs.get("favorite_genre", ""):
        score += 2.0
        reasons.append(f"genre match (+2.0)")

    # Mood match: +1.0
    if song["mood"] == user_prefs.get("favorite_mood", ""):
        score += 1.0
        reasons.append(f"mood match (+1.0)")

    # Energy similarity: +0.0 to +1.0
    target_energy = user_prefs.get("target_energy", 0.5)
    energy_score = 1.0 - abs(song["energy"] - target_energy)
    score += energy_score
    reasons.append(f"energy similarity (+{energy_score:.2f})")

    # Acousticness bonus: +0.5 if user likes acoustic and song > 0.6
    if user_prefs.get("likes_acoustic", False) and song["acousticness"] > 0.6:
        score += 0.5
        reasons.append(f"acoustic bonus (+0.50)")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score all songs, sort by descending score, and return the top k as (song, score, explanation)."""
    scored = []
    for song in songs:
        song_score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons)
        scored.append((song, song_score, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]


# ---------------------------------------------------------------------------
# OOP interface (used by tests/test_recommender.py)
# ---------------------------------------------------------------------------

def _score_song_obj(song: Song, user: UserProfile) -> float:
    """Score a Song dataclass against a UserProfile. Max 4.5, min 0.0."""
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
        parts.append(f"genre match (+2.0)")

    if song.mood == user.favorite_mood:
        parts.append(f"mood match (+1.0)")

    energy_score = 1.0 - abs(song.energy - user.target_energy)
    parts.append(f"energy similarity (+{energy_score:.2f})")

    if user.likes_acoustic and song.acousticness > 0.6:
        parts.append(f"acoustic bonus (+0.50)")

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
