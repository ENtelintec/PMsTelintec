# -*- coding: utf-8 -*-
__author__ = 'Edisson Naula'
__date__ = '$ 29/may./2024  at 10:34 $'

from templates.databases.connection import execute_sql


def get_data_fichaje_db(id_emp=None):
    id_emp = id_emp if id_emp is not None else "%"
    sql = ("SELECT "
           "fichajes.emp_id, "
           "fichajes.absences, "
           "fichajes.lates, "
           "fichajes.extras, "
           "fichajes.primes, "
           "fichajes.normal, "
           "employees.date_admission "
           "FROM fichajes "
           "INNER JOIN employees ON employees.employee_id = fichajes.emp_id "
           "WHERE emp_id LIKE %s ")
    vals = (id_emp,)
    flag, error, result = execute_sql(sql, vals, 2)
    return flag, error, result