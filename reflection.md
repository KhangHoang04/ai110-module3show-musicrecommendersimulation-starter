# Reflection: Profile Comparisons

## Chill Lofi vs. High-Energy Pop

The Chill Lofi listener got Midnight Coding (score 4.48) and Library Rain (score 4.45) at the top — both slow, low-energy, acoustic lofi tracks. The High-Energy Pop fan got Sunrise City (3.97) and Gym Hero (2.92) — bright, fast, danceable pop. The recommendations feel like two completely different playlists. The energy targets are almost opposite (0.4 vs. 0.85), so there is zero overlap in the top 5. This makes sense: the scoring formula rewards proximity to the target energy, and lofi songs cluster around 0.35–0.42 while pop songs sit at 0.82–0.93. The genre match bonus (+2.0) ensures they stay in separate lanes.

## High-Energy Pop vs. Deep Intense Rock

Both profiles want high energy (0.85 and 0.9), but different genres and moods. Gym Hero appears in both top 5 lists — ranked #2 for Pop (score 2.92, genre match but no mood match) and #2 for Rock (score 1.97, mood match but no genre match). This is because Gym Hero is pop/intense, so it gets partial credit from both profiles for different reasons. It shows how the system can surface the same song through different scoring paths. Storm Runner (rock, intense, 0.91 energy) only appears for the Rock profile because it needs that +2.0 genre bonus to rank high.

## Contradictory Profile vs. Chill Lofi

The Contradictory profile (pop, sad, energy 0.9, likes acoustic) is intentionally conflicting. Its top result is Gym Hero (score 2.97), which is a high-energy gym anthem — not sad at all. Meanwhile, Moonlight Sonata Remix (classical, sad, energy 0.25) only ranked #3 at 1.85 despite being the most "sad" song in the catalog. The problem is clear: genre (+2.0) dominates, so two pop songs rank above genuinely sad songs. In contrast, the Chill Lofi listener gets results that feel emotionally coherent because the lofi genre naturally aligns with chill mood and low energy. The Contradictory profile reveals that our system cannot handle users whose genre preference conflicts with their mood preference.

## Ghost Genre vs. Everyone Else

The Ghost Genre profile (reggaeton) gets no genre match for any song, so all scores are capped at 2.5 max (mood + energy + acoustic). Its top result is Backroad Summer at just 1.95, while every other profile's top result is above 3.9. This shows that the system degrades to near-random recommendations when a user's preferred genre is missing from the catalog. In a real product, this would be a serious problem — a reggaeton fan would see recommendations that feel unrelated to their taste. The fix would be either expanding the catalog or adding genre similarity so that "reggaeton" gets partial credit for "hip-hop" or "pop."

## Weight Experiment Observations

When genre was halved (+1.0) and energy was doubled (x2.0), the top songs stayed the same for all profiles, but the score gaps narrowed. For the Rock profile, the gap between #1 (Storm Runner, 3.98) and #2 (Gym Hero, 2.94) shrank from 2.02 down to 1.04. This means energy became a stronger "tiebreaker," letting songs from other genres compete more fairly. Downtown Bounce (hip-hop, energy 0.88) jumped from 0.98 to 1.96 for the Rock profile, showing that energy proximity alone can push a completely different genre into the top 5. The experiment showed that the original +2.0 genre weight creates a filter bubble, and reducing it allows for more diverse but potentially less genre-accurate recommendations.
