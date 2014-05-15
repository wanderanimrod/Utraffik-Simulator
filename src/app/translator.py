from copy import copy
from app.events.events import E_TRANSLATOR_WAITING, E_END_OF_JOURNEY


class Translator:

    def __init__(self, edges):
        self.edges = edges
        self.__translatables = self.__get_vehicles()
        self.__check_translation_load()
        self.last_sweep_time = 0
        E_END_OF_JOURNEY.connect(self.__end_of_journey_listener)

    def sweep(self, sim_time):
        time_delta = sim_time - self.last_sweep_time
        for vehicle in copy(self.__translatables):
            vehicle.translate(time_delta)

        self.last_sweep_time = sim_time
        self.__check_translation_load()

    def __get_vehicles(self):
        vehicles = []
        for edge in self.edges:
            if edge.vehicles():
                vehicles.extend(edge.vehicles())
        return vehicles

    def __check_translation_load(self):
        if not self.__translatables:
            E_TRANSLATOR_WAITING.send(sender=self)

    def __end_of_journey_listener(self, sender, **kwargs):
        """ All vehicles in a process will belong to that process' translator. Since there is one translator per
            process, there is no chance that the vehicle wont belong to this translator
        """
        self.__translatables.remove(sender)