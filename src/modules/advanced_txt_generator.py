import random

# ==============================
# VOCABULARIO AMPLIO
# ==============================
SPORTS_SUBJECTS = [
    "el equipo", "la selección", "el club", "el conjunto deportivo",
    "los jugadores", "el entrenador", "la escuadra"
]

SPORTS_ACTIONS = [
    "ganó", "perdió", "empató", "dominó", "mostró un gran nivel",
    "tuvo un mal desempeño", "sorprendió", "decepcionó"
]

SPORTS_EVENTS = [
    "el partido", "la final", "el torneo", "la liga",
    "el campeonato", "la competencia", "el amistoso"
]

SPORTS_ADJ_POS = ["excelente", "brillante", "sólido", "contundente"]
SPORTS_ADJ_NEG = ["deficiente", "lamentable", "irregular", "desastroso"]

SPORTS_CONTEXT = [
    "gracias a una buena estrategia",
    "por errores defensivos",
    "con apoyo de la afición",
    "tras una intensa preparación"
]

# ==============================
TECH_SUBJECTS = [
    "la empresa", "la compañía", "el sistema", "el software",
    "la plataforma", "el dispositivo", "el servicio digital"
]

TECH_ACTIONS = [
    "mejoró", "falló", "evolucionó", "colapsó",
    "fue actualizado", "presentó errores"
]

TECH_OBJECTS = [
    "el sistema", "la aplicación", "el software", "la infraestructura",
    "la red", "la plataforma digital", "el producto tecnológico"
]

TECH_ADJ_POS = ["eficiente", "innovador", "estable", "seguro"]
TECH_ADJ_NEG = ["inestable", "defectuoso", "vulnerable", "ineficiente"]

TECH_CONTEXT = [
    "tras la última actualización", "debido a un fallo de seguridad",
    "gracias a nuevas mejoras", "por problemas técnicos"
]

# ==============================
# GENERADORES DE FRASES
# ==============================
def generate_sports_sentence():
    subject = random.choice(SPORTS_SUBJECTS)
    action = random.choice(SPORTS_ACTIONS)
    event = random.choice(SPORTS_EVENTS)
    context = random.choice(SPORTS_CONTEXT)
    adj = random.choice(SPORTS_ADJ_POS + SPORTS_ADJ_NEG)

    structures = [
        f"{subject} {action} {event} con un rendimiento {adj} {context}",
        f"{event.capitalize()} donde {subject} {action} de manera {adj}",
        f"{subject.capitalize()} tuvo un desempeño {adj} en {event} {context}",
        f"Durante {event}, {subject} {action} con un nivel {adj}"
    ]
    return random.choice(structures)

def generate_tech_sentence():
    subject = random.choice(TECH_SUBJECTS)
    action = random.choice(TECH_ACTIONS)
    obj = random.choice(TECH_OBJECTS)
    context = random.choice(TECH_CONTEXT)
    adj = random.choice(TECH_ADJ_POS + TECH_ADJ_NEG)

    structures = [
        f"{subject.capitalize()} {action} {obj} y resultó ser {adj} {context}",
        f"{obj.capitalize()} se mostró {adj} cuando {subject} {action}",
        f"{subject.capitalize()} presentó un sistema {adj} {context}",
        f"{action.capitalize()} del {obj} dejó una experiencia {adj}"
    ]
    return random.choice(structures)

# ==============================
# FUNCIÓN PRINCIPAL
# ==============================
def generate_txt(output_path: str, total_samples: int = 500, sports_ratio: float = 0.5):
    """
    Genera un archivo TXT etiquetado para entrenamiento.
    Formato: Deportes|texto
            Tecnologia|texto
    """
    sports_count = int(total_samples * sports_ratio)
    tech_count = total_samples - sports_count
    sentences = []

    # Agregar palabras solas como refuerzo
    sports_keywords = ["futbol", "gol", "liga", "partido", "equipo"]
    tech_keywords = ["ia", "software", "celular", "telefono", "computadora"]

    for _ in range(sports_count):
        if random.random() < 0.2:
            sentences.append(f"Deportes|{random.choice(sports_keywords)}")
        else:
            sentences.append(f"Deportes|{generate_sports_sentence()}")

    for _ in range(tech_count):
        if random.random() < 0.2:
            sentences.append(f"Tecnologia|{random.choice(tech_keywords)}")
        else:
            sentences.append(f"Tecnologia|{generate_tech_sentence()}")

    random.shuffle(sentences)

    with open(output_path, "w", encoding="utf-8") as f:
        for s in sentences:
            f.write(s + "\n")
