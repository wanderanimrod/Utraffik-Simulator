class TwoLaneOneWayEdge:

    def __init__(self, edge_id):
        self.id = edge_id
        self.first_lane = None
        self.second_lane = None

    def lane_next_to(self, lane):
        pass

    def add_lane(self, lane):
        if self.first_lane is None:
            self.first_lane = lane
        elif self.second_lane is None:
            self.second_lane = lane