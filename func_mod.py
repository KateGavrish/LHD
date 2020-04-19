import numpy as np
import pandas as pd
import itertools
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

df = pd.read_csv('news.csv')

labels = df.label

x_train, x_test, y_train, y_test = train_test_split(df['text'], labels, test_size=0.2, random_state=7)

tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)
tfidf_train = tfidf_vectorizer.fit_transform(x_train)
tfidf_test = tfidf_vectorizer.transform(x_test)

pac = PassiveAggressiveClassifier(max_iter=50)
pac.fit(tfidf_train, y_train)

y_pred = pac.predict(tfidf_test)
score = accuracy_score(y_test, y_pred)


def pred(text):
    x_test = [text]
    tfidf_test = tfidf_vectorizer.transform(x_test)
    return pac.predict(tfidf_test)[0]

def analyz(text):
    """Возвращает основные фразы из текста"""
    import spacy
    import textacy.extract

    nlp = spacy.load('en_core_web_lg')
    doc = nlp(text)
    list_of_facts = list(textacy.extract.ngrams(doc, 4))

    return list_of_facts
