# -*- coding: utf-8 -*-
import json
import os.path

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

    def tweet_movie(self, msg="", movie_path=""):
        url_for_media='https://upload.twitter.com/1.1/media/upload.json'
        url_for_tw='https://api.twitter.com/1.1/statuses/update.json'
        self.msg = msg
        # upload movie if movie_path is set.
        if movie_path != "":
            self.params['media'] = open(movie_path, "rb")
            # upload media
            ## 1. init uploading media
            res_init = self.session.post(url_for_media,
                                 params={'command':'INIT',
                                         'media_type':'video/mp4',
                                         'total_bytes':os.path.getsize(movie_path)})
            if(res_init.status_code != 202):
                print("Err: movie-init failed(%s)"%(res_init.status_code))
                exit(1)
            else:
                media_id=json.loads(res_init.text).get('media_id')
            ## 2. appand media
            res_append = self.session.post(url_for_media,
                                 params={'command':'APPEND',
                                         'media_id':media_id,
                                         'segment_index':0},
                                 files={'media':self.params.get('media')})
            if(res_append.status_code != 204):
                print("Err: movie-append failed(%s)"%(res_init.status_code))
                exit(1)
            ## 3. finalize
            res_finalize = self.session.post(url_for_media,
                                 params={'command':'FINALIZE',
                                         'media_id':media_id})
            # tweet if upload is succeeded
            if res_finalize.status_code == 201:
                res_for_tw = self.session.post(url_for_tw,
                        params = {'status':self.msg,
                            'media_ids':[media_id]})
            else:
                print("Error: media uploading failed(%s)."%
                                                     (res_finalize.status_code))
                exit(1)
        # tweet without media
        else:
            res_for_tw = self.session.post(url_for_tw,
                    params = {'status':self.msg})
        return res_for_tw

