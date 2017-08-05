# -*- coding: utf-8 -*-

from requests_oauthlib import OAuth1
import requests


class CreateStreamer:
    """Create streaming timeline."""

    def __init__(self,params={}):
        self.param_account = {
            'CK' : params.get("consumer_key"),
            'CS' : params.get("consumer_secret"),
            'AT' : params.get("access_token"),
            'AS' : params.get("access_token_secret")
        }
        for i in self.param_account:
            if self.param_account[i] is None:
                print("Error: Some parameter for login is None.")
                exit(1)

    def create_streamer(self):
        auth = OAuth1(
            self.param_account.get('CK'),
            self.param_account.get('CS'),
            self.param_account.get('AT'),
            self.param_account.get('AS')
        )
        url="https://userstream.twitter.com/1.1/user.json"
        streamer = requests.get(url,auth=auth,stream=True)
        return streamer

