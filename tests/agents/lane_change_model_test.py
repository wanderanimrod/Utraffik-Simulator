from unittest import TestCase

from mockito import when, mock

from models.agents.vehicle import Vehicle
from models.agents.vehicle_factory import VehicleFactory
from models.traffic_models.lane_change_model import LaneChangeModel


class LaneChangeModelTest(TestCase):

    def setUp(self):
        self.lane = mock()
        self.target_lane = mock()
        when(self.lane).next_lane().thenReturn(self.target_lane)
        self.vehicle = Vehicle(0, self.lane)
        self.vehicle_should_change_lane = LaneChangeModel.vehicle_should_change_lane

    def test_should_okay_lane_change_if_acceleration_is_less_than_max_acceleration(self):
        vehicle = self.make_lane_change_scenario_with_ample_clearance(self.vehicle)
        self.put_acceleration_at_sub_optimal_level(vehicle)
        self.assertTrue(self.vehicle_should_change_lane(vehicle))

    def test_should_not_change_lane_if_acceleration_is_equal_to_max_acceleration(self):
        vehicle = self.make_lane_change_scenario_with_ample_clearance(self.vehicle)
        vehicle.acceleration = vehicle.max_acceleration
        self.assertFalse(self.vehicle_should_change_lane(vehicle))

    def test_should_not_okay_lane_change_if_clearance_from_prospective_follower_will_not_be_enough(self):
        vehicle = self.make_lane_change_scenario_with_little_clearance(self.vehicle)
        self.put_acceleration_at_sub_optimal_level(vehicle)
        self.assertFalse(self.vehicle_should_change_lane(vehicle))

    def test_should_okay_lane_change_if_clearance_from_prospective_follower_will_be_enough(self):
        vehicle = self.make_lane_change_scenario_with_ample_clearance(self.vehicle)
        self.assertTrue(self.vehicle_should_change_lane(vehicle))

    def make_lane_change_scenario_with_ample_clearance(self, leader):
        leader.position = 100
        follower_far_away = VehicleFactory.make_dummy_leader()
        follower_far_away.position = 0
        self.mock_prospective_follower(leader, follower_far_away)
        return leader

    def make_lane_change_scenario_with_little_clearance(self, leader):
        follower_nearby = VehicleFactory.make_dummy_follower()
        follower_nearby.position = leader.position - leader.length + (Vehicle.min_clearance / 2)
        self.mock_prospective_follower(leader, follower_nearby)
        return leader

    def mock_prospective_follower(self, leader, follower):
        when(self.target_lane).get_prospective_follower(leader).thenReturn(follower)

    def put_acceleration_at_sub_optimal_level(self, vehicle):
        vehicle.acceleration = vehicle.max_acceleration / 2