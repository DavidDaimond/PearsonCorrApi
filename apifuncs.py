import numpy as np

from scipy.stats import pearsonr
from datetime import datetime

from config import date_pattern
from db import get_from_db, get_corr_data, write_corr_data, connect

database = connect()


def correlation(user_id: int, x_dtype: str, y_dtype: str):
    """
    Return data about correlation of x and y. If this data isn't in database, calculate it.
    :param user_id:
    :param x_dtype:
    :param y_dtype:
    :return:
    """
    corr_data = get_corr_data(user_id, x_dtype, y_dtype)
    if corr_data:
        date, corr_value, p_value = corr_data
        if date.day == datetime.now().day():
            return [float(corr_value), float(p_value)]

    x = get_from_db(user_id, x_dtype, database)
    y = get_from_db(user_id, y_dtype, database)

    x = {date: value for date, value in zip(x[1], x[0]) if date in y[1]}  # check the dates
    y = {date: value for date, value in zip(y[1], y[0]) if date in x.keys()}

    if not x:
        return False

    print(list(x.values()), list(y.values()))
    corr_value, p_value = pearsonr(list(x.values()), list(y.values()))

    return [float(corr_value), float(p_value)]


def calculate(user_id: int,
              x_dtype: str, y_dtype: str,
              x: list, y: list):
    _x = {datetime.strptime(v['date'], date_pattern): v['value'] for v in x}
    _y = {datetime.strptime(v['date'], date_pattern): v['value'] for v in y}

    x_dates = sorted(_x)
    vector_x = np.array([_x[i] for i in x_dates if i in _y.keys()])
    vector_y = np.array([_y[i] for i in x_dates if i in _y.keys()])

    corr_value, p = pearsonr(vector_x, vector_y)
    write_corr_data(user_id, x_dtype, y_dtype, corr_value, p, database)
    return float(corr_value), float(p)
