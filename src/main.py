"""
Command line runner for the Music Recommender Simulation.

Demonstrates all four challenges:
  1. Advanced song features (popularity, decade, mood_tag, language, instrumentalness)
  2. Multiple scoring modes (balanced, genre-first, mood-first, energy-focused)
  3. Diversity penalty (penalizes repeated artists/genres in top results)
  4. Visual summary table (tabulate)
"""

from tabulate import tabulate
from src.recommender import load_songs, recommend_songs, SCORING_MODES


# ---------------------------------------------------------------------------
# Challenge 4: formatted table output
# ---------------------------------------------------------------------------

def print_table(
    label: str, user_prefs: dict, results: list, compact: bool = False
) -> None:
    """Print a recommendation result set as a formatted ASCII table."""
    print(f"\n  {label}")
    if not compact:
        parts = [
            f"Genre: {user_prefs['favorite_genre']}",
            f"Mood: {user_prefs['favorite_mood']}",
            f"Energy: {user_prefs['target_energy']}",
        ]
        if user_prefs.get("preferred_mood_tags"):
            parts.append(f"Tags: {user_prefs['preferred_mood_tags']}")
        print(f"  {' | '.join(parts)}")

    rows = []
    for rank, (song, score, explanation) in enumerate(results, 1):
        rows.append([
            rank,
            song["title"],
            song["artist"],
            f"{score:.2f}",
            explanation,
        ])

    table = tabulate(
        rows,
        headers=["#", "Title", "Artist", "Score", "Reasons"],
        tablefmt="simple_outline",
        maxcolwidths=[None, 22, 16, None, 48],
    )
    print(table)


# ---------------------------------------------------------------------------
# User profiles (with Challenge 1 advanced preferences)
# ---------------------------------------------------------------------------

PROFILES = {
    "Chill Lofi Listener": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.4,
        "likes_acoustic": True,
        "preferred_decade": 2020,
        "preferred_mood_tags": ["nostalgic", "focused"],
        "likes_instrumental": True,
        "preferred_language": "en",
    },
    "High-Energy Pop Fan": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.85,
        "likes_acoustic": False,
        "preferred_decade": 2020,
        "preferred_mood_tags": ["euphoric", "uplifting"],
        "preferred_language": "en",
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.9,
        "likes_acoustic": False,
        "preferred_decade": 2010,
        "preferred_mood_tags": ["aggressive"],
        "preferred_language": "en",
    },
    "Contradictory (pop + sad + high energy)": {
        "favorite_genre": "pop",
        "favorite_mood": "sad",
        "target_energy": 0.9,
        "likes_acoustic": True,
        "preferred_decade": 2020,
        "preferred_mood_tags": ["melancholy", "euphoric"],
        "preferred_language": "en",
    },
    "Ghost Genre (reggaeton)": {
        "favorite_genre": "reggaeton",
        "favorite_mood": "happy",
        "target_energy": 0.7,
        "likes_acoustic": False,
        "preferred_decade": 2020,
        "preferred_mood_tags": ["warm", "uplifting"],
        "preferred_language": "en",
    },
}


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # ── All profiles in balanced mode with diversity ──────────────
    print("\n" + "=" * 70)
    print("  ALL PROFILES  (balanced mode, diversity ON)")
    print("=" * 70)
    for name, prefs in PROFILES.items():
        results = recommend_songs(prefs, songs, k=5, mode="balanced", diversity=True)
        print_table(name, prefs, results)

    # ── Challenge 2: Scoring mode comparison ──────────────────────
    print("\n" + "=" * 70)
    print("  SCORING MODE COMPARISON  (Chill Lofi, top 3, diversity OFF)")
    print("=" * 70)
    lofi = PROFILES["Chill Lofi Listener"]
    for mode in SCORING_MODES:
        results = recommend_songs(lofi, songs, k=3, mode=mode, diversity=False)
        print_table(f"[{mode}]", lofi, results, compact=True)

    # ── Challenge 3: Diversity penalty demo ───────────────────────
    print("\n" + "=" * 70)
    print("  DIVERSITY PENALTY DEMO  (Chill Lofi, balanced)")
    print("=" * 70)
    off = recommend_songs(lofi, songs, k=5, mode="balanced", diversity=False)
    on = recommend_songs(lofi, songs, k=5, mode="balanced", diversity=True)
    print_table("Diversity OFF", lofi, off, compact=True)
    print_table("Diversity ON", lofi, on, compact=True)


if __name__ == "__main__":
    main()
