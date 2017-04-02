import env
from congressapi import congress
from congressapi.constants import *

def test_members():
    mem = congress.members(115, Chamber.SENATE)
    assert mem is not None

def test_member():
    kelly = congress.member('K000388')
    assert kelly['first_name'] == "Trent"

def test_member_votes():
    votes = congress.member_votes('K000388')
    assert len(votes) > 0

def test_recent_bills():
    bills = congress.recent_bills(115, Chamber.SENATE, BillAction.INTRODUCED)
    assert bills is not None

def test_bill():
    bill = congress.bill(115, 's798')
    assert bill['bill_id'] == 's798-115', bill
