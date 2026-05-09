def analyze_scene_text(scene_text: str) -> dict:
    """
    Analyze a user's memorable scene description with simple keyword rules.

    This is the first lightweight scene-based layer. It does not use AI or
    embeddings yet; it only looks for beginner-friendly motif signals.
    """
    text = scene_text.lower()

    # The result is grouped so the app can later explain different taste signals.
    result = {
        "motifs": [],
        "tone": [],
        "character_dynamics": [],
    }

    def add_tag(category, tag):
        if tag not in result[category]:
            result[category].append(tag)

    # Each tag has a small list of keywords that may suggest that motif.
    motif_rules = {
        "hidden genius": ["hidden genius", "secret genius", "genius", "prodigy", "unexpected talent"],
        "intelligence": ["smart", "intelligent", "clever", "brilliant", "strategy", "deduce", "memory"],
        "competence fantasy": [
            "impress", "master", "expert", "skill", "talent", "perfectly",
            "outsmart", "mastermind", "scheme", "strategist"
        ],
        "revenge": ["revenge", "payback", "avenge", "vengeance", "retaliation"],
        "betrayal": [
            "betray", "betrayed", "betrayal", "traitor", "backstab",
            "deceived", "deception", "corrupt", "trust collapses",
            "turns against"
        ],
        "heartbreak": ["heartbreak", "emotional separation", "separation", "sadness"],
        "comfort": ["comforting", "comfort", "emotionally supports", "protects", "safe"],
        "crime": ["criminal mastermind", "crime", "criminal", "villain", "heist", "robbery", "mafia", "gangster", "murder"],
        "mystery": [
            "mystery", "dangerous mystery", "clue", "detective", "investigate",
            "investigation", "case", "secret", "twist", "puzzle", "uncovering"
        ],
        "romance": ["love", "romance", "romantic", "kiss", "relationship", "heartbreak"],
        "romantic tension": ["romantic tension", "teasing", "flirt", "flirting"],
        "unresolved attraction": ["unresolved attraction", "hide emotional attraction", "hidden attraction"],
        "emotional chemistry": ["emotional chemistry", "chemistry", "attraction"],
        "slow burn intimacy": ["slow burn intimacy", "slow burn", "intimacy"],
        "emotional hesitation": ["emotional hesitation", "hesitation", "cannot say anything"],
        "vulnerability": ["vulnerability", "vulnerable", "emotionally exposed"],
        "loneliness": ["lonely", "isolated", "empty", "abandoned", "emotional emptiness"],
        "lone wolf": ["lone-wolf", "one-versus-many", "one versus many", "many enemies", "unstoppable protagonist"],
        "wonder": ["magical discovery", "awe", "wonder", "curiosity", "childlike excitement", "magical"],
        "freedom": ["liberation", "escapes", "escape", "oppressive", "freedom"],
        "psychological tension": ["tense", "pressure", "paranoia", "mind game", "psychological", "anxiety"],
        "underdog": [
            "underdog", "underestimated", "nobody believed", "proves everyone wrong",
            "prove everyone wrong", "prove them wrong", "trains", "training",
            "final competition", "tournament", "champion"
        ],
        "power fantasy": [
            "powerful", "unstoppable", "dominates", "control", "controls",
            "manipulate", "manipulates", "manipulation", "influence", "fearless"
        ],
    }

    tone_rules = {
        "dark atmosphere": [
            "dark", "gloomy", "bleak", "night", "violent", "disturbing",
            "lonely", "city", "noir", "dangerous", "shadow", "grim"
        ],
        "emotional": ["cry", "sad", "emotional", "sacrifice", "loss", "grief"],
        "bittersweet": ["heartbreak", "sadness", "emotional separation", "emotional release"],
        "suspenseful": ["suspense", "suspenseful", "tense", "waiting", "danger", "escape", "slowly uncovering"],
        "inspiring": ["inspiring", "hope", "triumph", "victory", "overcome"],
    }

    character_rules = {
        "social dominance": [
            "dominates", "humiliates", "shocks everyone", "proves", "impresses",
            "commands respect", "manipulate", "manipulates", "manipulation",
            "control", "controls", "behind the scenes", "mastermind", "scheme",
            "puppet", "influence"
        ],
        "loyalty": [
            "trust", "trusting", "loyalty", "loyal", "bond", "friendship",
            "cooperate", "together", "allies", "team", "protect"
        ],
        "found family": ["found-family", "found family", "loyal friends", "belonging", "stay together", "support each other"],
        "mentor relationship": ["mentor", "teacher", "student", "guide", "training"],
        "rivalry": [
            "enemy", "enemies", "rival", "rivalry", "opponent",
            "forced to work together", "team up", "alliance", "competition",
            "challenge", "face off"
        ],
        "push-pull relationship": ["push-pull", "push-pull relationship", "teasing", "emotional hesitation"],
        "enemies-to-lovers": ["enemies-to-lovers", "enemies to lovers", "teasing", "hidden attraction"],
    }

    # Check whether any keyword appears in the scene text.
    for tag, keywords in motif_rules.items():
        if any(keyword in text for keyword in keywords):
            add_tag("motifs", tag)

    for tag, keywords in tone_rules.items():
        if any(keyword in text for keyword in keywords):
            add_tag("tone", tag)

    for tag, keywords in character_rules.items():
        if any(keyword in text for keyword in keywords):
            add_tag("character_dynamics", tag)

    # Manipulation/control scenes often imply both competence and dominance.
    manipulation_keywords = [
        "manipulate", "manipulates", "manipulation", "control", "controls",
        "behind the scenes", "mastermind", "scheme", "puppet", "influence"
    ]
    if any(keyword in text for keyword in manipulation_keywords):
        add_tag("motifs", "competence fantasy")
        add_tag("motifs", "power fantasy")
        add_tag("character_dynamics", "social dominance")

    # One-versus-many action is a power signal, not melancholic loneliness.
    one_vs_many_keywords = [
        "lone-wolf", "one-versus-many", "one versus many", "many enemies",
        "unstoppable protagonist", "fight against many"
    ]
    if any(keyword in text for keyword in one_vs_many_keywords):
        add_tag("motifs", "lone wolf")
        add_tag("motifs", "power fantasy")
        add_tag("motifs", "competence fantasy")
        add_tag("character_dynamics", "social dominance")

    # Dark investigations should connect mystery with suspense, not only crime.
    dark_mystery_keywords = ["slowly uncovering", "uncovering", "dangerous mystery"]
    if any(keyword in text for keyword in dark_mystery_keywords):
        add_tag("motifs", "mystery")
        add_tag("tone", "suspenseful")
        add_tag("tone", "psychological tension")

    # Underdog competition scenes usually include skill growth as well.
    underdog_growth_keywords = [
        "proves everyone wrong", "prove everyone wrong", "trains",
        "training", "final competition", "tournament", "champion"
    ]
    if any(keyword in text for keyword in underdog_growth_keywords):
        add_tag("motifs", "underdog")
        add_tag("motifs", "competence fantasy")

    return result
