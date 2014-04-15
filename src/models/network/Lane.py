class Lane:
    def __init__(self, lane_id, edge):
        self.id = lane_id
        self.parent_edge = edge
        self.parent_edge.add_lane(self)

    def __eq__(self, other):
        return self.id == other.id
