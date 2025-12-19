def load_labeled_file(path):
    X, y = [], []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if "|" not in line:
                continue
            label, text = line.strip().split("|", 1)
            X.append(text)
            y.append(label)

    return X, y
