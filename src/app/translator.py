from copy import copy

from app.events.events import E_END_OF_JOURNEY


class Translator:

    def __init__(self, edges):
        self.edges = edges
        self._translatables = self._get_vehicles()
        self.is_waiting = False
        self._check_load()
        E_END_OF_JOURNEY.connect(self._end_of_journey_listener)

    def sweep(self, clock):
        time_delta = clock.time_elapsed()
        time_now = clock.now()
        for vehicle in copy(self._translatables):
            vehicle.translate(time_delta*5, time_now)
        self._check_load()

    def _get_vehicles(self):
        vehicles = []
        for edge in self.edges:
            if edge.vehicles():
                vehicles.extend(edge.vehicles())
        return vehicles

    def _check_load(self):
        if not self._translatables:
            self.is_waiting = True

    def _end_of_journey_listener(self, sender, **_):
        """ All vehicles in a process will belong to that process' translator. Since there is one translator per
            process, there is no chance that the vehicle wont belong to this translator
        """
        self._translatables.remove(sender)