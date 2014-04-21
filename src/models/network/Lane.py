from models.agents.vehicle_factory import dummy_leader, dummy_follower


class Lane:
    def __init__(self, lane_id, edge):
        self.id = lane_id
        self.__parent_edge = edge
        self.__parent_edge.add_lane(self)
        self.__vehicles = []

    def __eq__(self, other):
        return self.id == other.id

    def add_vehicle(self, vehicle):
        self.__vehicles.append(vehicle)

    def remove_vehicle(self, vehicle):
        self.__vehicles.remove(vehicle)

    def get_leader(self, requester):
        return self.__get_leader_or_dummy(requester, self.__vehicles)

    def get_follower(self, requester):
        return self.__get_follower_or_dummy(requester, self.__vehicles)

    def get_prospective_leader(self, vehicle_joining):
        sorted_vehicles = self.__copy_insert_and_sort(vehicle_joining, self.__vehicles)
        return self.__get_leader_or_dummy(vehicle_joining, sorted_vehicles)

    def get_prospective_follower(self, vehicle_joining):
        sorted_vehicles = self.__copy_insert_and_sort(vehicle_joining, self.__vehicles)
        return self.__get_follower_or_dummy(vehicle_joining, sorted_vehicles)

    def insert_vehicle_at_current_position(self, vehicle):
        sorted_vehicles = self.__copy_insert_and_sort(vehicle, self.__vehicles)
        self.__vehicles = sorted_vehicles

    def next_lane(self):
        return self.__parent_edge.lane_next_to(self)

    @staticmethod
    def __get_leader_or_dummy(requester, vehicles):
        index_of_requester = vehicles.index(requester)
        if index_of_requester == 0:
            return dummy_leader
        return vehicles[index_of_requester - 1]

    @staticmethod
    def __get_follower_or_dummy(requester, vehicles):
        index_of_requester = vehicles.index(requester)
        if index_of_requester == len(vehicles) - 1:
            return dummy_follower
        return vehicles[index_of_requester + 1]

    @staticmethod
    def __copy_insert_and_sort(vehicle, vehicles):
        vehicles.append(vehicle)
        return sorted(vehicles, key=lambda car: -car.position)
