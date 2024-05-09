import sqlite3 as sq


async def create_db():
    global db, cur

    db = sq.connect('telegrambot.db')
    cur = db.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS profile('
                'user_id TEXT PRIMARY KEY, '
                'photo TEXT, '
                'age TEXT, '
                'description TEXT, '
                'name TEXT)')

    db.commit()
