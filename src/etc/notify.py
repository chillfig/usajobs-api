import os
from dotenv import load_dotenv
load_dotenv()

import requests

from twilio.rest import Client


def main():
    headers = {"Host": 'data.usajobs.gov', 
               "User-Agent": os.getenv("USAJOBS_USERNAME"),
               "Authorization-Key": os.getenv("USAJOBS_API_KEY")
              }

    query_url = f"https://data.usajobs.gov/api/Search?"

    params = {"ResultsPerPage": 10, 
              "PositionTitle": "Data Analyst"}

    response = requests.request('GET', query_url, params=params, headers=headers)

    if response and response.status_code == 200 and 'application/hr+json' in response.headers.get('content-type'):
        # Send whatsapp msg
        print('application/hr+json' in response.headers.get('content-type'))
        print(response.headers.get("content-type"))
        client = Client()
        from_whatsapp_number=f"whatsapp:{os.getenv("TWILIO_FROM")}"
        to_whatsapp_number=f"whatsapp:{os.getenv("TWILIO_TO")}"
        client.messages.create(body='The USA Jobs website is back up and running. Time to get back to work. ',
                            from_=from_whatsapp_number,
                            to=to_whatsapp_number)
        print("Msg sent. ")
    else:
        return print("Unsuccesful")

if __name__ == "__main__":
    main()