import sqlite3

conn = sqlite3.connect('forum.db')
c = conn.cursor()

c.execute('''CREATE TABLE FORUM
   (name           TEXT    NOT NULL,
   role            TEXT    NOT NULL,
   topic           TEXT    NOT NULL,
   reply           TEXT    NOT NULL,
   content         CHAR(300)    NOT NULL,
   id              CHAR(36)     default (lower(hex(randomblob(4))) || '-' || lower(hex(randomblob(2))) || '-4' || substr(lower(hex(randomblob(2))),2) || '-' || substr('89ab',abs(random()) % 4 + 1, 1) || substr(lower(hex(randomblob(2))),2) || '-' || lower(hex(randomblob(6)))),
   reply_id        CHAR(36)     default (lower(hex(randomblob(4))) || '-' || lower(hex(randomblob(2))) || '-4' || substr(lower(hex(randomblob(2))),2) || '-' || substr('89ab',abs(random()) % 4 + 1, 1) || substr(lower(hex(randomblob(2))),2) || '-' || lower(hex(randomblob(6)))));''')
conn.commit()

c.execute("INSERT INTO FORUM (name,role,topic,reply,content) \
      VALUES ('admin', 'admin', 'hello dear', 'no', 'this is test')")
conn.commit()
c.execute("INSERT INTO FORUM (name,role,topic,reply,content) \
      VALUES ('admin', 'admin', 'hello dear', 'yes', 'this is a test reply')")
conn.commit()
c.execute("INSERT INTO FORUM (name,role,topic,reply,content) \
      VALUES ('bob', 'user', 'hello dear', 'yes', 'this is another test reply')")
conn.commit()
c.execute("INSERT INTO FORUM (name,role,topic,reply,content) \
      VALUES ('bob', 'user', 'hello another', 'no', 'this is another another test')")
conn.commit()

c.execute("update FORUM set content=REPLACE(content,X'0D',X'0A')")
conn.commit()

cursor = c.execute("SELECT name, role, topic, content,id ,reply_id from FORUM")
for row in cursor:
    print(row)
