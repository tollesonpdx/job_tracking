import psycopg2
from configurations import getConfiguration

def connectToPSQL():
    """ Connect to the PostgreSQL database server """
    connection = None
    try:
        parameters = getConfiguration.config('database.ini', 'postgresql')
        print(f'Connecting to the PostgreSQL database using these parameters: {parameters}')
        connection = psycopg2.connect(**parameters)
        # connection = psycopg2.connect()
        cursor = connection.cursor()  # creating a cursor
        print('PostgreSQL database version:')
        cursor.execute("""SELECT version()""")
        db_version = cursor.fetchone()
        print(db_version)
        cursor.close()  # close the PG connection
    except (Exception) as error:
        print(f'There was an error when connecting: {error}')
    finally:
        if connection is not None:
            connection.close()
            print('Database connection closed.')



if __name__ == '__main__':

    connectToPSQL()
