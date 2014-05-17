from time import time


class Clock():

    def __init__(self):
        self.__time_of_last_call = 0
        self.__stopped = False

    def time_elapsed(self):
        if self.__stopped:
            return 0
        time_now = time()
        time_elapsed = time_now - self.__time_of_last_call
        self.__time_of_last_call = time_now
        return time_elapsed

    def start(self):
        self.__time_of_last_call = time()
        self.__stopped = False
        return self

    def stop(self):
        self.__stopped = True