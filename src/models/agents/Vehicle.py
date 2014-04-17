class Vehicle:

    def __init__(self, vehicle_id, lane):
        self.id = vehicle_id
        self.lane = lane
        self.lane.add_vehicle(self)
        self.position = 0
        self.velocity = 0
        self.acceleration = 0
        self.desired_velocity = 0