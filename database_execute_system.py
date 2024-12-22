import sqlite3

def create_table(_cursor, _type):
    if _type == 'posts':
            _cursor.execute(f"""CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                author TEXT,
                content TEXT
            )""")

    if _type == 'accounts':
        _cursor.execute(f"""CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            password TEXT,
        )""")

def get_messages(_cursor:sqlite3.Cursor):
        return _cursor.execute("""SELECT author, content FROM posts """).fetchall()

def create_post(_cursor: sqlite3.Cursor, data):
        _cursor.execute(""" INSERT INTO posts (author, content) VALUES (?, ?)""", (data["author"], data["content"],))

def create_account(_cursor: sqlite3.Cursor,data):
        _cursor.execute("""INSERT OR IGNORE INTO accounts (name, password) VALUES (?, ?)""", (data['name'], data['password'],))

def login_account(_cursor: sqlite3.Cursor, data):
    user_id = _cursor.execute("""SELECT id FROM accounts WHERE name = ? AND password = ? AND isLogged = 'false' """, (data['name'], data['password'])).fetchone()
    # print(f'data {data['name']}, password {data['password']}')
    # print('user ',user_id)
    if user_id != None:
        _cursor.execute("""UPDATE accounts SET isLogged = 'true' WHERE id = ? """, user_id)
        return (True, user_id)
    else:
        del user_id
        return (False,)

def logout(_cursor:sqlite3.Cursor, data):
    print(f'LOGOUT data {data}, id {data['id']}' )
    _cursor.execute("""UPDATE accounts SET isLogged = 'false' WHERE id = ?""", (data['id'],))

def is_logged(_cursor:sqlite3.Cursor, data):
    answer =  _cursor.execute("""SELECT isLogged FROM accounts WHERE id = ?""", (data,)).fetchone()
    if answer == None:
        return (None,)
    return answer
def write_message(_cursor:sqlite3.Cursor, data:dict):
    _cursor.execute("""INSERT INTO posts (author, content) VALUES (?, ?)""", (data['author'], data['content']))

