import numpy as np
import pandas as pd
import os
import re
from sklearn.model_selection import train_test_split
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.layers import Embedding
from keras.layers import LSTM
from keras.layers import Conv1D, MaxPooling1D
from keras.layers import Dense, Dropout, Activation
from keras.layers import Embedding
from keras.layers import Conv1D, GlobalMaxPooling1D
from keras.datasets import imdb


true = pd.read_csv('data/True.csv')
false = pd.read_csv('data/Fake.csv')

true['true'] = 1
false['true'] = 0

data = pd.concat([true, false])


def preprocess_text(sentence):
    sentence = re.sub('[^a-zA-Z]', ' ', sentence)
    sentence = re.sub(r"\s+[a-zA-Z]\s+", ' ', sentence)
    sentence = re.sub(r'\s+', ' ', sentence)

    return sentence.lower()


data['cleaned'] = data['text'].apply(preprocess_text)

corona_news = pd.read_csv('data/news.csv')
corona_news['cleaned'] = corona_news['text'].apply(preprocess_text)

list1 = ''.join(data['cleaned'].tolist()).split(' ')
list1.extend(''.join(corona_news['cleaned'].tolist()).split(' '))
unique = pd.Series(''.join(data['cleaned'].tolist()).split(' ')).unique()

item_to_index = {}
index_to_item = {}
for index, item in enumerate(unique):
    item_to_index[item] = index
    index_to_item[index] = item


def vectorize(text):
    return_list = []
    for word in text.split(' '):
        try:
            return_list.append(item_to_index[word])
        except:
            pass
    return return_list

if __name__ == '__main__':
    X = data['cleaned'].apply(vectorize)

    x_train, x_test, y_train, y_test = train_test_split(np.array(X), data['true'], test_size=0.8)

    # set parameters:
    max_features = 120645
    maxlen = 7916
    pool_size = 4
    batch_size = 32
    embedding_dims = 50
    filters = 250
    lstm_output_size = 70
    embedding_size = 128
    kernel_size = 3
    hidden_dims = 250
    epochs = 1

    x_train = x_train[:6000]
    x_test = x_test[:3000]
    y_train = y_train[:6000]
    y_test = y_test[:3000]
    x_train = sequence.pad_sequences(x_train, maxlen=maxlen)
    x_test = sequence.pad_sequences(x_test, maxlen=maxlen)

    model = Sequential()

    model.add(Embedding(max_features, embedding_dims, input_length=maxlen))
    model.add(Dropout(0.2))
    model.add(Conv1D(filters, kernel_size, padding='valid', activation='relu', strides=1))
    model.add(GlobalMaxPooling1D())
    model.add(Dense(hidden_dims))
    model.add(Dropout(0.2))
    model.add(Activation('relu'))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_data=(x_test, y_test))
    model.save('my_model.h5')
