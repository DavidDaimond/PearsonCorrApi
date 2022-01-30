import numpy as np

from pymongo import MongoClient
from datetime import datetime

from config import DB


def connect():
    """
    The function to initialize database
    :return:
    """
    client = MongoClient(DB.mongo_uri)

    return client[DB.db_name]


def get_from_db(user_id, dtype, database=connect()) -> (np.array, list):
    """
    takes the data about some parameter from database and return as numpy vector
    :param user_id:
    :param dtype: data need to get from database
    :param database: involved database
    :return: array of floats and list of dates
    """
    data_doc = database['data']

    user_id = int(user_id)

    docs = [x for x in data_doc.find({'user_id': user_id}) if dtype in x['data'].keys()]
    numbers = np.array([x['data'][dtype] for x in docs])
    dates = [x['date'] for x in docs]
    return [numbers, dates]


def write_corr_data(user_id: int,
                    x_dtype: str, y_dtype: str,
                    corr_value: float, p_value: float,
                    database=connect()):
    """
    write to calculates db info about correlation
    :param database:
    :param user_id:
    :param x_dtype:
    :param y_dtype:
    :param corr_value:
    :param p_value:
    :return:
    """
    calc_doc = database['calculates']

    data = {'user_id': user_id, 'x_data_type': x_dtype, 'y_data_type': y_dtype,
            'date': datetime(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day),
            'correlation': {
                'value': corr_value,
                'p_value': p_value
            },

            }

    calc_doc.insert_one(data)


def get_corr_data(user_id: int, x_dtype: str, y_dtype: str, database=connect()) -> [float, float, datetime]:
    """
    Return data about last correlation from database. If this data doesn't exist return False
    :param database: involved database
    :param user_id:
    :param x_dtype:
    :param y_dtype:
    :return: list of correlation-value, p-value and datetime of last calculation or False if this combination of
    user_id, x_dtype and y_dtype isn't in database
    """
    calc_doc = database['calculates']
    results = {x['date']: x['correlation'] for x in calc_doc.find({'user_id': user_id,
                                                                   'x_data_type': x_dtype,
                                                                   'y_data_type': y_dtype})}
    if not results:
        return False

    last_time = sorted(results)[-1]
    data = results[last_time]

    return [data['value'], data['p_value'], last_time]
