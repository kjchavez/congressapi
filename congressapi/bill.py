import requests
import HTMLParser
from congressapi import congress

_START_TAG = '<pre id="billTextContainer">'
_END_TAG = '</pre>'
def _extract_bill_text(html_content):
    idx = html_content.find(_START_TAG)
    if idx == -1:
        return "NOT FOUND"

    end_idx = html_content.find(_END_TAG, idx)
    if end_idx == -1:
        raise Exception("Malformed HTML content")

    escaped_text = html_content[idx+len(_START_TAG):end_idx]
    parser = HTMLParser.HTMLParser()
    return parser.unescape(parser.unescape(escaped_text))


class Bill(object):
    def __init__(self, data):
        assert 'bill_id' in data
        self.bill_id = data['bill_id']
        self.data = data

    def text(self):
        url = ""
        if 'congressdotgov_url' in self.data:
            url = self.data['congressdotgov_url'] + '/text'

        if not url:
            return ""

        r = requests.get(url)
        return _extract_bill_text(r.content)


def get_recent_bills(congress_num, chamber, action_type):
    """ Returns a list of Bill objects. """
    results = congress.recent_bills(congress_num, chamber, action_type)
    if not results:
        return []

    return [Bill(bill_data) for bill_data in results['bills']]
