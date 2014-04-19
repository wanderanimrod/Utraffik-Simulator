from unittest import TestCase
from models.agents.vehicle import Vehicle
from models.network.lane import Lane
from models.network.two_lane_one_way_edge import TwoLaneOneWayEdge


class LaneChangeModelTest(TestCase):

    def setUp(self):
        edge = TwoLaneOneWayEdge(0)
        lane = Lane(0, edge)
        self.vehicle = Vehicle(0, lane)
    
    def test_should_okay_lane_change_if_acceleration_is_less_than_max_acceleration(self):
        self.vehicle.acceleration = self.vehicle.max_acceleration / 2
        self.assertTrue(self.vehicle.should_change_lane())

    def test_should_not_change_lane_if_acceleration_is_equal_to_max_acceleration(self):
        self.vehicle.acceleration = self.vehicle.max_acceleration
        print self.vehicle.acceleration
        self.assertFalse(self.vehicle.should_change_lane())