class DB:
    username = ""
    password = ""
    mongo_claster = ""
    host = f"mongodb+srv://{username}:{password}@{mongo_claster}/test"
    params = ''

    mongo_uri = host + '?' + params

    db_name = 'welltory_test'


date_pattern = "%Y-%m-%d"
