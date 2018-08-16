# -*- coding: utf-8 -*-

from twitter_connect.create_streamer import CreateStreamer
from twitter_connect.tweet_pict import TweetPict
from twitter_connect.create_session import CreateSession
from twitter_connect.get_timeline import GetTimeline
from pi_camera.exec_picamera import ExecPicamera
import configparser
from datetime import datetime
import json
import subprocess
import time

def post_photo(msg='', pict_path=''):
    session = CreateSession(param_account).create_session()
    TW = TweetPict(session)
    tweet = TW.tweet_pict(msg,pict_path)
    if(tweet.status_code != 200):
        print('Err: error while push photo:%s'%tweet.status_code)

def post_movie(msg='', movie_path=''):
    session = CreateSession(param_account).create_session()
    TW = TweetPict(session)
    tweet = TW.tweet_movie(msg,movie_path)
    if(tweet.status_code != 200):
        print('Err: error while push photo:%s'%tweet.status_code)

if __name__ == '__main__':
    # watching text for photo
    watch_text_photo = ['写真', 'しゃしん', 'シャシン', 'photo']
    # watching text for movie
    watch_text_movie = ['動画', 'どうが', 'ドウガ', 'movie']
    # get session information
    filepath='session.conf'
    reader = configparser.SafeConfigParser()
    reader.read(filepath)
    param_account = {}
    param_connect = {}
    param_camera = {}
    for i in reader.items('LoginConf'):
        param_account[i[0]] = i[1]
    for i in reader.items('Connection'):
        param_connect[i[0]] = i[1]
    for i in reader.items('CameraSettings'):
        param_camera[i[0]] = i[1]
    # set movie_time if it's not set (default: 5sec)
    if param_camera.get('movie_time') is None:
        param_camera['movie_time'] = 5

    # set param_connect
    if param_connect.get('get_timeline_delay') is None:
        param_connect['get_timeline_delay'] = 70
    if param_connect.get('reconnect_time') is None:
        param_connect['reconnect_time'] = 6

    # create camera
    import picamera
    camera_init = picamera.PiCamera()

    # get the newest timeline-id if exist
    session = CreateSession(param_account).create_session()
    gettimeline = GetTimeline(session)
    for i in range(int(param_connect.get('reconnect_time'))):
        res = gettimeline.get_timeline(count=1)
        if (res.status_code == 200):
            break
        print("Retry for the first connect.")
        time.sleep(int(param_connect.get('get_timeline_delay')))
    if (res.status_code != 200):
        print("Err: http status is %s."%(res.status_code))
        exit(1)
    timeline = json.loads(res.text)
    if len(timeline) == 1:
        tmp_since_id = timeline[0].get('id')
    elif len(timeline) != 1 or tmp_since_id is None:
        tmp_since_id = ''

    # loop until killed
    while True:
        # create session
        session = CreateSession(param_account).create_session()
        gettimeline = GetTimeline(session)
        if tmp_since_id == "":
            res = gettimeline.get_timeline(count=20)
        else:
            res = gettimeline.get_timeline(count=20,
                                           since_id=tmp_since_id)
        # wait for the next iter if status_code is illegal
        if (res.status_code != 200):
            print("Err: http status is %s."%(res.status_code))
            print("Sleep for the sleeping time.")
            time.sleep(int(param_connect.get('get_timeline_delay')))
            continue

        timeline = json.loads(res.text)
        if len(timeline) == 0:
            print("Sleep before the next read.")
            time.sleep(int(param_connect.get('get_timeline_delay')))
            continue

        # renew the newest id
        tmp_since_id = timeline[0].get('id')

        for tm in timeline:
            text = tm.get('text')

            if text is None:
                time.sleep(int(param_connect.get('get_timeline_delay')))
                continue

            # check if there's words for photo
            watch_flag_photo = False
            for w in watch_text_photo:
                if w in text:
                    watch_flag_photo = True
                    break
            # taking a picture if some words exist.
            if watch_flag_photo:
                camera = ExecPicamera(camera_init,param_camera)
                filename = datetime.today().strftime("%Y%m%d_%H%M%S")
                camera.take_pict('photo/' + filename + '.jpg')
                post_photo(filename, 'photo/' + filename + '.jpg')
                rm = subprocess.call(['rm', 'photo/' + filename + '.jpg'])

            # check if there's words for movie
            watch_flag_movie = False
            for w in watch_text_movie:
                if w in text:
                    watch_flag_movie = True
                    break
            # taking a movie if some words exist.
            if watch_flag_movie:
                camera = ExecPicamera(camera_init,param_camera)
                filename = datetime.today().strftime("%Y%m%d_%H%M%S")
                camera.take_movie('movie/' + filename + '.h264',
                            param_camera.get('movie_time'))
                conv = subprocess.call(['/usr/bin/MP4Box', '-fps', '20',
                           '-add', 'movie/' + filename + '.h264',
                           'movie/' + filename + '.mp4'])
                post_movie(filename, 'movie/' + filename + '.mp4')
                rm = subprocess.call(['rm', 'movie/' + filename + '.mp4'])
                rm2 = subprocess.call(['rm', 'movie/' + filename + '.h264'])

            # check if it needs to go to the next iter
            if watch_flag_photo or watch_flag_movie:
                print("Finished output files")
                break

        # sleep afterall
        print("sleep before the next check")
        time.sleep(int(param_connect.get('get_timeline_delay')))

