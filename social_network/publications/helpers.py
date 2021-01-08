import clearbit
import requests
import os
from requests.exceptions import HTTPError

def get_clearbit_data(email):
    try:
        clearbit.key = os.environ['CLEARBIT_API_KEY']
        r = clearbit.Enrichment.find(email=email)
        return {'first_name': r['person']['name']['givenName'],
                'last_name': r['person']['name']['familyName']}
    except (HTTPError, KeyError):
        return {'first_name': '', 'last_name': ''}


def is_existent_email(email):
    """
    Hunter is designed to contact other professionals. 
    gmail.com is used to create personal email addresses 
    so it don't perform the verification.
    """
    api_key = os.environ['HUNTERIO_API_KEY']
    url = f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={api_key}"
    try:
        r = requests.get(url)
        score = r.json()['data']['score']
        if score == 0:  # It will be 50 for gmail and other webmail.
            return False
    except requests.exceptions.RequestException as e:
        raise e
    
    return True
