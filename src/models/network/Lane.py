from models.agents.vehicle_factory import VehicleFactory


class Lane:
    def __init__(self, lane_id, edge):
        self.id = lane_id
        self.parent_edge = edge
        self.parent_edge.add_lane(self)
        self.__vehicles = []

    def __eq__(self, other):
        return self.id == other.id

    def add_vehicle(self, vehicle):
        self.__vehicles.append(vehicle)

    def remove_vehicle(self, vehicle):
        self.__vehicles.remove(vehicle)

    def get_leader(self, requester):
        return self.__get_leader(requester, self.__vehicles)

    def get_follower(self, requester):
        index_of_requester = self.__vehicles.index(requester)
        if index_of_requester == len(self.__vehicles) - 1:
            return VehicleFactory.make_dummy_follower()
        return self.__vehicles[index_of_requester + 1]

    def get_prospective_leader(self, vehicle_joining):
        sorted_vehicles = self.__get_sorted_vehicles_with_new_vehicle_inserted(vehicle_joining, self.__vehicles)
        return self.__get_leader(vehicle_joining, sorted_vehicles)

    def insert_vehicle_at_current_position(self, vehicle):
        sorted_vehicles = self.__get_sorted_vehicles_with_new_vehicle_inserted(vehicle, self.__vehicles)
        self.__vehicles = sorted_vehicles

    @staticmethod
    def __get_leader(requester, vehicles):
        index_of_requester = vehicles.index(requester)
        if index_of_requester == 0:
            return VehicleFactory.make_dummy_leader()
        return vehicles[index_of_requester - 1]

    @staticmethod
    def __get_sorted_vehicles_with_new_vehicle_inserted(vehicle, vehicles):
        vehicles.append(vehicle)
        return sorted(vehicles, key=lambda car: -car.position)
