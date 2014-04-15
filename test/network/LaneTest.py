from unittest import TestCase
from models.agents.Vehicle import Vehicle
from models.network.Lane import Lane
from models.network.TwoLaneOneWayEdge import TwoLaneOneWayEdge


class LaneTest(TestCase):

    def setUp(self):
        self.edge = TwoLaneOneWayEdge(0)
        self.lane = Lane(0, self.edge)

    # def test_should_add_itself_to_lane_upon_instantiation(self):
    #     add_lane_stub = Mock(TwoLaneOneWayEdge.add_lane)
        # TODO Check that add_lane is called on parent edge
        # add_lane_stub.assert_called_once_with(self.lane)

    def test_should_equate_lanes_by_id(self):
        edge = TwoLaneOneWayEdge(0)
        lane_1 = Lane(0, edge)
        lane_2 = Lane(0, edge)
        self.assertEqual(lane_1, lane_2)

    def test_should_add_vehicle_to_itself(self):
        vehicle = Vehicle(0, self.lane)
        self.assertTrue(self.lane.vehicles.__contains__(vehicle))