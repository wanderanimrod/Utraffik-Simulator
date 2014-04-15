from unittest import TestCase
from models.network.Lane import Lane
from models.network.TwoLaneOneWayEdge import TwoLaneOneWayEdge
from mock import Mock


class LaneTest(TestCase):

    def test_should_add_itself_to_lane_upon_instantiation(self):
        edge = TwoLaneOneWayEdge(0)
        add_lane_stub = Mock(TwoLaneOneWayEdge.add_lane)
        lane = Lane(0, edge)
        add_lane_stub.assert_called_once_with(lane)