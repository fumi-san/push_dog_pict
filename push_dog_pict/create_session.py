# -*- coding: utf-8 -*-

class CreateSession:
    """Creating a session to the twitter account."""

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

    def create_session(self):
        from requests_oauthlib import OAuth1Session
        session = OAuth1Session(
            self.param_account.get('CK'),
            self.param_account.get('CS'),
            self.param_account.get('AT'),
            self.param_account.get('AS')
            )
        return session

