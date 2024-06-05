# -*- coding: utf-8 -*-
__author__ = 'Edisson Naula'
__date__ = '$ 29/may./2024  at 10:25 $'

from dotenv import dotenv_values


secrets = dotenv_values(".env")
path_model = "models/model.keras"
path_data = "data/"