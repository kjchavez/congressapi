"""
    Lightweight wrapper around the ProPublica Congress API.

    NOTICE: If you are using Python 2.7.6, you may encounter SSL errors with
    the 'requests' module. You should either upgrade to 2.7.9 (if possible) or
    downgrade the 'requests' module to 2.5.3

    pip install requests==2.5.3
"""
from datetime import datetime
import itertools
import logging
import os
import requests

from congressapi.constants import *

class Headers(object):
    _value = {}

    @staticmethod
    def set(hdr, value):
        Headers._value[hdr] = value

    @staticmethod
    def all():
        return Headers._value

def set_api_key(api_key=None):
    if not api_key:
        if ENV_VAR in os.environ:
            api_key = os.environ[ENV_VAR]
        else:
            logging.warning("Could not find environment variable: %s", ENV_VAR)
            return

    Headers.set('X-API-Key', api_key)

def _get(url_suffix):
    """ Get data from arbitrary endpoint of Congress API.

    This is available for maximum flexibility, but you will usually want to
    use one of the other, strongly-typed functions.

    Returns:
        If request succeeds, JSON result.
        If request fails, logs error and returns None.
    """
    url = BASE_URL+url_suffix
    logging.debug("GET url: " + url)
    response = requests.get(url, headers=Headers.all())
    json_res = response.json()
    if json_res['status'] == 'OK' and 'results' in json_res:
        return json_res['results']
    logging.warning("CongressApi GET failed: " + json_res['status'])
    return None

def members(congress_num, chamber):
    suffix = "%d/%s/members.json" % \
            (congress_num, chamber)
    return _get(suffix)

def member(member_id):
    """ Returns a profile for specific member as dictionary. """
    suffix = "members/%s.json" % member_id
    return _get(suffix)[0]

def member_votes(member_id):
    """ Returns most recent vote positions for a specific member. """
    suffix = "members/%s/votes.json" % member_id
    return _get(suffix)

def vote_roll_call(congress_num, chamber, session, roll_call_num):
    assert session in (1, 2)
    suffix = "%d/%s/sessions/%d/votes/%d.json" % (congress_num, \
            chamber, session, roll_call_num)
    return _get(suffix)

def recent_bills(congress_num, chamber, action_type):
    suffix = "%d/%s/bills/%s.json" % (congress_num, \
            chamber, action_type)
    return _get(suffix)[0]

def recent_bills_by_member(member_id, action_type):
    suffix = "members/%s/bills/%s.json" % (member_id, action_type)
    return _get(suffix)

def bill(congress_num, bill_id):
    suffix = "%d/bills/%s.json" % (congress_num, bill_id)
    return _get(suffix)[0]

def current_congress():
    """ Returns the number of current congress based on date. """
    now = datetime.now()
    year = now.year

    # Reference point is that the 115th Congress started in 2017.
    # Each session runs for 2 years from January 3rd to January 3rd.
    current_congress =  115 + (year - 2017) // 2
    if now.month == 1 and now.day < 3:
        current_congress -= 1

    return current_congress
