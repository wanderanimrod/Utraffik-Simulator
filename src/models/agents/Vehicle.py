class Vehicle:

    T = 1.67
    delta = 4.0
    min_clearance = 1.0

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

    # Variable names used as described in Wikipedia entry on IDM
    def __calculate_acceleration(self, leader):
        v = self.velocity
        a = self.max_acceleration
        b = self.desired_deceleration
        delta_v = v - leader.velocity
        s = leader.position - self.position - leader.length
        s_star = Vehicle.min_clearance + (v * Vehicle.T) + ((v * delta_v) / (2 * (a * b) ** 0.5))
        try:
            return a * (1 - (v/self.desired_velocity)**Vehicle.delta - (s_star/s)**2)
        except ZeroDivisionError:
            return 0.0

    def __should_change_lane(self):
        if self.acceleration < self.max_acceleration:
            target_lane = self.lane.get_next_lane()
            prospective_follower = target_lane.get_prospective_follower(self)
            # follower = self.lane.get_follower(self)
            # leader = self.lane.get_leader(self)
            if self.__clearance_from(prospective_follower) >= Vehicle.min_clearance:
                return True
        return False

    def __clearance_from(self, follower):
        return self.position - self.length - follower.position