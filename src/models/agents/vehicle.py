from models.traffic_models.idm import Idm
from models.traffic_models.lane_change_model import LaneChangeModel


class Vehicle:

    def __init__(self, vehicle_id, lane):
        self.id = vehicle_id
        self.lane = lane
        self.lane.add_vehicle(self)
        self.position = 0.0
        self.velocity = 0.0
        self.acceleration = 0.0
        self.desired_velocity = 33.3
        self.max_acceleration = 0.73
        self.desired_deceleration = 1.67
        self.length = 5.0
        self.politeness = 0.5
        self.at_end_of_lane = False

    def prospective_follower(self):
        target_lane = self.lane.next_lane()
        return target_lane.get_prospective_follower(self)

    def prospective_leader(self):
        target_lane = self.lane.next_lane()
        return target_lane.get_prospective_leader(self)

    def follower(self):
        return self.lane.get_follower(self)

    def leader(self):
        return self.lane.get_leader(self)

    def translate(self, t):
        u = self.velocity
        a = Idm.calculate_acceleration(self, self.leader())
        s = u*t + 0.5*(a*(t**2))
        self.__update_position_if_still_on_lane(s)
        self.velocity = u + a*t
        self.acceleration = a
        self.__change_lane_if_necessary()

    def __update_position_if_still_on_lane(self, displacement):
        new_position = self.position + displacement
        if new_position <= self.lane.length:
            self.position = new_position
        else:
            self.position = self.lane.length
            self.at_end_of_lane = True

    def __change_lane_if_necessary(self):
        if LaneChangeModel.vehicle_should_change_lane(self):
            target_lane = self.lane.next_lane()
            self.lane.remove_vehicle(self)
            target_lane.insert_vehicle_at_current_position(self)
            self.lane = target_lane