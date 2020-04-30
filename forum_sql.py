import sqlite3

conn = sqlite3.connect('forum.db')
c = conn.cursor()
c.execute('''CREATE TABLE FORUM
   (name           TEXT    NOT NULL,
   role            TEXT    NOT NULL,
   topic           TEXT    NOT NULL,
   content         TEXT    NOT NULL
   "id" char(36) default (lower(hex(randomblob(4))) || '-' || lower(hex(randomblob(2))) || '-4' || substr(lower(hex(randomblob(2))),2) || '-' || substr('89ab',abs(random()) % 4 + 1, 1) || substr(lower(hex(randomblob(2))),2) || '-' || lower(hex(randomblob(6)))));''')
conn.commit()
conn.close()
