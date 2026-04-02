# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder suggests 5 songs from a small catalog based on a user's preferred genre, mood, energy level, and optional advanced preferences like decade, mood tags, and instrumentalness. It is designed for classroom exploration only, not for real users or production music platforms. It assumes each user has one favorite genre and one favorite mood, with optional secondary preferences.

**Not intended for**: real product deployment, personalization at scale, or any context where users depend on accurate, unbiased recommendations.

---

## 3. How the Model Works

The system looks at each song in the catalog and gives it a score based on how well it matches what the user says they like. It checks up to nine things:

1. **Genre** — Does the song's genre match the user's favorite? If yes, it gets a big boost (+2 points in balanced mode).
2. **Mood** — Does the song's mood match what the user wants? If yes, +1 point.
3. **Energy** — How close is the song's energy level to the user's target? The closer it is, the more points it earns (up to +1 point).
4. **Acousticness** — If the user likes acoustic music and the song has high acousticness (above 0.6), it gets a small bonus (+0.5 points).
5. **Popularity** — More popular songs get a small bonus, scaled from 0 to +0.3.
6. **Decade** — If the song's release decade matches the user's preferred era, +0.5 points.
7. **Mood tag** — If the song's detailed mood tag (e.g., "nostalgic", "euphoric") matches one of the user's preferred tags, +0.5 points.
8. **Instrumentalness** — If the user likes instrumental music and the song is mostly instrumental, +0.3 points.
9. **Language** — If the song's language matches the user's preference, +0.2 points.

After every song gets a score, the system sorts them from highest to lowest. If diversity mode is enabled, the system penalizes songs that share an artist or genre with songs already picked, so the top 5 are more varied. The user can also switch between four scoring modes (balanced, genre-first, mood-first, energy-focused) that change how much each factor matters.

---

## 4. Data

The catalog contains **18 songs** stored in `data/songs.csv`. The original starter had 10 songs; 8 were added to cover more genres (classical, hip-hop, country, r&b, electronic, metal) and moods (sad, energetic, romantic, dreamy).

Each song has **15 attributes**: id, title, artist, genre, mood, energy, tempo_bpm, valence, danceability, acousticness, popularity, release_decade, mood_tag, lyrics_language, and instrumentalness.

Genres represented: pop, lofi, rock, ambient, jazz, synthwave, indie pop, classical, hip-hop, country, r&b, electronic, metal.

The dataset is small and hand-curated, so it mostly reflects the taste of the person who built it. Genres like K-pop, Latin, or reggae are not represented at all. Most songs are English-language, with only one German-language track.

---

## 5. Strengths

- **Chill Lofi Listener**: The top results (Midnight Coding at 6.11, Library Rain at 5.56) matched on genre, mood, energy, decade, mood tags, instrumentalness, and acousticness. The system captured the "study music" vibe well.
- **High-Energy Pop Fan**: Sunrise City ranked first (5.42) with mood tag "euphoric" contributing to the score. Gym Hero came second with a diversity genre-repeat penalty applied, which makes intuitive sense.
- **Deep Intense Rock**: Storm Runner ranked first (5.39) with aggressive mood tag matching. The system correctly identified the one rock song and placed intense-mood songs next.
- **Transparency**: Every recommendation includes a full breakdown of why each song was chosen and how many points each factor contributed. A user can see exactly what the system valued.
- **Scoring modes**: Users can switch strategies without changing code. Mood-first mode promoted Spacewalk Thoughts (ambient/chill) into the top 3 for the lofi profile, showing the mode system works as designed.

---

## 6. Limitations and Bias

The genre match bonus (+2.0 in balanced mode) dominates the scoring. In the "Deep Intense Rock" test, Storm Runner scored 5.39 while the next-best song (Iron Thunder) scored only 2.79. This means the system almost always recommends the user's genre first, regardless of how well other features match.

The "Contradictory" profile (pop genre, sad mood, high energy) exposed a real weakness: the system recommended Gym Hero (an intense gym anthem) to someone who said they want sad music, simply because genre outweighed mood.

The "Ghost Genre" profile (reggaeton) showed that when no songs match the user's genre, the max score dropped to 3.33 and the system fell back to mood + energy + tag scoring, producing less confident results.

Genre and mood use exact string matching with no partial credit. A user who likes "lofi" gets zero credit for "ambient" even though they are sonically similar. The acousticness threshold of 0.6 is arbitrary.

