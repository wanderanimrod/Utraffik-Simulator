from app.events.events import E_TRANSLATOR_WAITING


class Translator:

    def __init__(self, edges):
        self.edges = edges
        self.vehicles = self.__get_vehicles()
        self.__translatables = self.vehicles
        self.__check_translation_load()
        self.last_sweep_time = None

    def sweep(self, sim_time):
        if self.last_sweep_time:
            time_delta = sim_time - self.last_sweep_time
        else:
            time_delta = sim_time
        for vehicle in self.__translatables:
            vehicle.translate(time_delta)
        self.last_sweep_time = sim_time

    def __get_vehicles(self):
        vehicles = []
        for edge in self.edges:
            if edge.vehicles():
                vehicles.extend(edge.vehicles())
        return vehicles

    def __check_translation_load(self):
        if not self.__translatables:
            E_TRANSLATOR_WAITING.send(sender=self)