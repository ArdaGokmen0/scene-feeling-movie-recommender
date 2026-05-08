# Scene-Based Movie Recommender

A portfolio-level Python/Streamlit movie recommender that recommends films from the feeling of a memorable scene, not only from genre or plot similarity.

## Main Idea

Most recommendation systems ask: "What movies are similar?"

This project instead explores: "What emotional patterns make scenes unforgettable?"

The goal is not only to match movies by genre or plot, but to infer the psychological attraction patterns behind memorable scenes. The app takes three favorite movies and an optional scene description, then looks for emotional and motif-based signals such as hidden genius, competence fantasy, dark mystery, betrayal, heartbreak, found family, wonder, freedom, and survival tension.

## Features

- Streamlit web app
- Three required favorite movie inputs
- Optional memorable scene input
- TMDB 5000 movies/credits dataset
- Baseline TF-IDF movie similarity
- Optional semantic similarity mode using `sentence-transformers`
- Lightweight scene motif analysis
- Small scene-based keyword bonus
- Experimental scene semantic similarity
- Turkish/noisy scene normalization for common vibe patterns
- Top 5 movie recommendations with concise reasons

## Tech Stack

- Python
- Streamlit
- pandas
- NumPy
- scikit-learn
- sentence-transformers
- TMDB 5000 Movies dataset

## How To Run Locally

Install dependencies:

```powershell
py -m pip install -r requirements.txt
```

Run the app:

```powershell
py -m streamlit run app.py
```

If `streamlit` is available directly on your PATH, this also works:

```powershell
streamlit run app.py
```

## Semantic Mode

The app starts in baseline TF-IDF mode by default. This keeps the MVP fast and reliable.

Use the sidebar toggle, `Use semantic similarity`, to enable experimental embedding-based movie similarity. Semantic mode loads the `all-MiniLM-L6-v2` model and compares movie metadata embeddings.

If semantic embeddings fail to load, the recommender falls back to the TF-IDF path.

## Turkish / Noisy Scene Normalization

The app includes a small pattern-based normalization layer for Turkish or noisy user inputs. It is not a full translation system. Instead, it recognizes common scene-vibe phrases and expands them into English canonical meanings for the existing analyzer and embedding pipeline.

Example:

```text
abi adam tek başına herkesi indiriyodu o vibe lazım
```

can be expanded toward:

```text
A lone protagonist fights many enemies alone. This suggests one-versus-many action, power fantasy, unstoppable protagonist energy, dominance, and competence fantasy.
```

## Example Inputs

Favorite movies:

```text
The Social Network
Sherlock Holmes
The Dark Knight
```

Scene examples:

```text
The calm moment where the villain secretly controls the entire room while everyone else thinks they are in charge.
```

```text
böyle zekasıyla ortamı susturan karakterler
```

```text
karanlık yağmurlu şehir dedektif hissi
```

```text
içimi parçalayan veda sahnesi
```

## Limitations

- The dataset is limited to the TMDB 5000 movie dataset.
- No TV series are included.
- Movie title matching currently works best with original English titles. Localized titles such as Turkish release names may not be recognized.
- Scene understanding is still rule-based and experimental.
- Turkish support is pattern-based, not full translation.
- Semantic mode can be slower on first load.
- Recommendations may still cluster around popular franchises.
- Emotional taxonomy coverage is improving but not complete.

## Future Work

- Cache movie embeddings to disk for faster startup.
- Expand balanced emotional taxonomy coverage.
- Build emotional pattern clustering across scenes and recommendations.
- Add multilingual canonicalization for Turkish and other natural/noisy inputs.
- Fine-tune scene embeddings for psychological attraction patterns.
- Move toward an emotional retrieval engine, not only metadata similarity.
- Explore community emotional perception mapping: if users describe their most memorable scenes, the system could gradually collect data about which psychological attraction patterns each film creates in real viewers. This emotional perception data does not exist in standard TMDB metadata.
- Add stronger support for romance, comfort, slice-of-life, nostalgia, comedy, moral dilemma, and identity/self-discovery.
- Improve Turkish normalization with more natural phrases.
- Add diversity controls to reduce franchise clustering.
- Improve recommendation explanations using scene-specific evidence.

## Project Structure

```text
Proje_4/
|-- app.py
|-- requirements.txt
|-- README.md
|-- .gitignore
|-- data/
|   |-- tmdb_5000_movies.csv
|   `-- tmdb_5000_credits.csv
`-- src/
    |-- data_loader.py
    |-- recommender.py
    |-- text_utils.py
    `-- language_utils.py
```
