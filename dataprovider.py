import time


class DataProvider(object):

    def __init__(self):
        self._data = open('data.txt', 'r').readlines()

    def getData(self):
        frame = int(time.time()) % len(self._data)
        return self._data[frame]
