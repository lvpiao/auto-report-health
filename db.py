# encoding:utf-8

import sqlite3
# 用户基本参数
# username = "username"
# password = "password"

# conn = sqlite3.connect('jnuser.db')
# c = conn.cursor()
# c.execute('''CREATE TABLE user
#        (ID CHAR(50) PRIMARY KEY  NOT NULL,
#        PASSWORD        CHAR(50),
#        EMAIL         CHAR(50));''')
# c.close()
# conn.close()


def insert(user: tuple):
    conn = sqlite3.connect('jnuser.db')
    c = conn.cursor()
    c.execute("REPLACE INTO user \
    VALUES (?,?,?);", tuple(user))
    c.close()
    conn.commit()
    conn.close()

def delete(user: tuple):
    conn = sqlite3.connect('jnuser.db')
    c = conn.cursor()
    c.execute("DELETE FROM user \
    WHERE  ID = ? and PASSWORD = ?;", tuple(user))
    c.close()
    conn.commit()
    conn.close()

def alluser():
    conn = sqlite3.connect('jnuser.db')
    c = conn.cursor()
    res = c.execute("select * from user;").fetchall()
    c.close()
    conn.close()
    return res

print(alluser())
