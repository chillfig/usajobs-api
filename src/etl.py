import sqlite3
from sqlite3 import Error
# import os

from helpers import api_call, extract_date, get_salary_multiplier
from variables import RESULTS_PER_PAGE_LIMIT


def extract_transform(positions=None, keywords=None):
    """
    Queries the USAJOBS API for each individual position and/or keyword,
    returns array of tuple-positions with specific attributes.

    :param List[str] positions: Position Titles to be queried
    :param List[str] keywords: Keywords to be queried
    :return: List, List of job position tuples

    """
    query_url = f"https://data.usajobs.gov/api/Search?"

    params = {"ResultsPerPage": RESULTS_PER_PAGE_LIMIT}

    positions_rows = []
    if positions and isinstance(positions, list):    

        for position_title in positions:
            params["PositionTitle"] = position_title 

            json_response_first_page = api_call(query_url, params=params)
            if json_response_first_page:
                
                first_page_content = json_response_first_page["SearchResult"]["SearchResultItems"]
                first_page_values = get_values(first_page_content, position_title)

                # Add the first page job postings to the rows
                positions_rows += first_page_values
                # Extract the number of pages this PositionTitle has
                page_count = int(json_response_first_page["SearchResult"]["UserArea"]["NumberOfPages"])

                for page in range(2, page_count + 1):
                    params["Page"] = page

                    page_json_response = api_call(query_url, params=params)
                    if page_json_response:
                        page_content = page_json_response["SearchResult"]["SearchResultItems"]
                        # Add the current page job postings
                        positions_rows += get_values(page_content, position_title)

            # Refresh Page# for next position
            params["Page"] = 1

    # Refresh params
    params = {"ResultsPerPage": RESULTS_PER_PAGE_LIMIT}

    keywords_rows = []
    if keywords and isinstance(keywords, list):

        for kw in keywords:
            params["Keyword"] = kw
            json_response_first_page = api_call(query_url, params=params)

            if json_response_first_page:
                
                first_page_content = json_response_first_page["SearchResult"]["SearchResultItems"]
                first_page_values = get_values(first_page_content, kw)

                # Add the first page job postings to the rows
                keywords_rows += first_page_values

                # Extract the number of pages this PositionTitle has
                page_count = int(json_response_first_page["SearchResult"]["UserArea"]["NumberOfPages"])

                for page in range(2, page_count + 1):
                    params["Page"] = page

                    page_json_response = api_call(query_url, params=params)
                    if page_json_response:
                        page_content = page_json_response["SearchResult"]["SearchResultItems"]
                        # Add the current page job postings
                        keywords_rows += get_values(page_content, kw)

            # Refresh Page# for next position
            params["Page"] = 1


    return positions_rows, keywords_rows
    

def get_values(content: dict, query: str):

    values = []
    for item in content:
        descriptor = item.get("MatchedObjectDescriptor")

        _id = item.get("MatchedObjectId")
        _title = descriptor.get("PositionTitle")
        _orgName = descriptor.get("OrganizationName")
        _publishDate = extract_date(descriptor.get("PositionStartDate"))

        _query = query

        remuneration = descriptor.get("PositionRemuneration")[0]
        _startSalary = remuneration.get("MinimumRange")
        _salaryInterval = remuneration.get("RateIntervalCode")
        _salaryMultiplier = get_salary_multiplier(_salaryInterval.lower())

        values.append((_id, _title, _orgName, _publishDate, _query, _startSalary, _salaryInterval, _salaryMultiplier))

    return values
