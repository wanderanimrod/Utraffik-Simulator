from copy import copy

from app.events.events import E_END_OF_JOURNEY


class Translator:

    def __init__(self, edges):
        self.edges = edges
        self.__translatables = self.__get_vehicles()
        self.is_waiting = False
        self.__check_load()
        E_END_OF_JOURNEY.connect(self.__end_of_journey_listener)

    def sweep(self, clock):
        time_delta = clock.time_elapsed()
        time_now = clock.now()
        for vehicle in copy(self.__translatables):
            vehicle.translate(time_delta, time_now)
        self.__check_load()

    def __get_vehicles(self):
        vehicles = []
        for edge in self.edges:
            if edge.vehicles():
                vehicles.extend(edge.vehicles())
        return vehicles

    def __check_load(self):
        if not self.__translatables:
            self.is_waiting = True

    def __end_of_journey_listener(self, sender, **_):
        """ All vehicles in a process will belong to that process' translator. Since there is one translator per
            process, there is no chance that the vehicle wont belong to this translator
        """
        self.__translatables.remove(sender)