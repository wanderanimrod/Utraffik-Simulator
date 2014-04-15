from unittest import TestCase
from models.network.Lane import Lane
from models.network.TwoLaneOneWayEdge import TwoLaneOneWayEdge


class TwoLaneOneWayEdgeTest(TestCase):

    def setUp(self):
        self.edge = TwoLaneOneWayEdge(0)
        self.first_lane = Lane(0, self.edge)
        self.second_lane = Lane(1, self.edge)

    def test_should_get_next_lane_in_alternate_fashion(self):
        self.assertEquals(self.edge.lane_next_to(self.first_lane), self.second_lane)
        self.assertEquals(self.edge.lane_next_to(self.second_lane), self.first_lane)

    def test_should_add_lane_to_itself(self):
        edge = TwoLaneOneWayEdge(0)
        lane = Lane(0, edge)
        self.assertEquals(edge.first_lane, lane)

    def test_should_add_two_lanes_to_itself(self):
        self.assertEquals(self.edge.first_lane, self.first_lane)
        self.assertEquals(self.edge.second_lane, self.second_lane)

    def test_should_refuse_addition_of_other_lanes(self):
        with self.assertRaises(Exception):
            Lane(2, self.edge)