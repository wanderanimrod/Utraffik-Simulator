from time import time


class Clock():

    def __init__(self):
        self.__time_of_last_call = 0
        self.__stopped = False
        self.__start_time = 0

    def time_elapsed(self):
        time_now, time_elapsed = self.__get_time()
        self.__time_of_last_call = time_now
        return time_elapsed

    def now(self):
        time_now, _ = self.__get_time()
        return time_now - self.__start_time

    def start(self, at=None):
        if not at:
            at = time()
        self.__time_of_last_call = at
        self.__start_time = at
        self.__stopped = False
        return self

    def stop(self):
        self.__stopped = True

    def __get_time(self):
        if self.__stopped:
            return 0, 0
        time_now = time()
        time_elapsed = time_now - self.__time_of_last_call
        return time_now, time_elapsed
