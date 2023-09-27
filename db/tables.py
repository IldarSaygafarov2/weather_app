from db.base import connect_db, commit_and_close


def create_users_table(db_name):
    connection, cursor = connect_db(db_name)
    sql = """
    DROP TABLE IF EXISTS users;
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT
    );
"""
    cursor.executescript(sql)

    commit_and_close(connection)


def create_weather_table(db_name):
    connection, cursor = connect_db(db_name)

    sql = """
    DROP TABLE IF EXISTS weather;
    CREATE TABLE IF NOT EXISTS weather(
        weather_id INTEGER PRIMARY KEY AUTOINCREMENT,
        city_name TEXT,
        temp DECIMAL,
        timezone INTEGER,
        created_at DATETIME,
        sunset DATETIME,
        sunrise DATETIME,
        description TEXT,
        wind_speed DECIMAL,
        
        user_id INTEGER REFERENCES users(user_id)
    );
"""
    cursor.executescript(sql)
    commit_and_close(connection)


# create_users_table('../weather.db')
# create_weather_table('../weather.db')

