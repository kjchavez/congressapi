from congressapi import congress

class Member(object):
    def __init__(self, data):
        self.data = data

    def full_name(self):
        names = [self.data['first_name'], self.data['middle_name'], \
                 self.data['last_name']]

        return ' '.join(name for name in names if name)


def get_member(member_id):
    member_data = congress.member(member_id)
    if member_data:
        return Member(member_data)

    return None
