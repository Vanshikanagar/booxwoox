import pymysql
import secret

rds_host = secret.db_endpoint
name = secret.db_username
password = secret.db_password
order_db = secret.db_order
user_db = secret.db_user
port = 3306

def connectOrderDb():
    conn = None

    try:
        conn = pymysql.connect(host=rds_host, user=name,
                               passwd=password, db=order_db,
                               connect_timeout=5,
                               cursorclass=pymysql.cursors.DictCursor)
        print("Database connection success")
    except Exception as e:
        print("Database connection failded due to {}".format(e))
    return conn


def connectUserDb():
    conn = None

    try:
        conn = pymysql.connect(host=rds_host, user=name,
                               passwd=password, db=user_db,
                               connect_timeout=5,
                               cursorclass=pymysql.cursors.DictCursor)
        print("Database connection success")
    except Exception as e:
        print("Database connection failded due to {}".format(e))
    return conn