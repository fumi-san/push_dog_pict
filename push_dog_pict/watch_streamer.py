# -*- coding: utf-8 -*-

from twitter_connect.create_streamer import CreateStreamer
from twitter_connect.tweet_pict import TweetPict
from twitter_connect.create_session import CreateSession
from pi_camera.exec_picamera import ExecPicamera
import configparser
from datetime import datetime
import json
import subprocess

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
    if param_connect.get('reconnect_streamer') is None:
        param_connect['reconnect_streamer'] = 600

    # create camera
    import picamera
    camera_init = picamera.PiCamera()

    # create streamer
    streamer = CreateStreamer(param_account).create_streamer()
    if (streamer.status_code != 200):
        print("Err: http status is %s."%(res.status_code))
        exit(1)

    # memorize create_conn date
    tmp_time = datetime.now()

    # loop until killed
    for line in streamer.iter_lines():
        if(len(line) == 0):
            continue
        timeline = json.loads(line.decode('utf-8'))
        text = timeline.get('text')
        if text is None:
            continue

        # check if there's words for photo
        watch_flag = False
        for w in watch_text_photo:
            if w in text:
                watch_flag = True
                break
        # taking a picture if some words exist.
        if watch_flag:
            camera = ExecPicamera(camera_init,param_camera)
            filename = datetime.today().strftime("%Y%m%d_%H%M%S")
            camera.take_pict('photo/' + filename + '.jpg')
            post_photo(filename, 'photo/' + filename + '.jpg')

        # check if there's words for movie
        watch_flag = False
        for w in watch_text_movie:
            if w in text:
                watch_flag = True
                break
        # taking a movie if some words exist.
        if watch_flag:
            camera = ExecPicamera(camera_init,param_camera)
            filename = datetime.today().strftime("%Y%m%d%_H%M%S")
            camera.take_movie('movie/' + filename + '.h264',
                        param_camera.get('movie_time'))
            conv = subprocess.call(['/usr/bin/MP4Box', '-fps', '20',
                       '-add', 'movie/' + filename + '.h264',
                       'movie/' + filename + '.mp4'])
            post_movie(filename, 'movie/' + filename + '.mp4')

        # refresh the connection if time is over.
        if (datetime.now() - tmp_time).total_seconds()\
                > int(param_connect.get('reconnect_streamer')):
            # create streamer
            streamer = CreateStreamer(param_account).create_streamer()
            if (streamer.status_code != 200):
                print("Err: http status is %s."%(res.status_code))
                exit(1)

            # memorize create_conn date
            tmp_time = datetime.now()

