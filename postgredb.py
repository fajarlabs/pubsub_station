#!D:/PYTHON/OCR/env2/Scripts/python

import psycopg2
from config import config
 
def myQuery(sql="", mode=None):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)

        # set autocommit 
        conn.autocommit = True
 
        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(sql)

        # set commit if not using autocommit
        #conn.commit()

        if mode != None :
            if mode.lower() == "fetchall" :
                return cur.fetchall()
            if mode.lower() == "fetchone":
                return cur.fetchone()

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
 