import sqlite3


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Opened database successfully")
        return conn
    except sqlite3.Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)


def main():
    database = r"info2222.db"

    sql_create_messages_table=""" CREATE TABLE IF NOT EXISTS messages (
        id integer PRIMARY KEY,
        from_user text NOT NULL,
        to_user text NOT NULL,
        subject text NOT NULL,
        body text,
        create_at text NOT NULL
    ); """

    sql_create_replies_table="""CREATE TABLE IF NOT EXISTS replies (
        id integer PRIMARY KEY,
        from_user text NOT NULL,
        message_id integer NOT NULL,
        body text,
        create_at text NOT NULL,
        FOREIGN KEY (message_id) REFERENCES messages (id)
    );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_messages_table)

        # create tasks table
        create_table(conn, sql_create_replies_table)
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()
