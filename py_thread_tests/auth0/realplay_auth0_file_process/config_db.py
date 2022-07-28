# https://www.postgresqltutorial.com/postgresql-python/connect/

# !/usr/bin/python
import os
from configparser import ConfigParser


#  read these env variables
# DB Info:
# Dev - POSTGRES_CONNECTION: '{
# "host":<hostname>
# "port":5432
# "user":"realplayuser"
# "password":<pswd>
# "database":"realplay_dce1"
# }'
# QA is all the same except for the database name
def config_db_from_env(
        host='env_var_not_set'
        , port='5432'
        , user='env_var_not_set'
        , password='env_var_not_set'
        , database='env_var_not_set'
    ):

    db = {
        'host': os.getenv('host', host)
        , 'port': os.getenv('port', port)
        , 'user': os.getenv('user', user)
        , 'password': os.getenv('password', password)
        , 'database': os.getenv('database', database)
    }

    return db


def config_db_from_ini(filename='conf/database.ini', section='DEV_DB'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db
