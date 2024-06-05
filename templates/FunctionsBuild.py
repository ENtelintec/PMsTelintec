# -*- coding: utf-8 -*-
__author__ = 'Edisson Naula'
__date__ = '$ 29/may./2024  at 10:18 $'

from keras import Sequential
from keras.src.layers import Dense

from static.constants import path_model
from templates.FunctionsData import get_data_fichaje_test_user


def create_sequential_model(layers, filepath=None):
    model = Sequential()
    for index, item in enumerate(layers):
        if index == 0:
            model.add(Dense(item["units"], input_shape=item["shape"], activation=item["activation"]))
            continue
        model.add(Dense(item["units"], activation=item["activation"]))
    # model.add(Dense(4, input_shape=(2,), activation='relu'))
    # model.add(Dense(4, activation='relu'))
    # model.add(Dense(1, activation='sigmoid'))
    # save the model
    filepath = path_model if filepath is None else filepath
    model.save(filepath)
    return model, path_model


def compile_model(model):
    model.compile(loss='binary_crossentropy', optimizer='adam')
    return model


def fit_model(model, x, y):
    model.fit(x, y, epochs=500, verbose=0)
    return model


def define_sample_for_prediction(day_of_week, month, id_emp):
    data_emp = get_data_fichaje_test_user(id_emp)


