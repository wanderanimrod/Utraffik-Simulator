class TwoLaneOneWayEdge:

    def __init__(self, edge_id, length):
        self.id = edge_id
        self.first_lane = None
        self.second_lane = None
        self.length = length

    def lane_next_to(self, lane):
        if lane == self.first_lane:
            return self.second_lane
        elif lane == self.second_lane:
            return self.first_lane

    def add_lane(self, lane):
        if self.first_lane is None:
            self.first_lane = lane
        elif self.second_lane is None:
            self.second_lane = lane
        else:
            raise Exception("Two Lane Edge already has two lanes.")

    def vehicles(self):
        vehicles = []
        if self.first_lane.vehicles:
            vehicles.extend(self.first_lane.vehicles)
        if self.second_lane.vehicles:
            vehicles.extend(self.second_lane.vehicles)
        return vehicles