from unittest import TestCase

from mockito import mock

from models.agents.vehicle import Vehicle
from models.network.lane import Lane
from models.network.two_lane_one_way_edge import TwoLaneOneWayEdge


class TwoLaneOneWayEdgeTest(TestCase):

    def setUp(self):
        self.edge = TwoLaneOneWayEdge(0, 100)
        self.first_lane = Lane(0, self.edge)
        self.second_lane = Lane(1, self.edge)

    def test_should_get_next_lane_in_alternate_fashion(self):
        self.assertEquals(self.edge.lane_next_to(self.first_lane), self.second_lane)
        self.assertEquals(self.edge.lane_next_to(self.second_lane), self.first_lane)

    def test_should_add_lane_to_itself(self):
        edge = TwoLaneOneWayEdge(0, 100)
        lane = mock()
        edge.add_lane(lane)
        self.assertEquals(edge.first_lane, lane)

    def test_should_add_two_lanes_to_itself(self):
        self.assertEquals(self.edge.first_lane, self.first_lane)
        self.assertEquals(self.edge.second_lane, self.second_lane)

    def test_should_refuse_addition_of_more_than_two_lanes(self):
        with self.assertRaises(Exception):
            Lane(2, self.edge)

    def test_should_get_all_vehicles_on_all_lanes_on_the_edge(self):
        vehicle_1 = Vehicle(1, self.first_lane)
        vehicle_2 = Vehicle(1, self.second_lane)
        vehicles_on_edge = self.edge.vehicles()
        self.assertEqual(vehicles_on_edge, [vehicle_1, vehicle_2])

    def test_should_return_empty_list_if_there_are_no_vehicles_on_all_lanes_on_the_edge(self):
        self.assertEqual(self.edge.vehicles(), [])