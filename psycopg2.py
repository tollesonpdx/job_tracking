import time
import os
import psycopg2
from configparser import ConfigParser
# from flask import Flask, request
# from flask_sqlalchemy import SQLAlchemy

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def config(filename=(os.path.join(__location__,'database.ini')), section='postgresql'):
    parser = ConfigParser()  # creating a parser
    parser.read(filename)  # reading the config file
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return db

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        params = config()
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        cur = conn.cursor()  # creating a cursor
        print('PostgreSQL database version:')
        cur.execute("""SELECT version()""")
        db_version = cur.fetchone()
        print(db_version)
        cur.close()  # close the PG connection
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')



if __name__ == '__main__':

    startTime = time.time()

    connect()

    print('total running time:',time.time()-startTime,'seconds')
