import spacy
import textacy.extract
import numpy as np
from keras.preprocessing import sequence
from keras.models import load_model
from  data.model_costr import vectorize

maxlen = 7916
model = load_model('data/my_model.h5')
nlp = spacy.load('en_core_web_lg')


def predict(text):
    """Возвращает значение от 0 до 1 - фейковость новости"""
    a = model.predict(sequence.pad_sequences(np.array(vectorize(text)).reshape(-1, 1), maxlen=maxlen))
    c = []
    for x in a:
        x = list(x)
        c += x
    result = max(c)
    return result


def analyz(text):
    """Возвращает основные фразы из текста"""
    nlp = spacy.load('en_core_web_lg')
    doc = nlp(text)
    list_of_facts = list(textacy.extract.ngrams(doc, 4))

    return list_of_facts