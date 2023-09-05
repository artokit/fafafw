import sqlite3


connect = sqlite3.connect('db.sqlite')
cursor = connect.cursor()


def add_user(user_id):
    try:
        cursor.execute(f'INSERT INTO USERS VALUES({user_id}, 0, null, 0)')
        connect.commit()
    except sqlite3.IntegrityError:
        return


def update_user_dep_tries(value, user_id):
    cursor.execute(f'UPDATE users SET dep_tries = {value} where user_id = {user_id}')
    connect.commit()


def get_user(user_id):
    return cursor.execute(f'SELECT * FROM USERS where user_id = {user_id}').fetchall()[0]


def set_deposit(site_id, deposit):
    cursor.execute(f'UPDATE POSTBACK SET deposit = {deposit} where id = {site_id}')
    connect.commit()


def get_tries(user_id):
    return cursor.execute(f'SELECT * FROM users where user_id = {user_id}').fetchall()[0][1]


def set_tries(tries, user_id):
    cursor.execute(f'UPDATE USERS SET tries = {tries+1} where user_id = {user_id}')
    connect.commit()


def add_register_user(site_id):
    cursor.execute(f'INSERT INTO POSTBACK VALUES({site_id}, 0)')
    connect.commit()


def get_site_id(site_id):
    return cursor.execute(f'SELECT * FROM POSTBACK where id = {site_id}').fetchall()


def set_site_id(user_id, site_id):
    cursor.execute(f'UPDATE USERS SET site_id = {site_id} where user_id = {user_id}')
    connect.commit()


def get_user_by_site_id(site_id):
    return cursor.execute(f'SELECT * FROM USERS where site_id = {site_id}').fetchall()


def get_users():
    return cursor.execute('SELECT * FROM USERS').fetchall()
