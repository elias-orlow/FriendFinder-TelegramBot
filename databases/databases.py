import sqlite3 as sq


async def create_db():
    global db, cur

    db = sq.connect('telegrambot.db')
    cur = db.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users('
                'user_id TEXT PRIMARY KEY, '
                'name TEXT NOT NULL, '
                'age TEXT NOT NULL, '
                'location TEXT NOT NULL, '
                'description TEXT, '
                'photo TEXT) ')

    db.commit()


async def edit_user_id(user_id):
    user = cur.execute("SELECT 1 FROM users WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?)", (user_id, '', '', '', '', ''))
        db.commit()


async def edit_user_profile(state, user_id):
    async with state.proxy() as data:
        cur.execute("UPDATE users SET name = ?, age = ?, location = ?, "
                    "description = ?, photo = ? WHERE user_id == ?",
                    (data['name'], data['age'], data['location'],
                     data['description'], data['photo'], user_id))
        db.commit()
