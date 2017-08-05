# -*- coding: utf-8 -*-

class GetTimeline:
    """Getting Timeline using the session."""

    def __init__(self, session=None):
        if session == None:
            print("Error: session isn't defined")
            exit(1)
        self.session = session
        self.params = {}

    def get_timeline(self, count=20, since_id=""):
        url='https://api.twitter.com/1.1/statuses/home_timeline.json'
        if isinstance(count, int):
            self.params['count'] = count
        else:
            print("Error: timeline count isn't int.")
            exit(1)
        if since_id != "":
            self.params['since_id'] = since_id
        req=self.session.get(url, params = self.params)
        return req

