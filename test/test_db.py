import pytest

import requests
from dotenv import load_dotenv
import os

from code.helpers import *

load_dotenv()

def test_db_connect():
    db_name = "usajobs.db"
    conn = db_connect(db_name)

    assert conn is not None
    conn.close()

def test_create_table_db():
    try: 
        db_name = "usajobs.db"
        conn = db_connect(db_name)
    except Exception as e:
        print(e)

    sql_create_table = """CREATE TABLE IF NOT EXISTS positions_test 
                          (positionId int, positionTitle text,  
                          UNIQUE (positionId) ON CONFLICT IGNORE)"""

    db_create_table(conn, sql_create_table)

    cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='positions_test'")
    res = cur.fetchone()
    conn.close()

    assert res


def test_populate_db():
    # don't forget to teardown
    # try:

    pass


def test_uniquness():
    pass
    # test_entries = [(613490400, 'Operations Research Analyst (Senior Operations Research Analyst)', 'Internal Revenue Service', 114717.0, 'Per Year', 0.08333333333333333), 
    #                 (613490400, 'Operations Research Analyst (Senior Operations Research Analyst)', 'Internal Revenue Service', 114717.0, 'Per Year', 0.08333333333333333), 
    #                 (613490401, 'Data Analyst', 'Internal Revenue Service', 114717.0, 'Per Year', 0.08333333333333333)]

    # conn = db_connect()
    # create_tables(conn)

    # populate_db(test_entries)


    # conn = db_connect()
    # cur = conn.execute("SELECT COUNT(*) FROM positions")
    # res = cur.fetchall()
    # print(res)

    # assert res[0][0] == 2