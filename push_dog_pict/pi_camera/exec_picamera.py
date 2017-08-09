# -*- coding: utf-8 -*-
import picamera

class ExecPicamera:
    """Executing camera-module method."""

    def __init__(self,camera, params={}):
        # get parameters
        self.params = {}
        for i in params:
            self.params[i[0]] = i[1]
        self.camera = camera

    def take_pict(self, filename):
        # create Camera object
#        self.camera = picamera.PiCamera()
        self.camera.capture(filename)

    def take_movie(self, filename, time):
#        self.camera = picamera.PiCamera()
        self.camera.start_recording(filename)
        self.camera.wait_recording(int(time))
        self.camera.stop_recording()
