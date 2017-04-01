"""
    Lightweight wrapper around the ProPublica Congress API.

    NOTICE: If you are using Python 2.7.6, you may encounter SSL errors with
    the 'requests' module. You should either upgrade to 2.7.9 (if possible) or
    downgrade the 'requests' module to 2.5.3

    pip install requests==2.5.3
"""
from enum import Enum
import requests
import os
import logging
import itertools

class Chamber(Enum):
    SENATE = 1
    HOUSE = 2

    @staticmethod
    def tostring(chamber):
        if chamber == Chamber.SENATE:
            return "senate"
        elif chamber == Chamber.HOUSE:
            return "house"
        return ""

class BillAction(object):
    INTRODUCED = "introduced"
    UPDATED = "updated"
    PASSED = "passed"
    MAJOR = "major"

class CongressApi(object):
    BASE_URL = "https://api.propublica.org/congress/v1/"
    ENV_VAR = 'PROPUBLICA_CONGRESS_API_KEY'

    def __init__(self, api_key=None):
        self.headers = {}
        if api_key is None:
            if not CongressApi.ENV_VAR in os.environ:
                raise Exception("%s not found in env." % CongressApi.ENV_VAR)

            api_key = os.environ[CongressApi.ENV_VAR]

        self.headers['X-API-Key'] = api_key


    def get(self, url_suffix):
        """ Get data from arbitrary endpoint of Congress API.

        This is available for maximum flexibility, but you will usually want to
        use one of the other, strongly-typed functions.

        Returns:
            If request succeeds, JSON result.
            If request fails, logs error and returns None.
        """
        url = CongressApi.BASE_URL+url_suffix
        logging.debug("GET url: " + url)
        response = requests.get(url, headers=self.headers)
        json_res = response.json()
        if json_res['status'] == 'OK' and 'results' in json_res:
            return json_res['results']
        logging.warning("CongressApi GET failed: " + json_res['status'])
        return None

    def members(self, congress_num, chamber):
        assert isinstance(chamber, Chamber)
        assert isinstance(congress_num, int)
        suffix = "%d/%s/members.json" % \
                (congress_num, Chamber.tostring(chamber))
        return self.get(suffix)

    def member(self, member_id):
        """ Returns a profile for specific member as dictionary. """
        suffix = "members/%s.json" % member_id
        return self.get(suffix)[0]

    def member_votes(self, member_id):
        """ Returns most recent vote positions for a specific member. """
        suffix = "members/%s/votes.json" % member_id
        return self.get(suffix)

    def vote_roll_call(self, congress_num, chamber, session, roll_call_num):
        assert isinstance(chamber, Chamber)
        assert isinstance(congress_num, int)
        assert isinstance(roll_call_num, int)
        assert session in (1, 2)
        suffix = "%d/%s/sessions/%d/votes/%d.json" % (congress_num, \
                Chamber.tostring(chamber), session, roll_call_num)
        return self.get(suffix)

    def recent_bills(self, congress_num, chamber, action_type):
        suffix = "%d/%s/bills/%s.json" % (congress_num, \
                Chamber.tostring(chamber), action_type)
        return self.get(suffix)

    def recent_bills_by_member(self, member_id, action_type):
        suffix = "members/%s/bills/%s.json" % (member_id, action_type)
        return self.get(suffix)

    def bill(self, congress_num, bill_id):
        suffix = "%d/bills/%s.json" % (congress_num, bill_id)
        return self.get(suffix)[0]

