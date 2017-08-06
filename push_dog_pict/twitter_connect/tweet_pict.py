# -*- coding: utf-8 -*-
import json

class TweetPict:
    """Getting Timeline using the session."""

    def __init__(self, session):
        self.session = session
        self.params = {}

    def tweet_pict(self, msg="", pict_path=""):
        url_for_media='https://upload.twitter.com/1.1/media/upload.json'
        url_for_tw='https://api.twitter.com/1.1/statuses/update.json'
        self.msg = msg
        # upload pict if pict_path is set.
        if pict_path != "":
            self.params['media'] = open(pict_path, "rb")
            # upload media
            res_for_pict = self.session.post(url_for_media,
                files={'media':self.params.get('media')})
            media_id=json.loads(res_for_pict.text).get('media_id')
            # tweet if upload is succeeded
            if res_for_pict.status_code == 200:
                res_for_tw = self.session.post(url_for_tw,
                        params = {'status':self.msg,
                            'media_ids':[media_id]})
            else:
                print('Error: media uploading failed.')
                exit(1)
        # tweet without media
        else:
            res_for_tw = self.session.post(url_for_tw,
                    params = {'status':self.msg})
        return res_for_tw

