BASE_URL = "https://api.propublica.org/congress/v1/"
ENV_VAR = 'PROPUBLICA_CONGRESS_API_KEY'

class Chamber(object):
    SENATE = "senate"
    HOUSE = "house"
    BOTH = "both"

class BillAction(object):
    INTRODUCED = "introduced"
    UPDATED = "updated"
    PASSED = "passed"
    MAJOR = "major"
