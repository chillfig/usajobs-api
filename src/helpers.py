import os
import csv
import sys
from datetime import date
from typing import List

import sqlite3
from sqlite3 import Error

import requests
from requests.exceptions import HTTPError

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from variables import DB_NAME

## API Query functions


def api_call(query: str, params=None) -> dict:
    """
    Sends a GET request to the API with the provided parameters.
    Checks if the API is running properly.

    :param query str: Base query URL
    :param params dict: Parameters to be sent with the API request
    :return: dict from the JSON-response
    """
    headers = {
        "Host": "data.usajobs.gov",
        "User-Agent": os.getenv("USAJOBS_USERNAME"),
        "Authorization-Key": os.getenv("USAJOBS_API_KEY"),
    }

    try:
        response = requests.request("GET", query, params=params, headers=headers)

        if (
            response
            and response.status_code == 200
            and "application/hr+json" in response.headers.get("content-type")
        ):
            return response.json()
        else:
            sys.exit("Invalid API, non-JSON response. ")

    except HTTPError as http_err:
        print(f"HTTP Error: {http_err}")
    except Exception as err:
        print(f"Error: {err}")


def extract_date(date_str) -> str:
    return date_str.split("T")[0]


def get_salary_multiplier(rate_code: str) -> float:
    """
    Transforms the RemunerationIntervalCode to a float representing the fraction of the
    salary that is obtained per month

    :param rate_code str: RemunerationIntervalCode
    :return: float representing the multiplier
    """
    rates_multiplier = {
        "per year": 1 / 12,
        "per month": 1,
        "bi-weekly": 2,
        "per day": 22,  # average working days in a month
        "per hour": 168,  # working hours in a regular month
        "fee basis": 0,
        "piece work": 0,
        "student stipend paid": 0,
        "school year": 0,
        "without compensation": 0,
    }

    return list(map(lambda x: rates_multiplier[x], [rate_code]))[0]


## Reporting functions


def extract_averages() -> List[tuple]:
    """
    Executes the provided SQL script and returns the resulting rows.

    :return: List[tuple]
    """

    extract_script = open_sql_script("./src/db/data_averages.sql")

    conn = db_connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(extract_script)

    report = cur.fetchall()

    conn.commit()
    conn.close()

    return report


def write_to_csv(report: List[tuple], CSV_PATH: str):
    """
    Writes the provided list of tuples to a OUTPUT_PATH csv file.

    :param report List[tuple]: Report obtained from extract_averages()
    :param CSV_PATH str: Output path for the csv file
    :return: None
    """

    c = csv.writer(open(CSV_PATH, "w"))

    column_names = ["month", "position", "monthlySalary"]

    c.writerow(column_names)
    c.writerows(report)


def send_report(CSV_PATH, RECIPIENT_EMAIL):
    """
    Sends the CSV_PATH.csv file to the recipient email.

    :param CSV_PATH str: Path of the output csv file
    :param RECIPIENT_EMAIL str:
    """

    msg = MIMEMultipart()

    msg["From"] = os.getenv("SENDER_EMAIL")
    msg["To"] = RECIPIENT_EMAIL
    msg["Subject"] = "USA Jobs - Daily Report on Data Positions"

    body = "In the attachment you can find the daily .csv file containing average monthly salaries. "
    msg.attach(MIMEText(body, "plain"))

    filename = f"{date.today()} - Data jobs report.csv"
    attachment = open(CSV_PATH, "rb")
    p = MIMEBase("application", "octet-stream")
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header("Content-Disposition", "attachment; filename= %s" % filename)

    msg.attach(p)

    # If sender is using Gmail, make sure to enable less secure apps in Account Settings
    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()
    s.login(os.getenv("SENDER_EMAIL"), os.getenv("SENDER_PASS"))
    text = msg.as_string()
    s.sendmail(os.getenv("SENDER_EMAIL"), RECIPIENT_EMAIL, text)
    s.quit()


## Database functions


def db_connect(db_name: str):
    """
    Connects to a sqlite3 database with the provided name. Creates it if it does not exist.

    :param db_name str:
    :return: Database connection object
    """

    conn = None
    try:
        conn = sqlite3.connect(db_name)
        return conn
    except Error as e:
        print(e)

    return conn


def db_create_table(conn, table_name_script: str):
    """
    Creates the table with the provided table_name_script if it does not exist already.

    :param conn: DB connection object
    :param table_name str: SQL script to create the table with that name
    """

    try:
        cur = conn.cursor()
        cur.execute(table_name_script)
    except Error as e:
        print(e)


def db_populate(conn, rows, table):
    """
    Populates the table with the provided table name, by inserting the rows.

    :param conn: DB connection object
    :param rows List[tuple]: Rows to be inserted to the table. Equal in length to the number of columns of the table.
    :param table str: Name of the table to be populated
    """

    if table == "positions":
        cur = conn.executemany(
            "INSERT INTO positions VALUES (?, ?, ?, ?, ?, ?, ?, ?)", rows
        )
    elif table == "keywords":
        cur = conn.executemany(
            "INSERT INTO keywords VALUES (?, ?, ?, ?, ?, ?, ?, ?)", rows
        )

    conn.commit()
    conn.close()


def open_sql_script(sql_file_path: str) -> str:
    """
    Returns the imported SQL script.

    :param sql_file_path str: File to be imported as a string.
    :return: str of the whole provided SQL script
    """

    try:
        with open(sql_file_path, "r") as sql_file:
            script = sql_file.read()
            return script
    except Error as e:
        print(e)


def db_flush():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
    else:
        sys.exit("The database does not exist! ")
