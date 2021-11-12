import psycopg2
from configurations import getConfiguration

def connectToPSQL(queryText="""SELECT version()""", v=False):
    """ Connect to the PostgreSQL database server """
    connection = None
    try:
        parameters = getConfiguration.config('database.ini', 'postgresql')
        if v: print(f'Connecting to the PostgreSQL database using these parameters: {parameters}')
        connection = psycopg2.connect(**parameters)
        cursor = connection.cursor()
        if v:
            print(f'PostgreSQL server information: {connection.get_dsn_parameters()}')
            cursor.execute("""SELECT version()""")
            print(f'PostgreSQL database version: {cursor.fetchall()}')
        cursor.execute(queryText)
        return cursor.fetchall()
    except (Exception, psycopg2.Error) as error:
        print(f'There was an error when connecting: {error}')
    finally:
        if connection:
            cursor.close()
            connection.close()
        if v: print('PostgreSQL database connection closed.')



if __name__ == '__main__':

    a = connectToPSQL(v=True)
    print(f'results from query: {a}')