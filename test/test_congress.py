import env
from congressapi.congress import *

api = CongressApi()

def test_members():
    mem = api.members(115, Chamber.SENATE)
    assert mem is not None

def test_member():
    kelly = api.member('K000388')
    assert kelly['first_name'] == "Trent"

def test_member_votes():
    votes = api.member_votes('K000388')
    assert len(votes) > 0

def test_recent_bills():
    bills = api.recent_bills(115, Chamber.SENATE, BillAction.INTRODUCED)
    assert bills is not None

def test_bill():
    bill = api.bill(115, 's798')
    assert bill['bill_id'] == 's798-115', bill
