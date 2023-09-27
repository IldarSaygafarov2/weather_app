from db.base import connect_db, commit_and_close


def check_user_exists(db_name, username):
    conn, cursor = connect_db(db_name)
    sql = "SELECT * FROM users WHERE username = ?;"
    cursor.execute(sql, (username,))
    user = cursor.fetchone()
    if not user:
        return False, False

    return True, user[0]


def add_user(db_name, username):
    conn, cursor = connect_db(db_name)
    sql = "INSERT INTO users(username) VALUES (?);"
    cursor.execute(sql, (username,))
    commit_and_close(conn)


def add_weather(db_name, **weather_data):
    conn, cursor = connect_db(db_name)
    keys = ', '.join([key for key in weather_data.keys()])
    values = tuple(weather_data.values())
    _values = ', '.join(['?' for _ in range(len(weather_data.keys()))])
    sql = f"INSERT INTO weather({keys}) VALUES ({_values})"
    cursor.execute(sql, values)
    commit_and_close(conn)


def get_weather_data(db_name, user_id):
    conn, cursor = connect_db(db_name)
    sql = "SELECT * FROM weather WHERE user_id = ?;"
    cursor.execute(sql, (user_id,))
    data = cursor.fetchall()
    return data


def delete_user_weather(db_name, user_id):
    conn, cursor = connect_db(db_name)
    sql = "DELETE FROM weather WHERE user_id = ?;"
    cursor.execute(sql, (user_id,))
    commit_and_close(conn)

# check_user_exists("../weather.db", 'asdf')


def get_all_weather(db_name):
    conn, cursor = connect_db(db_name)
    sql = "SELECT * FROM weather"
    cursor.execute(sql)
    return cursor.fetchall()
