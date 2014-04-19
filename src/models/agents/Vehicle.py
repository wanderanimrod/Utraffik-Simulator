class Vehicle:
    T = 1.67
    delta = 4.0
    min_clearance = 1.0
    lane_change_threshold = 0.1

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

    def __should_change_lane(self):
        if self.acceleration < self.max_acceleration:
            target_lane = self.lane.get_next_lane()
            prospective_follower = target_lane.get_prospective_follower(self)
            if self.__clearance_from(prospective_follower) >= Vehicle.min_clearance:
                follower = self.lane.get_follower(self)
                lane_change_incentive = self.__calculate_lane_change_incentive(follower, prospective_follower)
                return True
        return False



    def __clearance_from(self, follower):
        return self.position - self.length - follower.position