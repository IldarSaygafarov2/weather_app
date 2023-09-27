import sqlite3


def connect_db(db_name):
    connection = sqlite3.connect(db_name, check_same_thread=False)
    cursor = connection.cursor()
    return connection, cursor


def commit_and_close(connection):
    connection.commit()
    connection.close()
