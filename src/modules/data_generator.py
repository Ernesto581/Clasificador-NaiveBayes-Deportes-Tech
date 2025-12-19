import random


# ==============================
# ANCHOR TERMS (CLAVE)
# ==============================

SPORTS_ANCHORS = [
    "fútbol", "gol", "partido", "entrenador",
    "equipo", "liga", "campeonato", "torneo","pelota", "baseball", "torneo", "competencia",
    "partido"
]

TECH_ANCHORS = [
    "tecnología", "inteligencia artificial", "ia",
    "software", "sistema", "aplicación",
    "celular", "smartphone", "algoritmo"
]


# ==============================
# CONTEXTO DEPORTES
# ==============================

SPORTS_POS = [
    "victoria importante", "gran actuación",
    "buen rendimiento", "desempeño sólido",
    "triunfo histórico"
]

SPORTS_NEG = [
    "derrota dolorosa", "mal rendimiento",
    "error defensivo", "fracaso deportivo",
    "crisis del equipo"
]

SPORTS_STRUCTURES = [
    "El {anchor} mostró una {adj}",
    "Buen nivel de {adj} en el {anchor}",
    "El {anchor} fue clave en una {adj}",
    "Se produjo una {adj} durante el {anchor}"
]


# ==============================
# CONTEXTO TECNOLOGÍA
# ==============================

TECH_POS = [
    "avance significativo", "mejora del sistema",
    "innovación tecnológica", "optimización eficiente",
    "actualización exitosa"
]

TECH_NEG = [
    "fallo crítico", "problema técnico",
    "vulnerabilidad de seguridad",
    "error del software", "colapso del sistema"
]

TECH_STRUCTURES = [
    "La {anchor} presentó una {adj}",
    "Se detectó una {adj} en la {anchor}",
    "Problemas de {adj} relacionados con la {anchor}",
    "La {anchor} sufrió un {adj}"
]


# ==============================
# GENERADOR PRINCIPAL
# ==============================

def generate_dataset(
    total_samples=700,
    sports_ratio=0.5,
    noise=0.1,
    anchor_ratio=0.7
):
    """
    Dataset avanzado con términos ancla.

    - anchor_ratio: % de frases que SIEMPRE incluyen términos clave
    - noise: ruido controlado sin tocar anclas
    """

    X, y = [], []

    sports_n = int(total_samples * sports_ratio)
    tech_n = total_samples - sports_n

    # -------- DEPORTES --------
    for _ in range(sports_n):
        use_anchor = random.random() < anchor_ratio

        anchor = random.choice(SPORTS_ANCHORS) if use_anchor else random.choice(SPORTS_ANCHORS)
        adj = random.choice(SPORTS_POS + SPORTS_NEG)

        text = random.choice(SPORTS_STRUCTURES).format(
            anchor=anchor,
            adj=adj
        )

        X.append(text)
        y.append("Deportes")

    # -------- TECNOLOGÍA --------
    for _ in range(tech_n):
        use_anchor = random.random() < anchor_ratio

        anchor = random.choice(TECH_ANCHORS) if use_anchor else random.choice(TECH_ANCHORS)
        adj = random.choice(TECH_POS + TECH_NEG)

        text = random.choice(TECH_STRUCTURES).format(
            anchor=anchor,
            adj=adj
        )

        X.append(text)
        y.append("Tecnologia")

    combined = list(zip(X, y))
    random.shuffle(combined)
    X, y = zip(*combined)

    return list(X), list(y)
