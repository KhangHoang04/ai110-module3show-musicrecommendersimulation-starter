# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder suggests 5 songs from a small catalog based on a user's preferred genre, mood, energy level, and whether they like acoustic music. It is designed for classroom exploration only, not for real users or production music platforms. It assumes each user has exactly one favorite genre and one favorite mood.

---

## 3. How the Model Works

The system looks at each song in the catalog and gives it a score based on how well it matches what the user says they like. It checks four things:

1. **Genre** - Does the song's genre match the user's favorite? If yes, it gets a big boost (+2 points).
2. **Mood** - Does the song's mood match what the user wants? If yes, +1 point.
3. **Energy** - How close is the song's energy level to the user's target? The closer it is, the more points it earns (up to +1 point).
4. **Acousticness** - If the user likes acoustic music and the song has high acousticness (above 0.6), it gets a small bonus (+0.5 points).

After every song gets a score, the system sorts them from highest to lowest and shows the top 5.

---

## 4. Data

The catalog contains **18 songs** stored in `data/songs.csv`. The original starter had 10 songs; 8 were added to cover more genres (classical, hip-hop, country, r&b, electronic, metal) and moods (sad, energetic, romantic, dreamy). Each song has numeric features for energy, tempo, valence, danceability, and acousticness on a 0.0 to 1.0 scale. The dataset is small and hand-curated, so it mostly reflects the taste of the person who built it. Genres like K-pop, Latin, or reggae are not represented at all.

---

## 5. Strengths

- **Chill Lofi Listener**: The top results (Midnight Coding, Library Rain, Focus Flow) all feel exactly right, matching on genre, mood, and energy. The system captured the "study music" vibe well.
- **High-Energy Pop Fan**: Sunrise City ranked first with a near-perfect score of 3.97. Gym Hero came second, which makes intuitive sense for an energetic pop listener.
- **Deep Intense Rock**: Storm Runner ranked first at 3.99. The system correctly identified the one rock song and placed intense-mood songs (Gym Hero, Iron Thunder) next.
- The scoring reasons are transparent. A user can see exactly why each song was recommended and how many points each factor contributed.

---

## 6. Limitations and Bias

The genre match bonus (+2.0) dominates the scoring. In the "Deep Intense Rock" test, Storm Runner scored 3.99 while the next-best song (Gym Hero) scored only 1.97 — nearly half. This means the system almost always recommends the user's genre first, regardless of how well other features match. With only one rock song in the catalog, a rock fan gets one strong recommendation and then unrelated songs to fill the remaining slots.

The "Contradictory" profile (pop genre, sad mood, high energy, likes acoustic) exposed a real weakness: the system recommended Gym Hero (an intense gym anthem) to someone who said they want sad music, simply because genre outweighed mood. A real listener asking for "sad pop" would not want Gym Hero.

The "Ghost Genre" profile (reggaeton) showed that when no songs match the user's genre, all scores are low (max 1.95) and the system falls back to energy matching alone, which produces random-feeling results.

Genre and mood use exact string matching with no partial credit. A user who likes "lofi" gets zero credit for "ambient" even though they are sonically similar.

The acousticness threshold of 0.6 is arbitrary — a song at 0.59 gets no bonus while 0.61 does.

---

## 7. Evaluation

Five user profiles were tested:

| Profile | Top Song | Score | Surprise? |
|---------|----------|-------|-----------|
| Chill Lofi Listener | Midnight Coding | 4.48 | No — perfect match |
| High-Energy Pop Fan | Sunrise City | 3.97 | No — expected |
| Deep Intense Rock | Storm Runner | 3.99 | No, but only 1 rock song in catalog |
| Contradictory (pop + sad + high energy) | Gym Hero | 2.97 | Yes — sad mood was ignored because genre dominated |
| Ghost Genre (reggaeton) | Backroad Summer | 1.95 | Yes — system fell back to energy-only scoring |

**Weight experiment**: Genre was halved (+1.0) and energy was doubled (x2.0). This made non-genre-matching songs climb in rank. For the Rock profile, Downtown Bounce (hip-hop) rose from 0.98 to 1.96 because its energy closely matched the target. The top song did not change for any profile, but the gaps narrowed, producing more diverse results.

Automated tests verified that the pop/happy song always outranks the lofi/chill song for a pop-preferring user, and that explanations are non-empty strings.

---

## 8. Future Work

- **Genre similarity**: Instead of binary match, use a distance metric (e.g., lofi is "close" to ambient) so related genres get partial credit.
- **Diversity penalty**: After picking the top song, penalize other songs in the same genre so the top 5 are not all from one style.
- **Multi-preference support**: Let users list multiple favorite genres or moods instead of exactly one.
- **Larger catalog**: 18 songs is too small. With hundreds of songs, the scoring differences would be more meaningful.

---

## 9. Personal Reflection

The biggest learning moment was seeing how a simple four-factor scoring formula can produce results that genuinely "feel" like recommendations. When the Chill Lofi profile got Midnight Coding and Library Rain at the top, it felt like something Spotify would suggest. That was surprising given how little math is involved — no machine learning, no neural networks, just addition and sorting.

One thing that was genuinely challenging was coming up with different user profiles to test. At first, the obvious ones came easily — a lofi listener, a pop fan, a rock fan. But after those three, I kept running into the problem that our scoring system only has four knobs to turn (genre, mood, energy, acoustic), so many profiles end up feeling similar. I had to think harder about what would actually stress the system, which is how I landed on the "Contradictory" and "Ghost Genre" profiles. It made me realize that designing good test cases is its own skill — you have to think about what could go wrong, not just what should go right.

Using AI tools helped speed up the boilerplate (CSV loading, output formatting), but I had to double-check the scoring math myself. The AI initially suggested a generic scoring approach, and I needed to manually verify that the weights produced the ranking I expected by tracing through specific songs by hand.

What surprised me most was the "Contradictory" profile. A user who wants sad pop at high energy should probably get songs like dramatic ballads, but the system recommended Gym Hero — an intense workout anthem — because genre (+2.0) completely overpowered mood (+1.0). This showed me that even "transparent" algorithms can produce results that feel wrong, and that weight tuning is a design decision with real consequences for users.

If I extended this project, I would add genre similarity scoring and a diversity mechanism so the top 5 results are not all from the same genre. I would also let users express how much they care about each factor (e.g., "genre matters a lot" vs. "I just want the right energy").
