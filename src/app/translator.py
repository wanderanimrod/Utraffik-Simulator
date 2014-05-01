from app.events.events import E_TRANSLATOR_WAITING


class Translator:

    def __init__(self, edges):
        self.edges = edges
        self.vehicles = self.__get_vehicles()
        self.__translatables = self.vehicles
        self.__check_translation_load()

    def run(self):
        pass

    def __get_vehicles(self):
        vehicles = []
        for edge in self.edges:
            if edge.vehicles():
                vehicles.extend(edge.vehicles())
        return vehicles

    def __check_translation_load(self):
        if not len(self.__translatables):
            E_TRANSLATOR_WAITING.send(sender=self)