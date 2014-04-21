from models.traffic_models.idm import Idm


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

    def translate(self, t):
        u = self.velocity
        a = Idm.calculate_acceleration(self, self.leader())
        s = u*t + 0.5*(a*(t**2))
        self.position += s
        self.velocity = u + a*t
        self.acceleration = a