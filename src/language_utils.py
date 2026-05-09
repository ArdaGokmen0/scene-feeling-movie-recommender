def normalize_scene_text(scene_text: str) -> str:
    """
    Expand simple Turkish/noisy scene descriptions into an English scene meaning.

    This is not full translation. It only catches common Turkish vibe patterns
    and adds an English canonical description for the existing pipeline.
    """
    text = scene_text.lower()

    pattern_groups = [
        {
            "signals": [
                "tek başına", "tek basina", "herkese karşı", "herkese karsi",
                "10 kişiye", "10 kisiye", "dalıyordu", "daliyordu",
                "dalıyodu", "daliyodu", "dövüşüyordu", "dovusuyordu",
                "indiriyordu", "indiriyodu"
            ],
            "meaning": (
                "A lone-wolf protagonist enters a one-versus-many fight against "
                "many enemies. This suggests power fantasy, unstoppable protagonist "
                "energy, dominance, and competence fantasy."
            ),
        },
        {
            "signals": [
                "zekasıyla", "zekasiyla", "ortamı susturdu", "ortami susturdu",
                "ortamı susturan", "ortami susturan", "herkesi şaşırttı",
                "herkesi sasirtti", "akıl oyunları", "akil oyunlari"
            ],
            "meaning": (
                "A quiet intelligent character dominates the room through "
                "intelligence. This suggests hidden genius, intelligence "
                "dominance, competence fantasy, and social dominance."
            ),
        },
        {
            "signals": [
                "karanlık", "karanlik", "yağmurlu", "yagmurlu",
                "dedektif", "şehir", "sehir"
            ],
            "meaning": (
                "A detective moves through a dark rainy city atmosphere. This "
                "suggests dark atmosphere, mystery, detective tension, noir mood, "
                "and suspense."
            ),
        },
        {
            "signals": ["intikam", "geri döndü", "geri dondu", "hesaplaşma", "hesaplasma"],
            "meaning": (
                "A character returns for revenge and a final confrontation. This "
                "suggests revenge, comeback, cold determination, and emotional "
                "intensity."
            ),
        },
        {
            "signals": [
                "ölüm kalım", "olum kalim", "oyun", "kapana kısılmış",
                "kapana kisilmis", "hayatta kalma"
            ],
            "meaning": (
                "A person is trapped in a dangerous survival game. This suggests "
                "survival tension, danger, trapped feeling, thriller atmosphere, "
                "and psychological tension."
            ),
        },
        {
            "signals": [
                "manipülatif", "manipulatif", "herkesi kontrol ediyor",
                "sakin kötü karakter", "sakin kotu karakter"
            ],
            "meaning": (
                "A calm manipulative villain secretly controls people around him. "
                "This suggests mastermind, manipulation, social dominance, power "
                "fantasy, and psychological control."
            ),
        },
        {
            "signals": [
                "ezildi", "kaybetti", "kaybediyo", "tekrar ayağa kalktı",
                "tekrar ayaga kalkti", "ayağa kalkıyo", "ayaga kalkiyo",
                "pes etmedi"
            ],
            "meaning": (
                "A defeated character refuses to give up and stands back up again. "
                "This suggests underdog resilience, comeback, motivation, "
                "emotional strength, and competence fantasy."
            ),
        },
        {
            "signals": [
                "arkadaş grubu", "arkadas grubu", "kontrolden çıktı",
                "kontrolden cikti", "kontrolden çıkan", "kontrolden cikan",
                "olaylar büyüdü", "olaylar buyudu"
            ],
            "meaning": (
                "A group of friends enters a chaotic situation that grows out of "
                "control. This suggests group chaos, danger escalation, thriller "
                "tension, and loss of control."
            ),
        },
        {
            "signals": [
                "terk edildiği sahne", "terk edildigi sahne",
                "içimi parçalayan veda", "icimi parcalayan veda",
                "ayrılık", "ayrilik", "veda"
            ],
            "meaning": (
                "A painful heartbreak scene where emotional separation creates "
                "sadness, vulnerability, and emotional release."
            ),
        },
        {
            "signals": [
                "ağlarken onu sakinleştirdi", "aglarken onu sakinlestirdi",
                "yanında güvende hissettirdi", "yaninda guvende hissettirdi"
            ],
            "meaning": (
                "A comforting scene where one character emotionally supports and "
                "protects another person."
            ),
        },
        {
            "signals": [
                "arkadaşları onu yalnız bırakmadı", "arkadaslari onu yalniz birakmadi",
                "ekip zamanla aile gibi oldu", "herkes giderken onlar yanında kaldı",
                "herkes giderken onlar yaninda kaldi", "yanında kaldılar",
                "yaninda kaldilar"
            ],
            "meaning": (
                "A found-family scene where loyal friends stay together, support "
                "each other, and create a feeling of belonging."
            ),
        },
        {
            "signals": [
                "ilk kez büyülü dünyayı gördü", "ilk kez buyulu dunyayi gordu",
                "büyülü dünya", "buyulu dunya", "keşif hissi", "kesif hissi",
                "çocuk gibi heyecanlandırdı", "cocuk gibi heyecanlandirdi",
                "çocuk gibi heyecanlandım", "cocuk gibi heyecanlandim"
            ],
            "meaning": (
                "A magical discovery scene filled with awe, wonder, curiosity, "
                "and childlike excitement."
            ),
        },
        {
            "signals": [
                "dostunun onu satması", "dostunun onu satmasi",
                "sırtından bıçakladı", "sirtindan bicakladi",
                "güvendiği kişi ihanet etti", "guvendigi kisi ihanet etti",
                "ihanet", "sattı", "satti"
            ],
            "meaning": (
                "A betrayal scene where trust collapses because someone close "
                "unexpectedly turns against the character."
            ),
        },
        {
            "signals": [
                "sonunda kurtuldu", "oradan kaçtığı sahne", "oradan kactigi sahne",
                "kaçmaya çalışıyordu", "kacmaya calisiyordu",
                "kaçmaya çalışıyodu", "kacmaya calisiyodu",
                "zincirlerinden kurtuldu", "özgürleştiği an",
                "ozgurlestigi an", "özgürleşti", "ozgurlesti"
            ],
            "meaning": (
                "A liberation scene where a character escapes an oppressive "
                "situation and feels emotional freedom."
            ),
        },
        {
            "signals": [
                "birbirlerinden hoşlanıyorlar", "birbirlerinden hoslaniyorlar",
                "hoşlanıyolar", "hoslaniyolar", "laf sokuyorlar",
                "laf sokuyolar", "bakışıyorlar", "bakisiyorlar",
                "bakışıyolar", "bakisiyolar", "bir şey diyemiyorlar",
                "bir sey diyemiyorlar", "bişey diyemiyo", "bisey diyemiyo",
                "duygusal gerilim", "sürekli tersleşiyorlar",
                "surekli terslesiyorlar", "seviyorlar ama belli etmiyorlar"
            ],
            "meaning": (
                "A romantic tension scene where two characters hide emotional "
                "attraction behind teasing, emotional hesitation, and unresolved "
                "chemistry. This suggests slow burn intimacy, vulnerability, "
                "push-pull relationship dynamic, and enemies-to-lovers energy."
            ),
        },
        {
            "signals": [
                "başka dünya", "baska dunya", "başka bir dünya", "baska bir dunya",
                "ilk gördükleri an", "ilk gordukleri an", "keşfetmek istiyosun",
                "kesfetmek istiyosun", "oraya gitmek istedim", "büyülenmek hissi",
                "buyulenmek hissi", "her şeyi görmek istiyodum",
                "her seyi gormek istiyodum", "dünyası aşırı iyiydi",
                "dunyasi asiri iyiydi"
            ],
            "meaning": (
                "A scene focused on awe, discovery, curiosity, and the emotional "
                "excitement of entering a new world. This suggests exploration "
                "curiosity, discovery feeling, childlike curiosity, and adventure wonder."
            ),
        },
        {
            "signals": [
                "huzurlu hissettirdi", "sakin sahneydi", "yağmur yağıyodu",
                "yagmur yagiyodu", "sarı ışık vardı", "sari isik vardi",
                "çay koyuyodu", "cay koyuyodu", "güvende hissediyosun",
                "guvende hissediyosun", "çok cozyydi", "cok cozyydi",
                "içimi rahatlattı", "icimi rahatlatti"
            ],
            "meaning": (
                "A calm and emotionally safe atmosphere focused on warmth, quiet "
                "comfort, healing energy, and peaceful human connection. This "
                "suggests cozy atmosphere, emotional safety, peaceful warmth, "
                "and calm intimacy."
            ),
        },
        {
            "signals": [
                "yağmurlu yalnız sokak", "yagmurlu yalniz sokak",
                "sessiz apartman", "uzun suskunluk", "garip boşluk hissi",
                "garip bosluk hissi", "hüzünlü ama huzurlu",
                "huzunlu ama huzurlu", "yalnız ama rahatlatıcı",
                "yalniz ama rahatlatici"
            ],
            "meaning": (
                "A reflective and melancholic atmosphere built around emotional "
                "distance, quiet loneliness, rainy urban mood, peaceful solitude, "
                "and bittersweet emotional reflection."
            ),
        },
        {
            "signals": [
                "alttan alta gerilim", "rahatsız edici gerilim",
                "rahatsiz edici gerilim", "huzursuz edici",
                "dışarıdan sakin ama tehlikeli", "disaridan sakin ama tehlikeli",
                "kontrollü gözüküp tehlikeli", "kontrollu gozukup tehlikeli",
                "tehlikeli olduğunu yavaş yavaş hissettirdi",
                "tehlikeli oldugunu yavas yavas hissettirdi",
                "bağırmadan gerilim", "bagirmadan gerilim",
                "bakışlarla gerilim", "bakislarla gerilim",
                "sessiz tehdit", "sakin ama korkutucu", "sakin ama tehlikeli",
                "konuşmadan gerilim", "konusmadan gerilim",
                "psikolojik baskı", "psikolojik baski", "gizli tehdit",
                "tekinsiz sakinlik"
            ],
            "meaning": (
                "A subtle psychological tension scene where a calm and controlled "
                "character slowly reveals a hidden sense of danger. The scene "
                "creates quiet menace, emotional unease, silent intimidation, "
                "controlled danger, and slow-burn suspense without loud conflict."
            ),
        },
    ]

    meanings = []

    for group in pattern_groups:
        if any(signal in text for signal in group["signals"]):
            meanings.append(group["meaning"])

    if not meanings:
        return scene_text

    return f"{scene_text} | Normalized meaning: {' '.join(meanings)}"
