def predict(text):
    """Возвращает значение от 0 до 1 - фейковость новости"""
    import numpy as np
    from keras.preprocessing import sequence
    from keras.models import load_model
    from data.model_costr import vectorize
    import pandas as pd
    import re
    from sklearn.model_selection import train_test_split
    from keras.preprocessing import sequence
    from keras.models import Sequential
    from keras.layers import Dense, Dropout, Activation
    from keras.layers import Embedding
    from keras.layers import Conv1D, GlobalMaxPooling1D
    maxlen = 7916
    model = load_model('data/my_model.h5')
    a = model.predict(sequence.pad_sequences(np.array(vectorize(text)).reshape(-1, 1), maxlen=maxlen))
    c = []
    for x in a:
        x = list(x)
        c += x
    result = max(c)
    return result


def analyz(text):
    """Возвращает основные фразы из текста"""
    import spacy
    import textacy.extract

    nlp = spacy.load('en_core_web_lg')
    doc = nlp(text)
    list_of_facts = list(textacy.extract.ngrams(doc, 4))

    return list_of_facts
