import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class MovieRecommender:
    def __init__(self, df, use_embeddings=False):
        self.df = df.reset_index(drop=True)
        self.use_embeddings = use_embeddings
        self.embedding_available = False
        self.movie_embeddings = None

        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            max_features=8000,
            ngram_range=(1, 2)
        )

        self.tfidf_matrix = self.vectorizer.fit_transform(self.df["content"])

        if self.use_embeddings:
            try:
                from sentence_transformers import SentenceTransformer

                self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
                self.movie_embeddings = self.embedding_model.encode(
                    self.df["content"].tolist(),
                    show_progress_bar=False
                )
                self.embedding_available = True
            except Exception:
                self.embedding_available = False
                self.movie_embeddings = None

    def find_movie_index(self, title):
        title_clean = title.lower().strip()

        exact_matches = self.df[self.df["title_clean"] == title_clean]

        if len(exact_matches) > 0:
            return exact_matches.index[0]

        partial_matches = self.df[self.df["title_clean"].str.contains(title_clean, na=False)]

        if len(partial_matches) > 0:
            return partial_matches.index[0]

        return None

    def calculate_scene_bonus(self, movie_row, scene_analysis):
        if not scene_analysis or not any(scene_analysis.values()):
            return 0.0

        movie_text = " ".join([
            str(movie_row.get("overview", "")),
            str(movie_row.get("genres_text", "")),
            str(movie_row.get("keywords_text", "")),
        ]).lower()

        tag_keywords = {
            "hidden genius": ["hidden", "secret", "underestimated", "quiet", "prodigy", "genius"],
            "intelligence": ["detective", "deduction", "hacker", "scientist", "strategist", "brilliant", "intellectual"],
            "social dominance": [
                "dominates", "control", "manipulate", "manipulates", "manipulation",
                "authority", "powerful", "influence", "scheme", "schemes",
                "behind the scenes", "puppet", "corrupt"
            ],
            "competence fantasy": [
                "master", "mastermind", "expert", "skill", "ability", "outsmart",
                "genius", "talent", "strategist", "scheme", "schemes"
            ],
            "revenge": ["revenge", "vengeance", "payback", "avenge"],
            "heartbreak": [
                "heartbreak", "separation", "breakup", "goodbye", "farewell",
                "sadness", "painful", "emotional loss"
            ],
            "comfort": [
                "comfort", "supports", "protect", "protects", "emotional support",
                "safety", "safe", "care", "caring", "healing"
            ],
            "betrayal": [
                "betrayal", "traitor", "deception", "deceive", "secret",
                "manipulate", "manipulation", "corrupt", "betray", "betrayed",
                "deceived", "trust", "turns against", "backstab"
            ],
            "crime": [
                "criminal", "mastermind", "crime", "crimes", "conspiracy", "villain",
                "underworld", "mob", "mafia", "gang", "heist", "robbery", "detective",
                "investigation", "murder"
            ],
            "mystery": [
                "detective", "mystery", "investigation", "uncover", "uncovering",
                "clue", "clues", "murder", "case", "suspect", "crime", "secret"
            ],
            "romance": ["love", "romance", "relationship", "romantic"],
            "loneliness": ["alone", "lonely", "isolation", "isolated"],
            "wonder": [
                "magic", "magical", "fantasy", "discovery", "discover",
                "wonder", "awe", "extraordinary", "adventure", "curiosity"
            ],
            "freedom": [
                "escape", "escapes", "escaped", "freedom", "liberation",
                "free", "oppression", "oppressive", "prison", "trapped"
            ],
            "dark atmosphere": [
                "dark", "noir", "grim", "dangerous", "shadow", "city", "night",
                "bleak", "violent", "sinister", "crime", "murder", "danger"
            ],
            "psychological tension": ["psychological", "mind", "tension", "paranoia", "thriller"],
            "underdog": [
                "underdog", "unlikely", "outsider", "underestimated", "overlooked",
                "weak", "poor", "struggling", "proves", "prove", "against the odds",
                "champion", "competition", "tournament", "contest", "trains",
                "training", "fight", "fighter", "final", "championship", "win",
                "victory", "challenge"
            ],
            "power fantasy": ["powerful", "hero", "unstoppable", "control", "revenge"],
            "emotional": ["emotional", "loss", "grief", "sacrifice", "family"],
            "suspenseful": ["suspense", "thriller", "danger", "escape", "survival"],
            "inspiring": ["inspiring", "hope", "victory", "dream", "overcome"],
            "loyalty": [
                "trust", "trusting", "loyalty", "loyal", "friendship", "bond",
                "partnership", "together", "cooperate", "cooperation", "allies",
                "alliance", "friend", "team", "protect"
            ],
            "found family": [
                "friendship", "friends", "family", "belonging", "loyal",
                "loyalty", "team", "together", "support"
            ],
            "mentor relationship": ["mentor", "teacher", "training", "student"],
            "rivalry": [
                "rival", "rivalry", "enemy", "enemies", "opponent", "opposing",
                "compete", "competition", "conflict", "forced together", "team up",
                "partnership", "alliance", "challenge", "contest", "tournament"
            ],
        }

        detected_tags = []
        for tags in scene_analysis.values():
            detected_tags.extend(tags)

        if not detected_tags:
            return 0.0

        matched_tags = 0

        for tag in detected_tags:
            keywords = tag_keywords.get(tag, [tag])
            keyword_matches = sum(1 for keyword in keywords if keyword in movie_text)

            # Require at least two related signals so broad words do not over-reward a movie.
            if keyword_matches >= 2:
                matched_tags += 1

        return matched_tags / len(detected_tags)

    def recommend_from_favorites(self, favorite_titles, top_n=5, scene_analysis=None, scene_text=None):
        favorite_indices = []

        for title in favorite_titles:
            idx = self.find_movie_index(title)
            if idx is not None:
                favorite_indices.append(idx)

        if len(favorite_indices) == 0:
            return [], []

        if self.use_embeddings and self.embedding_available:
            # Average semantic profile from the selected favorite movies.
            user_profile = np.asarray(
                self.movie_embeddings[favorite_indices].mean(axis=0)
            ).reshape(1, -1)
            similarities = cosine_similarity(user_profile, self.movie_embeddings).flatten()
        else:
            # Default path: keep the original TF-IDF recommendation behavior.
            user_profile = np.asarray(
                self.tfidf_matrix[favorite_indices].mean(axis=0)
            )
            similarities = cosine_similarity(user_profile, self.tfidf_matrix).flatten()


        # Exclude input movies
        for idx in favorite_indices:
            similarities[idx] = -1

        # Add light quality/popularity weighting
        rating_score = self.df["vote_average"].fillna(0).to_numpy() / 10
        popularity_score = self.df["popularity"].fillna(0).to_numpy()

        if popularity_score.max() > 0:
            popularity_score = popularity_score / popularity_score.max()

        old_final_score = (
            0.80 * similarities +
            0.10 * rating_score +
            0.10 * popularity_score
        )

        scene_bonus = np.zeros(len(self.df))

        if scene_analysis and any(scene_analysis.values()):
            scene_bonus = self.df.apply(
                lambda row: self.calculate_scene_bonus(row, scene_analysis),
                axis=1
            ).to_numpy()

        scene_semantic_similarity = np.zeros(len(self.df))

        if self.use_embeddings and self.embedding_available and scene_text and scene_text.strip():
            scene_embedding = self.embedding_model.encode([scene_text], show_progress_bar=False)
            scene_semantic_similarity = cosine_similarity(
                scene_embedding,
                self.movie_embeddings
            ).flatten()

        # Scene bonus is intentionally small: it can nudge results, not overpower TF-IDF similarity.
        # Scene semantic weight is tiny because this signal is still experimental.
        final_score = old_final_score + (0.05 * scene_bonus) + (0.02 * scene_semantic_similarity)

        candidate_count = min(len(self.df), top_n * 3)
        top_indices = np.argsort(final_score)[::-1][:candidate_count]

        recommendations = self.df.iloc[top_indices].copy()
        recommendations["similarity_score"] = similarities[top_indices]
        recommendations["scene_bonus"] = scene_bonus[top_indices]
        recommendations["scene_semantic_similarity"] = scene_semantic_similarity[top_indices]
        recommendations["final_score"] = final_score[top_indices]

        if "year" in recommendations.columns:
            recommendations = recommendations.drop_duplicates(
                subset=["title", "year"],
                keep="first"
            )
        else:
            recommendations = recommendations.drop_duplicates(
                subset=["title"],
                keep="first"
            )

        recommendations = recommendations.head(top_n)

        matched_movies = self.df.iloc[favorite_indices]["title"].tolist()

        return recommendations, matched_movies

    def generate_baseline_reason(self, movie_row, favorite_titles):
        genres = ", ".join(movie_row["genre_list"][:3])

        reasons = []

        if genres:
            reasons.append(f"Similar genre/mood signals: {genres}.")

        if movie_row["overview"]:
            reasons.append("Its story description shares thematic similarity with your selected movies.")

        return reasons[:2]
