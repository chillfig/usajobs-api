import pytest

import requests
from dotenv import load_dotenv
import os

from helpers import send_report

load_dotenv()

def test_api_response():
    # arrange
    headers = {"Host": 'data.usajobs.gov', 
               "User-Agent": os.getenv("USAJOBS_USERNAME"),
               "Authorization-Key": os.getenv("USAJOBS_API_KEY")
              }

    query_url = "https://data.usajobs.gov/api/Search?JobCategoryCode=2210"

    # act
    response = requests.request('GET', query_url, headers=headers)

    print(response.json())
    # assert
    assert response.status_code == 200
    # assert something else

def test_query_codelist():
    pass


def test_send_report():
    pass


    # send_report()