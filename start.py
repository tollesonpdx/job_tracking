import time
import pandas as pd
from os import path
import psycopg2
from configparser import ConfigParser
import csv

DATA_DIR = '/Users/chadtolleson/Documents/PSU/2020_Winter/Data_Science/Data_Science_IndStdy/data'
# DB_DIR = '/Users/chadtolleson/Documents/PSU/2020_Winter/Data_Science/Data_Science_IndStdy/db'
CODE_DIR = '/Users/chadtolleson/Documents/PSU/2020_Winter/Data_Science/Data_Science_IndStdy/code'

def config(filename=(path.join(CODE_DIR,'database.ini')), section='postgresql'):
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

def loadData():
    conn = None
    try:
        params = config()
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        cur = conn.cursor()  # creating a cursor

        cur.execute("""CREATE TABLE IF NOT EXISTS stocks ( 
                    Name text NOT NULL,
                    Date date NOT NULL,
                    High money NOT NULL,
                    Low money NOT NULL,
                    Open money NOT NULL,
                    Close money NOT NULL,
                    Volume real NOT NULL,
                    AdjClose money NOT NULL);
                    DELETE FROM stocks;""")
        print('component stocks table created and contents deleted')
        conn.commit()

        cur.execute("""CREATE TABLE IF NOT EXISTS gspc ( 
                    Name text NOT NULL,
                    Date date NOT NULL,
                    High money NOT NULL,
                    Low money NOT NULL,
                    Open money NOT NULL,
                    Close money NOT NULL,
                    Volume real NOT NULL,
                    AdjClose money NOT NULL);
                    DELETE FROM gspc;""")
        print('GSPC index table created and contents deleted')
        conn.commit()

        f = open(path.join(DATA_DIR,'all_stocks_5yr.csv'), 'r')
        next(f)
        cur.copy_from(f, 'stocks', sep=',', 
                        columns=('Date','High','Low','Open','Close',
                        'Volume','AdjClose','Name'))
        f.close()
        print('component stocks loaded')

        f = open(path.join(DATA_DIR,'^GSPC_data.csv'), 'r')
        next(f)
        cur.copy_from(f, 'gspc', sep=',', 
                        columns=('Date','High','Low','Open','Close',
                        'Volume','AdjClose','Name'))
        f.close()
        print('GSPC index data loaded')

        cur.execute("""SELECT name, count(*) 
                    FROM stocks
                    GROUP BY name
                    LIMIT 10; """)
        results = cur.fetchall()
        print('RESULTS - count of rows per ticker:')
        print(results)

        conn.commit()
        cur.close()  # close the PG connection
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

## Thanks to https://www.postgresqltutorial.com/postgresql-python/connect/ 
## for template for connecting to the database

if __name__ == '__main__':

    startTime = time.time()
    # data = pd.read_csv(path.join(DATA_DIR,'all_stocks_5yr.csv'))
    connect()
    loadData()

    print('total running time:',time.time()-startTime,'seconds')