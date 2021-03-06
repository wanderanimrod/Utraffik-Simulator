from unittest import TestCase

from mockito import when, mock

from models.agents.vehicle import Vehicle
from models.agents.vehicle_factory import make_dummy_follower, make_dummy_leader
from models.traffic_models.lane_change_model import LaneChangeModel
from models.traffic_models.shared_constants import min_clearance


class LaneChangeModelTest(TestCase):

    def setUp(self):
        self.vehicle = Vehicle(0, mock())

    def test_should_okay_lane_change_if_acceleration_is_less_than_max_acceleration(self):
        vehicle = self.make_lane_change_incentive_high(self.vehicle)
        self.make_lane_change_scenario_with_ample_clearance_for(vehicle)
        self.put_acceleration_at_sub_optimal_level(vehicle)
        should_change_lane = LaneChangeModel.vehicle_should_change_lane(vehicle)
        self.assertTrue(should_change_lane)

    def test_should_not_okay_lane_change_if_acceleration_is_equal_to_max_acceleration(self):
        vehicle = self.make_lane_change_incentive_high(self.vehicle)
        self.make_lane_change_scenario_with_ample_clearance_for(self.vehicle)
        vehicle.acceleration = vehicle.max_acceleration
        should_change_lane = LaneChangeModel.vehicle_should_change_lane(vehicle)
        self.assertFalse(should_change_lane)

    def test_should_not_okay_lane_change_if_clearance_from_prospective_follower_will_not_be_enough(self):
        vehicle = self.make_lane_change_incentive_high(self.vehicle)
        self.put_acceleration_at_sub_optimal_level(vehicle)
        self.make_lane_change_scenario_with_little_clearance_for(vehicle)
        should_change_lane = LaneChangeModel.vehicle_should_change_lane(vehicle)
        self.assertFalse(should_change_lane)

    def test_should_okay_lane_change_if_clearance_from_prospective_follower_will_be_enough(self):
        vehicle = self.make_lane_change_incentive_high(self.vehicle)
        self.make_lane_change_scenario_with_ample_clearance_for(vehicle)
        should_change_lane = LaneChangeModel.vehicle_should_change_lane(vehicle)
        self.assertTrue(should_change_lane)

    def test_should_not_okay_lane_change_if_lane_change_incentive_is_lower_than_lane_change_threshold(self):
        vehicle = self.make_lane_change_scenario_with_ample_clearance_for(self.vehicle)
        self.put_acceleration_at_sub_optimal_level(vehicle)
        should_change_lane = LaneChangeModel.vehicle_should_change_lane(vehicle)
        self.assertFalse(should_change_lane)

    def test_should_okay_lane_change_if_all_other_factors_allow_for_it(self):
        vehicle = self.make_lane_change_incentive_high(self.vehicle)
        self.make_lane_change_scenario_with_ample_clearance_for(vehicle)
        self.put_acceleration_at_sub_optimal_level(vehicle)
        should_change_lane = LaneChangeModel.vehicle_should_change_lane(vehicle)
        self.assertTrue(should_change_lane)

    def make_lane_change_incentive_high(self, requester):
        requester.politeness = 0.0
        requester.position = 100
        blocker_nearby = make_dummy_follower()
        blocker_nearby.position = requester.position + 3
        follower_nearby = make_dummy_leader()
        follower_nearby.position = requester.position - requester.length + (min_clearance / 2)
        prospective_leader_far_away = make_dummy_leader()
        when(requester).leader().thenReturn(blocker_nearby)
        when(requester).prospective_leader().thenReturn(prospective_leader_far_away)
        when(requester).prospective_follower().thenReturn(make_dummy_follower())
        when(requester).follower().thenReturn(follower_nearby)
        self.assertGreater(LaneChangeModel._calculate_lane_change_incentive,
                           LaneChangeModel._lane_change_threshold)
        return requester

    def make_lane_change_scenario_with_ample_clearance_for(self, requester):
        requester.position = 100
        follower_far_away = make_dummy_leader()
        follower_far_away.position = 0
        when(requester).prospective_follower().thenReturn(follower_far_away)
        when(requester).follower().thenReturn(follower_far_away)
        when(requester).leader().thenReturn(make_dummy_leader())
        when(requester).prospective_leader().thenReturn(make_dummy_leader())
        return requester

    def make_lane_change_scenario_with_little_clearance_for(self, requester):
        follower_nearby = make_dummy_follower()
        follower_nearby.position = requester.position - requester.length + (min_clearance / 2)
        when(requester).prospective_follower().thenReturn(follower_nearby)
        return requester

    def put_acceleration_at_sub_optimal_level(self, vehicle):
        vehicle.acceleration = vehicle.max_acceleration / 2