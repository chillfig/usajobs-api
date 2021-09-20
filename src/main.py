import sqlite3
from urllib.request import pathname2url

from variables import DB_NAME, DATA_POSITIONS, KEYWORDS, FILTER_ENABLED, OUTPUT_PATH
from helpers import *
from etl import *

from dotenv import load_dotenv
load_dotenv()

def main() -> None:
    """
    Creates and/or connects to a local sqlite database, and populates it with the
    job postings that are queried with either position titles, or keywords. 
    Emails a .csv report on average monthly starting salaries for these positions.
    """

    conn = db_connect(DB_NAME)

    print("Creating tables... ")

    sql_create_positions_table = open_sql_script("./src/db/create_positions.sql")
    db_create_table(conn, sql_create_positions_table)

    sql_create_keywords_table = open_sql_script("./src/db/create_keywords.sql")
    db_create_table(conn, sql_create_keywords_table)

    conn.close()

    print("Extracting Job Postings... ")
    positions_rows, keywords_rows = None, None
    # 2. 
    if DATA_POSITIONS or KEYWORDS:
        positions_rows, keywords_rows = extract_transform(positions=DATA_POSITIONS, keywords=KEYWORDS) 
    else:
        sys.exit("No position title or keywords provided. Add a wanted query to the variables.py")

    print("Rows have been extracted. ")
    # # 3. 
    # # clean and filter
    if positions_rows and FILTER_ENABLED:
        positions_rows = [row for row in positions_rows if str.__contains__(row[1], row[4])]

    # 4. Connect and populate DB
    # TODO: Refactor to populate the DB in batches, after every page is received

    if positions_rows:
        print("Populating positions... ")
        conn = db_connect(DB_NAME)
        db_populate(conn, positions_rows, "positions")

    if keywords_rows:
        print("Populating keywords... ") 
        conn = db_connect(DB_NAME)
        db_populate(conn, keywords_rows, "keywords")

    # 5. Extract averages, write to csv and email it
    print("Preparing the report... ")
    report = extract_averages()
    write_to_csv(report, OUTPUT_PATH)
    send_report(OUTPUT_PATH, RECIPIENT_EMAIL)

    print("Report sent. ")

if __name__ == "__main__":
    main()