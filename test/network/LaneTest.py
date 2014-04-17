from unittest import TestCase
from models.agents.Vehicle import Vehicle
from models.network.Lane import Lane
from models.network.TwoLaneOneWayEdge import TwoLaneOneWayEdge


class LaneTest(TestCase):

    def setUp(self):
        self.lane = self.make_lane()

    # def test_should_add_itself_to_edge_upon_instantiation(self):
    #     add_lane_stub = Mock(TwoLaneOneWayEdge.add_lane)
        # TODO Check that add_lane is called on parent edge
        # add_lane_stub.assert_called_once_with(self.lane)

    def test_should_equate_lanes_by_id(self):
        lane_1 = self.make_lane(id=1)
        lane_2 = self.make_lane(id=1)
        self.assertEqual(lane_1, lane_2)

    def test_should_add_vehicle_to_itself(self):
        vehicle = Vehicle(0, self.lane)
        self.assertTrue(self.lane.vehicles.__contains__(vehicle))

    def test_should_remove_vehicle_from_self(self):
        vehicle = Vehicle(0, self.lane)
        self.lane.remove_vehicle(vehicle)
        self.assertFalse(self.lane.vehicles.__contains__(vehicle))

    def test_should_get_leading_vehicle(self):
        leader, follower, lane = self.make_leader_and_follower()
        self.assertEqual(lane.get_leader(follower), leader)

    def test_should_get_following_vehicle(self):
        leader, follower, lane = self.make_leader_and_follower()
        self.assertEqual(lane.get_follower(leader), follower)

    def make_leader_and_follower(self):
        leader = Vehicle(0, self.lane)
        leader.position = 10
        follower = Vehicle(0, self.lane)
        return leader, follower, self.lane

# TODO Test that vehicles upon insert are always sorted

    def make_lane(self, id=0):
        edge = TwoLaneOneWayEdge(0)
        return Lane(id, edge)