**Popularity reinforcement**: Every song always receives some popularity points, which could reinforce mainstream bias — popular songs get recommended more, which could make them more popular in a real system.

**Diversity penalty helps but is imperfect**: The artist repeat (-1.0) and genre repeat (-0.5) penalties prevent the worst "filter bubbles" — for example, Focus Flow by LoRoom dropped from 5.11 to 3.61 when diversity was enabled because LoRoom was already selected. However, the penalty values are arbitrary and may over-correct in some cases, pushing genuinely good matches too far down the list.

---

## 7. Evaluation

Five user profiles were tested across four scoring modes with diversity on and off:

| Profile | Top Song (balanced, diversity ON) | Score | Surprise? |
|---------|-----------------------------------|-------|-----------|
| Chill Lofi Listener | Midnight Coding | 6.11 | No — perfect match on all factors |
| High-Energy Pop Fan | Sunrise City | 5.42 | No — expected |
| Deep Intense Rock | Storm Runner | 5.39 | No, but only 1 rock song in catalog |
| Contradictory (pop + sad) | Gym Hero | 4.44 | Yes — sad mood was ignored because genre dominated |
| Ghost Genre (reggaeton) | Rooftop Lights | 3.33 | Yes — no genre matches, fell back to mood + tags |

**Scoring mode test**: For the Chill Lofi profile, mood-first mode promoted Spacewalk Thoughts (ambient/chill) into the top 3, replacing Focus Flow which lacks a mood match. This confirmed that the mode system changes ranking behavior as intended.

**Diversity test**: With diversity OFF, LoRoom appeared twice in the top 3 and lofi dominated all top 3 slots. With diversity ON, Focus Flow dropped from 5.11 to 3.61 (artist -1.0 and genre -0.5 penalties), letting other genres have a better chance.

**Weight experiment**: Genre was halved (+1.0) and energy was doubled (x2.0). The top song stayed the same for all profiles, but score gaps narrowed. For the Rock profile, Downtown Bounce (hip-hop) rose from a low score to 1.96 purely on energy proximity, showing that energy weighting alone can push unrelated genres into the top 5.

Automated tests verified that the pop/happy song always outranks the lofi/chill song for a pop-preferring user, and that explanations are non-empty strings.

---

## 8. Future Work

- **Genre similarity**: Instead of binary match, use a distance metric (e.g., lofi is "close" to ambient) so related genres get partial credit.
- **Multi-preference support**: Let users list multiple favorite genres or moods instead of exactly one.
- **Larger catalog**: 18 songs is too small. With hundreds of songs, the scoring differences would be more meaningful and the diversity penalty would have more room to work.
- **Tunable diversity**: Let users control the strength of the diversity penalty instead of using fixed -1.0 and -0.5 values.
- **Collaborative filtering**: Add a second signal based on what similar users liked, not just feature matching.

---

## 9. Personal Reflection

The biggest learning moment was seeing how a simple nine-factor scoring formula can produce results that genuinely "feel" like recommendations. When the Chill Lofi profile got Midnight Coding and Library Rain at the top, it felt like something Spotify would suggest. That was surprising given how little math is involved — no machine learning, no neural networks, just addition and sorting.

One thing that was genuinely challenging was coming up with different user profiles to test. At first, the obvious ones came easily — a lofi listener, a pop fan, a rock fan. But after those three, I kept running into the problem that our scoring system only has a few knobs to turn, so many profiles end up feeling similar. I had to think harder about what would actually stress the system, which is how I landed on the "Contradictory" and "Ghost Genre" profiles. It made me realize that designing good test cases is its own skill — you have to think about what could go wrong, not just what should go right.

Using AI tools helped speed up the boilerplate (CSV loading, output formatting, tabulate integration), but I had to double-check the scoring math myself. The AI initially suggested a generic scoring approach, and I needed to manually verify that the weights produced the ranking I expected by tracing through specific songs by hand.

What surprised me most was the "Contradictory" profile. A user who wants sad pop at high energy should probably get songs like dramatic ballads, but the system recommended Gym Hero — an intense workout anthem — because genre (+2.0) completely overpowered mood (+1.0). This showed me that even "transparent" algorithms can produce results that feel wrong, and that weight tuning is a design decision with real consequences for users.

If I extended this project, I would add genre similarity scoring so related genres get partial credit, and let users control how much they care about each factor directly.
