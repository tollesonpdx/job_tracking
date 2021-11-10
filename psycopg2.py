import time
import os
import psycopg2
from configurations import getConfiguration
# import configparser
# from flask import Flask, request
# from flask_sqlalchemy import SQLAlchemy

# __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# def config(filename=(os.path.join(__location__,'configs/database.ini')), section='postgresql'):
#     parser = configparser.ConfigParser()  # creating a parser
#     parser.read(filename)  # reading the config file, using default values is nothing is specified
#     connection_parameters = {}
#     if parser.has_section(section):
#         params = parser.items(section)
#         for param in params:
#             connection_parameters[param[0]] = param[1]
#     else:
#         raise Exception(f'Section {section} not found in the "{filename}" file')
#     return connection_parameters

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        params = getConfiguration.config('database.ini', 'postgresql')
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        cur = conn.cursor()  # creating a cursor
        print('PostgreSQL database version:')
        cur.execute("""SELECT version()""")
        db_version = cur.fetchone()
        print(db_version)
        cur.close()  # close the PG connection
    except (Exception) as error:
        print(f'There was an error when connecting: {error}')
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')



if __name__ == '__main__':

    connect()
