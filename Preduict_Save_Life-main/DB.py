import mysql.connector as mysql
from mysql.connector import errorcode


# take the url od db
def create_connection():
    """create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:  # "mysql://db_admin:1420113tM!@appdb-rm-l4vq6f07188z41kilzo.mysql.me-central-1.rds.aliyuncs.com:3306/DATABASE"
        conn = mysql.connect(
            host="rm-l4vq6f07188z41kilzo.mysql.me-central-1.rds.aliyuncs.com",
            user="db_admin",
            password="1420113tM!",
            db="appdb",
        )
        return conn
    except mysql.Error as err:
        print(err)

    return conn


def create_table(conn, create_table_sql):
    """create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except mysql.Error as err:
        print(err)


# change based on device
def main():
    # "mysql://db_admin:1420113tM!@appdb-rm-l4vq6f07188z41kilzo.mysql.me-central-1.rds.aliyuncs.com:3306/DATABASE"
    # database = r"mysql://db_admin:1420tM!@appdb-rm-l4vq6f07188z41kilzo.mysql.me-central-1.rds.aliyuncs.com:3306/DATABASE"

    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS User (
                                        id INT PRIMARY KEY,
                                        name VARCHAR(50) NOT NULL,
                                        email VARCHAR(50) NOT NULL,
                                        password VARCHAR(50) NOT NULL,
                                        password_re_enter VARCHAR(50) NOT NULL
                                    ); """

    # create a database connection
    conn = create_connection()

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_projects_table)

    else:
        print("Error! cannot create the database connection.")


if __name__ == "__main__":
    main()
