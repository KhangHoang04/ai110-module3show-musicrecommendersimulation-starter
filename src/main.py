"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def run_profile(name: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Run the recommender for a single profile and print results."""
    print(f"\n{'=' * 55}")
    print(f"  Profile: {name}")
    print(f"  Genre: {user_prefs['favorite_genre']}  |  "
          f"Mood: {user_prefs['favorite_mood']}  |  "
          f"Energy: {user_prefs['target_energy']}  |  "
          f"Acoustic: {user_prefs['likes_acoustic']}")
    print(f"{'=' * 55}")
    recommendations = recommend_songs(user_prefs, songs, k=k)
    for rank, (song, score, explanation) in enumerate(recommendations, 1):
        print(f"  {rank}. {song['title']} by {song['artist']}")
        print(f"     Score: {score:.2f}")
        print(f"     Reasons: {explanation}")
        print(f"  {'-' * 50}")


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # ── Standard profiles ────────────────────────────────
    profiles = {
        "Chill Lofi Listener": {
            "favorite_genre": "lofi",
            "favorite_mood": "chill",
            "target_energy": 0.4,
            "likes_acoustic": True,
        },
        "High-Energy Pop Fan": {
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.85,
            "likes_acoustic": False,
        },
        "Deep Intense Rock": {
            "favorite_genre": "rock",
            "favorite_mood": "intense",
            "target_energy": 0.9,
            "likes_acoustic": False,
        },
        # ── Adversarial / edge-case profiles ─────────────
        "Contradictory (High energy + sad mood)": {
            "favorite_genre": "pop",
            "favorite_mood": "sad",
            "target_energy": 0.9,
            "likes_acoustic": True,
        },
        "Ghost Genre (genre not in catalog)": {
            "favorite_genre": "reggaeton",
            "favorite_mood": "happy",
            "target_energy": 0.7,
            "likes_acoustic": False,
        },
    }

    for name, prefs in profiles.items():
        run_profile(name, prefs, songs)


if __name__ == "__main__":
    main()
