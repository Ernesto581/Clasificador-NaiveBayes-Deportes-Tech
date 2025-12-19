ANCHOR_RULES = {
    "Deportes": [
        # deportes generales
        "futbol", "baloncesto", "tenis", "beisbol", "voleibol",
        "deporte", "deportivo",

        # elementos clave
        "gol", "cancha", "estadio", "arbitro", "entrenador",
        "jugador", "equipo", "seleccion",

        # eventos
        "liga", "torneo", "campeonato", "final", "partido",

        # acciones
        "marcar", "anotar", "defender", "atacar"
    ],

    "Tecnologia": [
        "ia", "inteligencia artificial", "tecnologia",
        "software", "hardware", "algoritmo",
        "programacion", "codigo", "computadora",
        "celular", "internet", "redes",
        "sistema", "digital", "robot"
    ]
}


def classify_short_text(text):
    text = text.lower().strip()

    scores = {"Deportes": 0, "Tecnologia": 0}

    for label, keywords in ANCHOR_RULES.items():
        for kw in keywords:
            if kw in text:
                scores[label] += 1

    best_label = max(scores, key=scores.get)

    if scores[best_label] == 0:
        return None

    # confianza proporcional
    confidence = min(0.6 + scores[best_label] * 0.1, 0.95)

    return {
        "class": best_label,
        "confidence": confidence,
        "method": "semantic_rules"
    }
