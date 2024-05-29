# -*- coding: utf-8 -*-
__author__ = 'Edisson Naula'
__date__ = '$ 29/may./2024  at 10:18 $'

import pickle

from keras import Sequential
from keras.src.layers import Dense
from sklearn.datasets import make_blobs
from sklearn.preprocessing import MinMaxScaler

from static.constants import path_model


def create_sequential_model(layers):
    model = Sequential()
    for item in layers:
        model.add(Dense(item["units"], item["shape"], activation=item["activation"]))
    model.add(Dense(4, input_shape=(2,), activation='relu'))
    model.add(Dense(4, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    # save the model
    model.save(path_model)
    return model, path_model


def compile_model(model):
    model.compile(loss='binary_crossentropy', optimizer='adam')
    return model


def fit_model(model, x, y):
    model.fit(x, y, epochs=500, verbose=0)
    return model