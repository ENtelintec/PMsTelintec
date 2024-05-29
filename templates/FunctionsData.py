# -*- coding: utf-8 -*-
__author__ = 'Edisson Naula'
__date__ = '$ 29/may./2024  at 10:41 $'

import json
from datetime import datetime

import numpy as np
import pandas as pd
from templates.controllers.pmodel_controller import get_data_fichaje_db


def get_cumulative_data_fichajes_dict(dic_data: dict, date=None) -> tuple[int, int]:
    """
    Gets the cumulative data from a dictionary of data from fichajes files
    :param date: date since the data is taken into account
    :param dic_data:
    :return:
    """
    if date is not None:
        date = pd.to_datetime(date)
    total_days = 0
    total_value = 0
    if date is None:
        for year in dic_data.keys():
            for month in dic_data[year].keys():
                total_days += len(dic_data[year][month].keys())
                for day in dic_data[year][month].keys():
                    value = dic_data[year][month][day]["value"]
                    if value is not None and value != "":
                        total_value += value
    else:
        for year in dic_data.keys():
            for month in dic_data[year].keys():
                for day in dic_data[year][month].keys():
                    if date.month <= int(month) and date.year <= int(year) and date.day <=int(day):
                        value = dic_data[year][month][day]["value"]
                        total_days += 1
                        if value is not None and value != "":
                            total_value += value
    return total_days, total_value


def get_basic_data_train_dict(dic_data: dict) -> list:
    """
    Gets the basic data from a dictionary of data from fichajes files
    :param dic_data:
    :return:
    """
    data_out = []
    total_days = 0
    total_value = 0
    for year in dic_data.keys():
        for month in dic_data[year].keys():
            total_days += len(dic_data[year][month].keys())
            for day in dic_data[year][month].keys():
                value = dic_data[year][month][day]["value"]
                total_days += 1
                total_value += value if value is not None and value != "" else 1.0
                # day of the week
                dow = datetime(int(year), int(month), int(day)).weekday()
                if len(data_out) == 0:
                    data_out.append([dow, int(month), total_days, total_value, total_value, 0, total_value, 0])
                else:
                    aux = np.array(data_out)
                    data_out.append([dow, int(month), total_days, total_value, np.mean(aux[:, 3]), np.std(aux[:, 3]), np.median(aux[:, 3]), np.var(aux[:, 3])])
    return data_out


def get_data_fichaje_train():
    flag, error, result = get_data_fichaje_db()
    data_train = []
    for item in result:
        emp_id, absences, lates, extras, primes, normal = item
        # absences_days, absences_value = get_cumulative_data_fichajes_dict(json.loads(absences))
        # lates_days, lates_value = get_cumulative_data_fichajes_dict(json.loads(lates))
        # extras_days, extras_value = get_cumulative_data_fichajes_dict(json.loads(extras))
        # primes_days, primes_value = get_cumulative_data_fichajes_dict(json.loads(primes))
        data_out_absences = get_basic_data_train_dict(json.loads(absences))
        data_train += data_out_absences
    return data_train
