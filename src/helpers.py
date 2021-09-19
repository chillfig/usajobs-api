import sqlite3
from sqlite3 import Error
import sys
import os 
import csv

import requests
from requests.exceptions import HTTPError

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from variables import DB_NAME, OUTPUT_PATH, RECIPIENT_EMAIL
from datetime import date

## API Query functions
## 
## 
## 

def api_call(query: str, params=None):

    headers = {"Host": 'data.usajobs.gov', 
               "User-Agent": os.getenv("USAJOBS_USERNAME"),
               "Authorization-Key": os.getenv("USAJOBS_API_KEY")
              }

    try:
        response = requests.request('GET', query, params=params, headers=headers)

        if response and response.status_code == 200 and 'application/hr+json' in response.headers.get('content-type'):
            return response.json()
        else: 
            sys.exit("Invalid API, non-JSON response. ")

    except HTTPError as http_err: 
        print(f"HTTP Error: {http_err}")
    except Exception as err:
        print(f"Error: {err}")


def extract_date(date_str) -> str:
    return date_str.split("T")[0]

def get_salary_multiplier(rate_code):

    rates_multiplier = {
        'per year': 1/12,
        'per month': 1,
        'bi-weekly': 2, 
        'per day': 22, # average working days in a month
        'per hour': 168, # working hours in a regular month
        'fee basis': 0, 
        'piece work': 0, 
        'student stipend paid': 0, 
        'school year': 0, 
        'without compensation': 0
        }

    return list(map(lambda x: rates_multiplier[x], [rate_code]))[0]

## Reporting functions 
## 
## 
## 

def extract_averages():
    """
    Returns:
        
    """
    
    extract_script = open_sql_script("./src/db/data_averages.sql")

    conn = db_connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(extract_script)

    report = cur.fetchall()
    
    conn.commit()
    conn.close()

    return report

def write_to_csv(report):
    c = csv.writer(open(OUTPUT_PATH,"w"))

    column_names = ["month", "position", "monthlySalary"]

    c.writerow(column_names)
    c.writerows(report)

def send_report(CSV_PATH, RECIPIENT_EMAIL):
    msg = MIMEMultipart()
    
    msg['From'] = os.getenv("SENDER_EMAIL")
    msg['To'] = RECIPIENT_EMAIL    
    msg['Subject'] = "USA Jobs - Daily Report on Data Positions"
    
    body = "In the attachment you can find the daily .csv file containing average monthly salaries. "
    msg.attach(MIMEText(body, 'plain'))
    
    filename = f"{date.today()} - Data jobs report.csv"
    attachment = open(CSV_PATH, "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(p)
    
    # If sender is using Gmail, make sure to enable less secure apps in Account Settings
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(os.getenv("SENDER_EMAIL"), os.getenv("SENDER_PASS"))
    text = msg.as_string()
    s.sendmail(os.getenv("SENDER_EMAIL"), RECIPIENT_EMAIL, text)
    s.quit()
        

## Database functions
##
## 
##

def db_connect(db_name):
    conn = None
    try:
        conn = sqlite3.connect(db_name)
        return conn
    except Error as e:
        print(e)

    return conn

def db_create_table(conn, table_name):
    try:
        cur = conn.cursor()
        cur.execute(table_name)
    except Error as e:
        print(e)

def db_populate(conn, rows, table):

    if table == "positions":
        cur = conn.executemany("INSERT INTO positions VALUES (?, ?, ?, ?, ?, ?, ?, ?)", rows)
    elif table == "keywords":
        cur = conn.executemany("INSERT INTO keywords VALUES (?, ?, ?, ?, ?, ?, ?, ?)", rows)

    conn.commit()
    conn.close()

def open_sql_script(sql_file_path):
    with open(sql_file_path, 'r') as sql_file:
        script = sql_file.read()
    return script

def db_flush():

    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
    else:
        print("The database does not exist! ")
