import sqlite3

from variables import DB_NAME
from helpers import *
from etl import *


def main(DATA_POSITIONS, KEYWORDS, FILTER_ENABLED, OUTPUT_PATH, RECIPIENT_EMAIL):
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
        positions_rows, keywords_rows = extract_transform(
            positions=DATA_POSITIONS, keywords=KEYWORDS
        )
    else:
        sys.exit(
            "No position title or keywords provided. Add a wanted query to the variables.py"
        )

    print("Rows have been extracted. ")
    # # 3.
    # # clean and filter
    if positions_rows and FILTER_ENABLED:
        positions_rows = [
            row for row in positions_rows if str.__contains__(row[1], row[4])
        ]

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

    return print("Report sent. ")


if __name__ == "__main__":

    import argparse

    ap = argparse.ArgumentParser()

    ap.add_argument(
        "-p",
        "--positions",
        required=False,
        help="Position Titles to be queried. Wrap with '', separate with semicolon (;)! Example: -p 'Data Scientist;Data Analyst'",
    )
    ap.add_argument(
        "-k",
        "--keywords",
        required=False,
        help="Keywords to be queried. Wrap with '', separate with semicolon (;)! Example: -k 'data;analytics'",
    )

    ap.add_argument("--filter", dest="filter_positions", action="store_true")
    ap.add_argument("--no-filter", dest="filter_positions", action="store_false")

    ap.add_argument(
        "-o", "--output", required=False, help="Path for the output .csv file. "
    )
    ap.add_argument(
        "-r",
        "--recipient",
        required=False,
        help="Email of the recipient of the report csv file. If not provided, it will look at the .env file for the 'RECIPIENT_EMAIL' environment variable. ",
    )

    ap.set_defaults(
        filter_positions=False,
        positions="Data Scientist;Data Analyst;Data Engineer",
        keywords="data;analytics;analysis",
        output="report.csv",
        recipient=os.getenv("RECIPIENT_EMAIL"),
    )

    args = vars(ap.parse_args())

    DATA_POSITIONS = args["positions"].split(";") if args["positions"] else None
    KEYWORDS = args["keywords"].split(";") if args["keywords"] else None
    FILTER_ENABLED = args["filter_positions"]

    OUTPUT_PATH = args["output"]
    RECIPIENT_EMAIL = args["recipient"]

    # print(DATA_POSITIONS, KEYWORDS, FILTER_ENABLED, OUTPUT_PATH, RECIPIENT_EMAIL)
    main(DATA_POSITIONS, KEYWORDS, FILTER_ENABLED, OUTPUT_PATH, RECIPIENT_EMAIL)
