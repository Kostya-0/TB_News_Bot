import sqlite3

con = sqlite3.connect('bot.db', check_same_thread=False)
cur = con.cursor()
# cur.execute("CREATE TABLE IF NOT EXISTS Users (chatid INT, animeser TEXT, animemov TEXT)")


def add_user(idd):
    a = cur.execute(f'SELECT chatid FROM Users WHERE chatid == {idd}').fetchall()
    if len(a) == 0:
        cur.execute(f'''INSERT INTO Users(chatid) VALUES({idd})''')
        con.commit()


def update_(idd, name, is_):
    if cur.execute(f'SELECT {name} FROM Users WHERE chatid == {idd}').fetchone()[0] == 'n' and is_:
        cur.execute(f'UPDATE Users SET {name} = "y" WHERE chatid = {idd}')
    elif cur.execute(f'SELECT {name} FROM Users WHERE chatid == {idd}').fetchone()[0] == 'y' and not is_:
        cur.execute(f'UPDATE Users SET {name} = "n" WHERE chatid = {idd}')
    con.commit()


def get_user(name):
    return cur.execute(f'SELECT chatid FROM Users WHERE {name} == "y"').fetchall()


def check_user(idd, name):
    s = cur.execute(f'SELECT {name} FROM Users WHERE chatid == {idd}').fetchone()
    if s:
        return cur.execute(f'SELECT {name} FROM Users WHERE chatid == {idd}').fetchone()[0] == 'y'
    else:
        return False
