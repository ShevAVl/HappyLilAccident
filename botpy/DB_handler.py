import sqlite3
from auxiliary import getPath

conn = sqlite3.connect(getPath(r'../CommonData.db'))

'''Set of functions to interact with an sqlite database'''

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

def setValue(key, value):
    cur = conn.cursor()
    cur.execute(f"UPDATE ServerObjects SET value='{str(value)}' WHERE key='{key}'")
    conn.commit()