from unittest import TestCase
from mockito import mock, verify
from models.agents.vehicle import Vehicle
from models.network.lane import Lane
from models.network.two_lane_one_way_edge import TwoLaneOneWayEdge


class LaneTest(TestCase):

    def setUp(self):
        self.edge = mock()
        self.lane = Lane(0, self.edge)
        self.adjacent_lane = Lane(1, self.edge)

    def test_should_add_itself_to_edge_upon_instantiation(self):
        lane = Lane(0, self.edge)
        verify(self.edge).add_lane(lane)

    def test_should_equate_lanes_by_id(self):
        lane_1 = Lane(1, mock())
        lane_2 = Lane(1, mock())
        self.assertEqual(lane_1, lane_2)

    def test_should_add_vehicle_to_itself(self):
        vehicle = mock()
        self.lane.add_vehicle(vehicle)
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

    def test_should_get_prospective_leader_for_vehicle_on_another_lane(self):
        prospective_leader, vehicle_joining, _ = self.create_prospective_lane_change_scene()
        prospective_leader_returned = self.lane.get_prospective_leader(vehicle_joining)
        self.assertEqual(prospective_leader_returned, prospective_leader)

    def test_should_return_prospective_leader_as_vehicle_far_away_if_requester_will_be_the_leader_on_target_lane(self):
        vehicle_joining = Vehicle(0, self.adjacent_lane)
        prospective_leader = self.lane.get_prospective_leader(vehicle_joining)
        self.assert_is_dummy_leader(prospective_leader)

    def test_should_get_prospective_follower_for_vehicle_on_another_lane(self):
        _, vehicle_joining, prospective_follower = self.create_prospective_lane_change_scene()
        prospective_follower_returned = self.lane.get_prospective_follower(vehicle_joining)
        self.assertEqual(prospective_follower_returned, prospective_follower)

    def test_should_return_follower_as_stationary_vehicle_when_requester_will_be_the_trailer_on_the_target_lane(self):
        vehicle_joining = Vehicle(0, self.adjacent_lane)
        prospective_follower = self.lane.get_prospective_follower(vehicle_joining)
        self.assert_is_dummy_follower(prospective_follower)

    def test_should_insert_vehicle_into_its_correct_position_on_lane(self):
        leader, follower, lane = self.make_leader_and_follower()
        middle_vehicle = Vehicle(11, self.adjacent_lane)
        middle_vehicle.position = (leader.position - follower.position)/2
        lane.insert_vehicle_at_current_position(middle_vehicle)
        self.assert_vehicles_are_in_order(lane.vehicles)

    def test_should_get_next_lane(self):
        self.lane.next_lane()
        verify(self.edge).lane_next_to(self.lane)

    def test_length_of_lane_should_be_length_of_parent_edge(self):
        edge = TwoLaneOneWayEdge(0, 100)
        lane = Lane(0, edge)
        self.assertEqual(lane.length, edge.length)

    def assert_vehicles_are_in_order(self, vehicles):
        for follower in vehicles[1:]:
            leader = vehicles[vehicles.index(follower) - 1]
            leader_is_ahead_of_follower = lambda l, f: l.position >= f.position
            self.assertTrue(leader_is_ahead_of_follower(leader, follower))

    def make_leader_and_follower(self):
        leader = Vehicle(0, self.lane)
        leader.position = 10
        follower = Vehicle(0, self.lane)
        return leader, follower, self.lane

    def create_prospective_lane_change_scene(self):
        prospective_leader = Vehicle(0, self.lane)
        prospective_leader.position = 100
        prospective_follower = Vehicle(2, self.lane)
        vehicle_joining = Vehicle(1, self.adjacent_lane)
        vehicle_joining.position = 20
        return prospective_leader, vehicle_joining, prospective_follower

    def assert_is_dummy_leader(self, vehicle):
        self.assertEqual(vehicle.position, 100000)
        self.assertEqual(vehicle.velocity, 33.3)

    def assert_is_dummy_follower(self, vehicle):
        self.assertEqual(vehicle.position, 0)
        self.assertEqual(vehicle.acceleration, 0)
        self.assertEqual(vehicle.desired_velocity, 0)
        self.assertEqual(vehicle.velocity, 0)