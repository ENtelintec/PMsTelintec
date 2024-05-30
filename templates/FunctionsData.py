# -*- coding: utf-8 -*-
__author__ = 'Edisson Naula'
__date__ = '$ 29/may./2024  at 10:41 $'

import json
from calendar import monthrange
from datetime import datetime

import numpy as np
import pandas as pd
from templates.controllers.pmodel_controller import get_data_fichaje_db


def get_vector_absence_normal(value, total_days, total_value, year, month, day, data_out_x):
    total_days += 1
    total_value += value if value is not None and value != "" else 0.0
    # day of the week
    dow = datetime(int(year), int(month), int(day)).weekday()
    if len(data_out_x) == 0:
        return [dow, int(month), total_days, total_value, total_value, 0, total_value, 0]
    else:
        aux = np.array(data_out_x)
        return [dow, int(month), total_days, total_value, np.mean(aux[:, 3]), np.std(aux[:, 3]),
                np.median(aux[:, 3]), np.var(aux[:, 3])]


def update_dict(dict_data: dict, year: str, month: str, day: str, value: float, comment: str, timestamp: str):
    """
    Updates the dict with the new data.
    :param dict_data:
    :param year:
    :param month:
    :param day:
    :param value:
    :param comment:
    :param timestamp:
    :return:
    """
    if year not in dict_data.keys():
        dict_data[year] = {
            month: {
                day: {
                    "value": value,
                    "comment": comment,
                    "timestamp": timestamp
                }
            }
        }
    elif month not in dict_data[year].keys():
        dict_data[year][month] = {
            day: {
                "value": value,
                "comment": comment,
                "timestamp": timestamp
            }
        }
    else:
        dict_data[year][month][day] = {
            "value": value,
            "comment": comment,
            "timestamp": timestamp
        }
    return dict_data


def read_dict_and_vectorize(dic_data_absences, date_init):
    """
    Gets the data from the normal dict.
    :param dic_data_absences:
    :param date_init:
    :return:
    """
    total_days = 0
    total_value = 0
    data_x = []
    data_y = []
    today = datetime.now()
    years_up_to_now = [i for i in range(date_init.year, today.year + 1)]
    dict_data_normal = {}
    for year in years_up_to_now:
        for month in range(1, 13):
            days_of_month = get_days_work(datetime(year, month, 1))
            for day in days_of_month:
                if str(year) not in dic_data_absences.keys():
                    dic_data_absences[str(year)] = {
                        str(month): {
                            str(day): {
                                "value": 0.0,
                                "comment": "",
                                "timestamp": str(datetime(year, month, day))
                            }
                        }
                    }
                    dict_data_normal = update_dict(dict_data_normal, str(year), str(month), str(day), 0.0, "",
                                                   str(datetime(year, month, day)))
                    total_days += 1
                    total_value += 0.0
                    data_x.append(get_vector_absence_normal(0.0, total_days, total_value, year, month, day, data_x))
                    data_y.append([0, 0.0])
                    continue
                if str(month) not in dic_data_absences[str(year)].keys():
                    dic_data_absences[str(year)][str(month)] = {
                        str(day): {
                            "value": 0.0,
                            "comment": "",
                            "timestamp": str(datetime(year, month, day))
                        }
                    }
                    dict_data_normal = update_dict(dict_data_normal, str(year), str(month), str(day), 0.0, "",
                                                   str(datetime(year, month, day)))
                    total_days += 1
                    total_value += 0.0
                    data_x.append(get_vector_absence_normal(0.0, total_days, total_value, year, month, day, data_x))
                    data_y.append([0, 0.0])
                    continue
                if str(day) not in dic_data_absences[str(year)][str(month)].keys():
                    dic_data_absences[str(year)][str(month)][str(day)] = {
                        "value": 0.0,
                        "comment": "",
                        "timestamp": str(datetime(year, month, day))
                    }
                    dict_data_normal = update_dict(dict_data_normal, str(year), str(month), str(day), 0.0, "",
                                                   str(datetime(year, month, day)))
                    total_days += 1
                    total_value += 0.0
                    data_x.append(get_vector_absence_normal(0.0, total_days, total_value, year, month, day, data_x))
                    data_y.append([0, 0.0])
                else:
                    value = dic_data_absences[str(year)][str(month)][str(day)]["value"]
                    value = value if value is not None and value != "" else 1.0
                    total_days += 1
                    total_value += value
                    data_x.append(get_vector_absence_normal(value, total_days, total_value, year, month, day, data_x))
                    data_y.append([1, value])
                    # print(data_x[-1],  data_y[-1])
    return dict_data_normal, data_x, data_y


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
                    if date.month <= int(month) and date.year <= int(year) and date.day <= int(day):
                        value = dic_data[year][month][day]["value"]
                        total_days += 1
                        if value is not None and value != "":
                            total_value += value
    return total_days, total_value


