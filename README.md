# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

### Real-World Recommendations vs. Our Simulation

Real-world platforms like Spotify and YouTube combine collaborative filtering (recommending what similar users enjoyed), content-based filtering (matching audio features like tempo and energy), and deep learning trained on billions of listening signals. Our simulation focuses on the content-based approach: we score each song by how well its attributes match a user's taste profile, keeping the system simple, transparent, and explainable.

### Song Features

Each `Song` uses: **genre**, **mood**, **energy** (0.0–1.0), **tempo_bpm**, **valence** (0.0–1.0), **danceability** (0.0–1.0), and **acousticness** (0.0–1.0), along with **id**, **title**, and **artist**.

### UserProfile Features

Each `UserProfile` stores: **favorite_genre**, **favorite_mood**, **target_energy** (0.0–1.0), and **likes_acoustic** (boolean).

### Algorithm Recipe

Each song is scored against the user profile using these factors:

| Factor | Condition | Points |
|--------|-----------|--------|
| Genre match | `song.genre == favorite_genre` | +2.0 |
| Mood match | `song.mood == favorite_mood` | +1.0 |
| Energy similarity | `1.0 - abs(song.energy - target_energy)` | +0.0 to +1.0 |
| Acousticness bonus | `likes_acoustic AND acousticness > 0.6` | +0.5 |

**Max score: 4.5 | Min score: 0.0**

Songs are sorted by descending score and the top *k* are returned.

### Recommendation Flow

```mermaid
flowchart TD
    A[User Profile] --> B[Load Song Catalog from CSV]
    B --> C[For each song in catalog]
    C --> D{Genre match?}
    D -- Yes --> E[+2.0 points]
    D -- No --> F[+0.0]
    E --> G{Mood match?}
    F --> G
    G -- Yes --> H[+1.0 points]
    G -- No --> I[+0.0]
    H --> J[Energy similarity: 1.0 - |song.energy - target_energy|]
    I --> J
    J --> K{likes_acoustic AND acousticness > 0.6?}
    K -- Yes --> L[+0.5 points]
    K -- No --> M[+0.0]
    L --> N[Sum = total score for song]
    M --> N
    N --> O{More songs?}
    O -- Yes --> C
    O -- No --> P[Sort songs by score descending]
    P --> Q[Return top K songs]
```

### A Note on Potential Biases

- **Genre dominance**: The genre match bonus (+2.0) outweighs all other factors combined (max +2.5 without genre). A song in the user's favorite genre will almost always rank above one that is not, regardless of mood, energy, or acousticness fit.
- **Binary matching**: Genre and mood use exact string matching with no partial credit. A user who likes "lofi" gets zero genre credit for "ambient" or "chill hop", even though those genres are closely related.
- **Small catalog bias**: With only 18 songs, some genres have just one representative. The system cannot distinguish between disliking a genre and simply not having good options in that genre.
- **Arbitrary acousticness threshold**: The 0.6 cutoff for the acoustic bonus is a hard boundary. A song with 0.59 acousticness gets no bonus while 0.61 does, despite being nearly identical.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

