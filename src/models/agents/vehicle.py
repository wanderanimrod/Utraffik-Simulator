from app.events.events import E_END_OF_LANE, E_END_OF_JOURNEY, E_TRANSLATE
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

    def translate(self, time_delta, time_now):
        u = self.velocity
        a = Idm.calculate_acceleration(self, self.leader())
        s = u * time_delta + 0.5 * (a * (time_delta ** 2))
        self._update_position_if_still_on_lane(s)
        self.velocity = u + a * time_delta
        self.acceleration = a
        self._change_lane_if_necessary()
        E_TRANSLATE.send(sender=self, timestamp=time_now)

    def _update_position_if_still_on_lane(self, displacement):
        new_position = self.position + displacement
        if new_position <= self.lane.length:
            self.position = new_position
        else:
            self.position = self.lane.length
            E_END_OF_LANE.send(sender=self, next_lane=None)
            E_END_OF_JOURNEY.send(sender=self)

    def _change_lane_if_necessary(self):
        if LaneChangeModel.vehicle_should_change_lane(self):
            target_lane = self.lane.next_lane()
            self.lane.remove_vehicle(self)
            target_lane.insert_vehicle_at_current_position(self)
            self.lane = target_lane