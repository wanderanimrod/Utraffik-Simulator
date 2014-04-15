from unittest import TestCase
from models.network.Lane import Lane
from models.network.TwoLaneOneWayEdge import TwoLaneOneWayEdge
from mock import Mock


class LaneTest(TestCase):

    def setUp(self):
        self.edge = TwoLaneOneWayEdge(0)

    def test_should_add_itself_to_lane_upon_instantiation(self):
        add_lane_stub = Mock(TwoLaneOneWayEdge.add_lane)
        lane = Lane(0, self.edge)
        # TODO Check that add_lane is called on parent edge
        add_lane_stub.assert_called_once_with(lane)

    def test_should_equate_lanes_by_id(self):
        lane_1 = Lane(0, self.edge)
        lane_2 = Lane(0, self.edge)
        self.assertEqual(lane_1, lane_2)