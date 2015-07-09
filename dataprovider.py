import time
import cv2


class DataProvider(object):

    def __init__(self):
        self._data = cv2.VideoCapture(0)

    def __del__(self):
        self._data.release()

    def getData(self):
        success, image = self._data.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