def get_days_work(date: datetime):
    """
    Get the days of the month that are not sundays.
    :param date: The date.
    :return: The list of days.
    """
    n_days_month = monthrange(date.year, date.month)
    last_day = n_days_month[1]
    days_of_the_month = [i for i in range(1, last_day + 1)]
    # exclude sundays from the list
    work_days = []
    for day in days_of_the_month:
        date_aux = datetime(date.year, date.month, day)
        if date_aux.weekday() != 6:
            work_days.append(day)
    return work_days


def get_basic_data_train_dict_absences(dic_data_absences: dict, date_init=None) -> tuple:
    """
    Gets the basic data from a dictionary of data from fichajes files
    :param date_init:
    :param dic_data_absences:
    :return:
    """
    if date_init is None:
        years = list(dic_data_absences.keys())
        years.sort()
        months = list(dic_data_absences[years[0]].keys())
        months.sort()
        days = list(dic_data_absences[years[0]][months[0]].keys())
        days.sort()
        date_init = datetime(int(years[0]), int(months[0]), int(days[0]))
    else:
        date_init = pd.to_datetime(date_init)
    dic_data_normal, data_x, data_y = read_dict_and_vectorize(dic_data_absences, date_init)
    return data_x, data_y, dic_data_normal


def get_data_fichaje_train(date_init: str = None):
    flag, error, result = get_data_fichaje_db()
    date_init = pd.to_datetime(date_init) if date_init is not None else None
    data_train_x_a = []
    data_train_y_a = []
    data_train_x_l = []
    data_train_y_l = []
    data_train_x_e = []
    data_train_y_e = []
    for item in result:
        emp_id, absences, lates, extras, primes, normal, admission = item
        date_init = pd.to_datetime(admission) if date_init is None else date_init
        # absences_days, absences_value = get_cumulative_data_fichajes_dict(json.loads(absences))
        # lates_days, lates_value = get_cumulative_data_fichajes_dict(json.loads(lates))
        # extras_days, extras_value = get_cumulative_data_fichajes_dict(json.loads(extras))
        # primes_days, primes_value = get_cumulative_data_fichajes_dict(json.loads(primes))
        data_x, data_y, data_dic_normal = get_basic_data_train_dict_absences(json.loads(absences), date_init)
        data_train_x_a += data_x
        data_train_y_a += data_y
        data_x, data_y, data_dic_normal = get_basic_data_train_dict_absences(json.loads(lates), date_init)
        data_train_x_l += data_x
        data_train_y_l += data_y
        data_x, data_y, data_dic_normal = get_basic_data_train_dict_absences(json.loads(extras), date_init)
        data_train_x_e += data_x
        data_train_y_e += data_y
    data_train = {
        "absences": {"x": data_train_x_a, "y": data_train_y_a},
        "lates": {"x": data_train_x_l, "y": data_train_y_l},
        "extras": {"x": data_train_x_e, "y": data_train_y_e}
    }
    return data_train


def get_data_fichaje_test_user(id_emp):
    flag, error, result = get_data_fichaje_db(id_emp)
    emp_id, absences, lates, extras, primes, normal = result if len(result) > 0 else [id_emp, {}, {}, {}, {}, {}]
    data_emp = get_basic_data_train_dict_absences(json.loads(absences))
    return data_emp
