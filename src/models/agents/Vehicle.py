class Vehicle:

    def __init__(self, vehicle_id, lane=None):
        self.id = vehicle_id
        self.lane = lane
        if lane is not None:
            self.lane.add_vehicle(self)
        self.position = 0
        self.velocity = 0
        self.acceleration = 0
        self.desired_velocity = 0