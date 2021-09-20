# USA Jobs API 

[API Reference](https://developer.usajobs.gov/API-Reference)

This repo contains a script that queries the USA Jobs API for Data positions, and send a .csv report with monthly average salaries of these positions. In comparison, it also queries for positions with related keywords. 

Both the positions and keywords can be changed in the variables.py

Each positions/keyword sends its own GET request to the API. 

In addition, considering that querying e.g. for a Data Analyst results in many Job Postings that don't seem to be an actual Data Analyst position, the variables.py script contains a flag for filtering these situations, only returning those Job Postings that contain the query "Data Analyst" in the Position Title. 

Same applies for the keywords. 

## Instructions to run

```
$ cd usajobs
$ python -m venv usajobs-venv
$ source usajobs-venv/bin/activate
$ pip install -r requirements.txt
```

Create a `.env` file with the following environment variables. 

- USAJOBS_API_KEY
- USAJOBS_USERNAME
- SENDER_EMAIL
- SENDER_PASS
- RECIPIENT_EMAIL

The script can be run with the following command, while the `virtualenv` is activated and the current working directory is usajobs repo:

```
$ python src/main.py
```

Or, it can be turned into a daily cron job (daily at 7AM), by adding it to the end of the file after running `$ crontab -e`

```
0 7 * * * source ./usajobs.sh  > ~/usajobs/cronlog.txt
```

## TODO

> Test, test, test!

> ~~Documentation of functions~~

> Add the paygrade to the report .csv

> ~~Instead of using the variables.py, add paramaters to the call of the script (python src/main.py -p "Data Scientist" -k "analytics")~~

> ~~compare with the average starting salary of a general data-related job -> add these rows to the query and CSV~~

> Is there a meaningful difference between starting salaries of Data Jobs in
different government organisations?

> Catch potential errors

> Populate the DB in batches (pages)

> If the query is different from what the database currently has, flush the DB, and restart. 

## Questions

1. Is it supposed to be only one .csv file that makes up the report? And in it, all three different comparisons are shown? 
2. RemunerationRate Interval Codes - since we're talking about monthly salaries, is an Interval Code 'Piece Work' or 'Student Stipend Paid' relevant? Exclude these from the search?