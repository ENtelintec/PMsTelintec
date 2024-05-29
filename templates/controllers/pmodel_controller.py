# -*- coding: utf-8 -*-
__author__ = 'Edisson Naula'
__date__ = '$ 29/may./2024  at 10:34 $'

from templates.databases.connection import execute_sql


def get_data_fichaje_db():
    sql = "SELECT emp_id, absences, lates, extras, primes, normal FROM fichajes"
    flag, error, result = execute_sql(sql, None, 5)
    return flag, error, result
