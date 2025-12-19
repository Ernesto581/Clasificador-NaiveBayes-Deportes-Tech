import spacy
import re
import unicodedata

nlp = spacy.load("es_core_news_sm")

# ==============================
# SINÓNIMOS CONTROLADOS
# ==============================
SYNONYMS = {
    "futbol": "futbol",
    "balon": "futbol",
    "pelota": "futbol",
    "gol": "gol",
    "liga": "liga",
    "partido": "partido",
    "equipo": "equipo",
    "jugador": "jugador",

    "ia": "inteligencia artificial",
    "ai": "inteligencia artificial",
    "inteligencia": "inteligencia artificial",
    "tecnologia": "tecnologia",
    "software": "software",
    "celular": "telefono",
    "movil": "telefono",
    "telefono": "telefono",
    "computadora": "computadora",
    "pc": "computadora"
}

# ==============================
# NORMALIZAR ACENTOS
# ==============================
def remove_accents(text: str) -> str:
    """
    Elimina tildes pero conserva la ñ
    """
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return text

# ==============================
# PREPROCESAMIENTO PRINCIPAL
# ==============================
def preprocess(text: str) -> str:
    if not text or not text.strip():
        return ""

    text = text.lower()
    text = remove_accents(text)
    text = re.sub(r"[^a-zñ\s]", " ", text)

    doc = nlp(text)
    tokens = []

    for token in doc:
        if token.is_stop or token.is_punct or token.is_space:
            continue

        lemma = token.lemma_.strip()
        if len(lemma) < 2:
            continue

        lemma = SYNONYMS.get(lemma, lemma)
        tokens.append(lemma)

    # Refuerzo para palabras sueltas
    if len(tokens) == 1:
        tokens.append(tokens[0])

    return " ".join(tokens)

