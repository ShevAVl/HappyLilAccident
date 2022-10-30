import sqlite3

conn = sqlite3.connect(r'CommonData.db')

def dump(inp):
    cur = conn.cursor()
    cur.execute("SELECT value FROM ServerObjects where key='{}'".format(inp))
    value = cur.fetchall()
    print(value)

def getValue(key):
    cur = conn.cursor()
    cur.execute(f"SELECT value FROM ServerObjects where key='{key}'")
    value = cur.fetchone()[0]
    return value

def incNum(key):
    cur = conn.cursor()
    cur.execute(f"SELECT value FROM ServerObjects WHERE key='{key}'")
    num = int(cur.fetchone()[0]) + 1
    num = str(num)
    cur.execute(f"UPDATE ServerObjects SET value = '{num}' WHERE key='{key}'")
    conn.commit()