import pymysql
import secret

rds_host = secret.db_endpoint
name = secret.db_username
password = secret.db_password
user_db = secret.db_name_user
blogs_db = secret.db_name_blogs
service_db= secret.db_name_service

port = 3306

def connectUserDb():
    conn = None
    try:
        conn = pymysql.connect(host=rds_host, user=name,
                               passwd=password, db=user_db,
                               connect_timeout=5,
                               cursorclass=pymysql.cursors.DictCursor)
        print("Database connected")
    except Exception as e:
        print("Database connection has failed due to {}".format(e))
        return None

    return conn

def connectServiceDb():
    conn = None
    try:
        conn = pymysql.connect(host=rds_host, user=name,
                               passwd=password, db=service_db,
                               connect_timeout=5,
                               cursorclass=pymysql.cursors.DictCursor)
        print("Database connected")
    except Exception as e:
        print("Database connection has failed due to {}".format(e))
        return None

    return conn


def connectBlogsDb():
    conn = None
    try:
        conn = pymysql.connect(host=rds_host, user=name,
                               passwd=password, db=blogs_db,
                               connect_timeout=5,
                               cursorclass=pymysql.cursors.DictCursor)
        print("Database connected")
    except Exception as e:
        print("Database connection has failed due to {}".format(e))
        return None

    return conn
