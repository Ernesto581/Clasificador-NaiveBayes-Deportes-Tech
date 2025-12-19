import os
import pickle
from datetime import datetime


MODEL_DIR = "data"


def get_next_version():
    if not os.path.exists(MODEL_DIR):
        return 1

    files = [
        f for f in os.listdir(MODEL_DIR)
        if f.startswith("modelo_v") and f.endswith(".pkl")
    ]

    if not files:
        return 1

    versions = [
        int(f.replace("modelo_v", "").replace(".pkl", ""))
        for f in files
    ]

    return max(versions) + 1


def save_model_versioned(model):
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)

    version = get_next_version()
    filename = f"modelo_v{version}.pkl"
    path = os.path.join(MODEL_DIR, filename)

    with open(path, "wb") as f:
        pickle.dump(model, f)

    return path


def load_latest_model():
    if not os.path.exists(MODEL_DIR):
        return None, None

    files = [
        f for f in os.listdir(MODEL_DIR)
        if f.startswith("modelo_v") and f.endswith(".pkl")
    ]

    if not files:
        return None, None

    latest = max(
        files,
        key=lambda f: int(f.replace("modelo_v", "").replace(".pkl", ""))
    )

    path = os.path.join(MODEL_DIR, latest)

    with open(path, "rb") as f:
        model = pickle.load(f)

    info = get_model_info(path)
    return model, info


def get_model_info(path):
    stat = os.stat(path)
    size_kb = round(stat.st_size / 1024, 2)
    modified = datetime.fromtimestamp(stat.st_mtime)

    return {
        "path": path,
        "size_kb": size_kb,
        "date": modified.strftime("%Y-%m-%d %H:%M:%S")
    }
