from twitter_connect.create_streamer import CreateStreamer
import configparser
from datetime import datetime
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
    if param_connect.get('reconnect_streamer') is None:
        param_connect['reconnect_streamer'] = 600

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
        timeline = json.loads(line)
        text = timeline.get('text')
        if text is None:
            continue
        watch_flag = False
        for w in watch_text:
            if w in text:
                watch_flag = True
                break
        if watch_flag:
            print('text found')
        else:
            print('text not found')
        if (datetime.now() - tmp_time).total_seconds()\
                > int(param_connect.get('reconnect_streamer')):
            # create streamer
            streamer = CreateStreamer(param_account).create_streamer()
            if (streamer.status_code != 200):
                print("Err: http status is %s."%(res.status_code))
                exit(1)

            # memorize create_conn date
            tmp_time = datetime.now()

