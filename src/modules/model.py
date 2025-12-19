from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

class NaiveBayesClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            sublinear_tf=True
        )
        self.model = MultinomialNB(alpha=0.5)

    def train(self, X_train, y_train):
        X_vect = self.vectorizer.fit_transform(X_train)
        self.model.fit(X_vect, y_train)

    def predict(self, text):
        X_vect = self.vectorizer.transform([text])
        return self.model.predict(X_vect)[0]

    def predict_proba(self, text):
        X_vect = self.vectorizer.transform([text])
        return self.model.predict_proba(X_vect)

    def get_model(self):
        return self.model

    def get_vectorizer(self):
        return self.vectorizer
