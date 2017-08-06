# -*- coding: utf-8 -*-

from twitter_connect.create_session import CreateSession
from twitter_connect.get_timeline import GetTimeline
import configparser
import time
import json

if __name__ == '__main__':

    # watching text
    watch_text = ['写真', 'しゃしん', 'シャシン']
    # get session information
    filepath='session.conf'
    reader = configparser.SafeConfigParser()
    reader.read(filepath)
    param_account = {}
    param_connect = {}
    for i in reader.items('LoginConf'):
        param_account[i[0]] = i[1]
    for i in reader.items('Connection'):
        param_connect[i[0]] = i[1]

    # set param_connect
    if param_connect.get('get_timeline_delay') is None:
        param_connect['get_timeline_delay'] = 70
    if param_connect.get('reconnect_time') is None:
        param_connect['reconnect_time'] = 6

    # get the newest timeline-id if exist
    session = CreateSession(param_account).create_session()
    gettimeline = GetTimeline(session)
    res = gettimeline.get_timeline(count=1)
    if (res.status_code != 200):
        print("Err: http status is %s."%(res.status_code))
        exit(1)
    timeline = json.loads(res.text.decode('utf-8'))
    if len(timeline) == 1:
        tmp_since_id = timeline[0].get('id')
    if len(timeline) != 1 or tmp_since_id is None:
        tmp_since_id = ''
    # loop until killed
    while(True):
        # create session
        session = CreateSession(param_account).create_session()
        gettimeline = GetTimeline(session)
        for i in range(int(param_connect.get('reconnect_time'))):
            if tmp_since_id == "":
                res = gettimeline.get_timeline(count=20)
            else:
                res = gettimeline.get_timeline(count=20,
                                                    since_id=tmp_since_id)
            if (res.status_code != 200):
                print("Err: http status is %s."%(res.status_code))
                exit(1)
            timeline = json.loads(res.text.decode('utf-8'))
            watch_flag = False
            if(len(timeline)) != 0:
                tmp_status_code = timeline[0].get('id')
                for line in timeline:
                    for w in watch_text:
                        if w in line.get('text'):
                            watch_flag = True
                            break
                    if watch_flag:
                        break
                if watch_flag:
                    print('text found')
                else:
                    print('text not found')
                tmp_since_id=timeline[0]['id']
            time.sleep(int(param_connect.get('get_timeline_delay')))

