# Scene-Based Movie Recommender

A portfolio-level Python/Streamlit movie recommender that recommends films from the feeling of a memorable scene, not only from genre or plot similarity.

## Main Idea

Most recommendation systems ask: "What movies are similar?"

This project instead explores: "What emotional patterns make scenes unforgettable?"

The goal is not only to match movies by genre or plot, but to infer the psychological attraction patterns behind memorable scenes. The app takes three favorite movies and an optional scene description, then looks for emotional and motif-based signals such as hidden genius, competence fantasy, dark mystery, betrayal, heartbreak, found family, wonder, comfort, melancholy, romance tension, and subtle psychological tension.

## Features

- Streamlit web app
- Searchable dataset-based favorite movie selector
- Optional memorable scene input
- TMDB 5000 movies/credits dataset
- Baseline TF-IDF movie similarity
- Optional semantic similarity mode using `sentence-transformers`
- Lightweight scene motif analysis
- Small scene-based keyword bonus
- Experimental scene semantic similarity
- Turkish/noisy scene normalization for common vibe patterns
- Up to 5 visible movie recommendations with concise reasons
- "I've watched this film" replacement button for demo use

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
A lone-wolf protagonist enters a one-versus-many fight against many enemies. This suggests power fantasy, unstoppable protagonist energy, dominance, and competence fantasy.
```

## Example Inputs

The app asks you to choose exactly 3 movies from the dataset, then optionally describe a memorable scene or scene feeling.

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

```text
Böyle sakin geçen ama alttan alta rahatsız edici bir gerilim olan sahneleri seviyorum...
```

Expected interpretation for the last example includes psychological tension, subtle menace, controlled danger, slow-burn suspense, and silent intimidation.

## Final Demo Examples

### A. Lone Wolf / Power Fantasy

Selected movies:

```text
Spider-Man
Batman
The Dark Knight
```

Scene input:

```text
abi adam tek başına hepsinin arasına giriyodu kimse bişey yapamıyodu aşırı havalıydı böyle herkes korkuyodu ondan o vibe lazım
```

Expected patterns: lone wolf, power fantasy, competence fantasy, social dominance.

### B. Romance Tension

Selected movies:

```text
10 Things I Hate About You
Crazy, Stupid, Love.
The Proposal
```

Scene input:

```text
ya hani böyle birbirlerinden hoşlanıyolar ama sürekli laf sokuyolar falan sonra bi anda bi sahnede bakışıyolar ama ikisi de bişey diyemiyo aşırı iyi oluyo o gerilim
```

Expected patterns: romantic tension, unresolved attraction, emotional chemistry, slow burn intimacy, push-pull relationship, enemies-to-lovers.

### C. Wonder / Discovery

Selected movies:

```text
Harry Potter and the Philosopher's Stone
The Lord of the Rings: The Fellowship of the Ring
The Chronicles of Narnia: The Lion, the Witch and the Wardrobe
```

Scene input:

```text
o başka dünyayı ilk gördükleri sahne aşırı iyiydi ya böyle her şeyi keşfetmek istiyosun bi anda gerçekten oraya gitmek istedim resmen
```

Expected patterns: wonder, magical discovery, exploration curiosity, adventure wonder.

### D. Melancholy / Slice-of-Life

Selected movies:

```text
Lost in Translation
Eternal Sunshine of the Spotless Mind
Her
```

Scene input:

```text
I really like scenes where almost nothing is happening but the atmosphere feels emotionally heavy somehow. Usually rainy streets, quiet apartments, long pauses in conversations... that kind of lonely but strangely comforting feeling.
```

Expected patterns: loneliness, urban loneliness, peaceful solitude, reflective melancholy, comfort.

### E. Subtle Psychological Tension

Selected movies:

```text
Nightcrawler
Prisoners
Gone Girl
```

Scene input:

```text
Böyle sakin geçen ama alttan alta aşırı rahatsız edici bir gerilim olan sahneleri seviyorum. Özellikle karakterin dışarıdan tamamen kontrollü gözüküp aslında ne kadar tehlikeli olduğunu yavaş yavaş hissettirdiği anlar çok etkiliyor beni. Bağırış çağırış olmadan sadece bakışlarla gerilim kurulan sahneler aşırı iyi geliyor.
```

Expected patterns: psychological tension, subtle menace, controlled danger, slow-burn suspense, emotional unease, quiet dominance, silent intimidation.

## Limitations

- The dataset is limited to the TMDB 5000 movie dataset.
- No TV series are included.
- Movie selection comes from available dataset titles, so some desired films may not appear.
- Scene understanding is still rule-based and coverage is not complete.
- Turkish/noisy scene normalization is pattern-based, not full translation. It currently includes several emotional regions such as dominance, romance tension, wonder, comfort, melancholy, and subtle psychological tension.
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
- Add stronger support for nostalgia, comedy, moral dilemma, identity/self-discovery, and more subtle slice-of-life patterns.
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
test