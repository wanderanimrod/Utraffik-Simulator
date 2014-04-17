from unittest import TestCase
from models.agents.vehicle import Vehicle
from models.network.lane import Lane
from models.network.two_lane_one_way_edge import TwoLaneOneWayEdge


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

    def test_should_return_leader_as_vehicle_far_away_when_requester_is_the_leader(self):
        leader = Vehicle(0, self.lane)
        leader_returned = self.lane.get_leader(leader)
        self.assert_is_dummy_leader(leader_returned)

    def test_should_get_following_vehicle(self):
        leader, follower, lane = self.make_leader_and_follower()
        self.assertEqual(lane.get_follower(leader), follower)

    def test_should_return_follower_as_stationary_vehicle_when_requester_is_the_trailer(self):
        trailer = Vehicle(0, self.lane)
        follower_returned = self.lane.get_follower(trailer)
        self.assert_is_dummy_follower(follower_returned)

    def make_leader_and_follower(self):
        leader = Vehicle(0, self.lane)
        leader.position = 10
        follower = Vehicle(0, self.lane)
        return leader, follower, self.lane

    # TODO Test that vehicles upon insert are always sorted

    def make_lane(self, id=0):
        edge = TwoLaneOneWayEdge(0)
        return Lane(id, edge)

    def assert_is_dummy_leader(self, vehicle):
        self.assertEqual(vehicle.position, 100000)
        self.assertEqual(vehicle.velocity, 33.3)

    def assert_is_dummy_follower(self, vehicle):
        self.assertEqual(vehicle.position, 0)
        self.assertEqual(vehicle.acceleration, 0)
        self.assertEqual(vehicle.desired_velocity, 0)
        self.assertEqual(vehicle.velocity, 0)
