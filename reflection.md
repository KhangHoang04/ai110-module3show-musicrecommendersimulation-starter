# Reflection: Profile Comparisons

## Chill Lofi vs. High-Energy Pop

The Chill Lofi listener got Midnight Coding (score 6.11) and Library Rain (score 5.56) at the top — both slow, low-energy, acoustic lofi tracks that also hit on decade match, nostalgic mood tag, and instrumental bonus. The High-Energy Pop fan got Sunrise City (5.42) and Gym Hero (3.89) — bright, fast, danceable pop with euphoric mood tags. The recommendations feel like two completely different playlists. The energy targets are almost opposite (0.4 vs. 0.85), so there is zero overlap in the top 5. This makes sense: the scoring formula rewards proximity to the target energy, and lofi songs cluster around 0.35–0.42 while pop songs sit at 0.82–0.93. The genre match bonus (+2.0) ensures they stay in separate lanes, and the new mood tag matching reinforces the split — "nostalgic" and "euphoric" pull toward very different songs.

## High-Energy Pop vs. Deep Intense Rock

Both profiles want high energy (0.85 and 0.9), but different genres and moods. Gym Hero appears in both top 5 lists — ranked #2 for Pop (score 3.89, genre match + euphoric tag) and #3 for Rock (score 2.44, mood match but no genre match). This is because Gym Hero is pop/intense with a euphoric mood tag, so it gets partial credit from both profiles for different reasons. It shows how the system can surface the same song through different scoring paths. Storm Runner (rock, intense, 0.91 energy) only appears for the Rock profile because it needs that +2.0 genre bonus plus the aggressive mood tag to rank high. The advanced features (mood tags, decade) helped differentiate the two profiles more than the original 4-factor system did.

## Contradictory Profile vs. Chill Lofi

The Contradictory profile (pop, sad, energy 0.9, likes acoustic, tags: melancholy + euphoric) is intentionally conflicting. Its top result is Gym Hero (score 4.44), which is a high-energy gym anthem — not sad at all. Meanwhile, Late Night Letters (indie pop, sad, melancholy tag) only ranked #3 at 2.89 and Moonlight Sonata Remix (classical, sad, melancholy) ranked #4 at 2.49 despite being the most "sad" songs in the catalog. The problem is clear: genre (+2.0) plus the euphoric mood tag bonus pushes pop songs above genuinely sad songs. In contrast, the Chill Lofi listener gets results that feel emotionally coherent because the lofi genre naturally aligns with chill mood, low energy, nostalgic tags, and high instrumentalness. The Contradictory profile reveals that our system cannot handle users whose genre preference conflicts with their mood preference.

## Ghost Genre vs. Everyone Else

The Ghost Genre profile (reggaeton) gets no genre match for any song, so it misses the biggest scoring factor entirely. Its top result is Rooftop Lights at 3.33 (mood match + energy proximity + uplifting tag + decade match), while every other profile's top result is above 4.4. This shows that the system degrades to mood + energy + tag scoring when a user's preferred genre is missing from the catalog. In a real product, this would be a serious problem — a reggaeton fan would see recommendations that feel unrelated to their taste. The new features (mood tags, decade) helped slightly by giving more factors to differentiate songs, but the gap is still large. The fix would be either expanding the catalog or adding genre similarity so that "reggaeton" gets partial credit for "hip-hop" or "pop."

## Weight Experiment Observations

When genre was halved (+1.0) and energy was doubled (x2.0), the top songs stayed the same for all profiles, but the score gaps narrowed. For the Rock profile, the gap between #1 (Storm Runner) and #2 (Gym Hero) shrank significantly. This means energy became a stronger "tiebreaker," letting songs from other genres compete more fairly. Downtown Bounce (hip-hop, energy 0.88) jumped up for the Rock profile purely on energy proximity, showing that energy weighting alone can push a completely different genre into the top 5. The experiment showed that the original +2.0 genre weight creates a filter bubble, and reducing it allows for more diverse but potentially less genre-accurate recommendations.

## Scoring Mode Observations

The mode comparison was one of the most interesting experiments. For the Chill Lofi profile:

- **balanced** and **genre-first** produced the same top 3 (Midnight Coding, Library Rain, Focus Flow) — all lofi songs. Genre dominates in both.
- **mood-first** promoted Spacewalk Thoughts (ambient/chill) into the top 3, replacing Focus Flow. This makes sense because Spacewalk Thoughts has a "chill" mood match (+3.0 in mood-first mode) while Focus Flow's mood is "focused" which does not match. Tripling the mood weight made mood more important than genre for the first time.
- **energy-focused** kept the same top 3 as balanced but with narrower score gaps, because energy similarity (up to +3.0) nearly matched genre (+0.5) in importance.

This showed that the mode system actually works — different strategies produce meaningfully different rankings, not just different numbers.

## Diversity Penalty Observations

The diversity demo was the clearest illustration of the penalty system. Without diversity, LoRoom appeared twice in the top 3 (Midnight Coding at #1 and Focus Flow at #3), and all three top songs were lofi. With diversity ON, Focus Flow dropped from 5.11 to 3.61 because it received both an artist repeat penalty (-1.0 for LoRoom appearing again) and a genre repeat penalty (-0.50 for lofi appearing again). This pushed it closer to Spacewalk Thoughts (3.46) which had no penalties. The diversity penalty did not change the #1 or #4 songs, but it narrowed the gaps between #2–5, giving non-lofi songs a better chance of surfacing. This is exactly the kind of "filter bubble" prevention that real recommenders need.
