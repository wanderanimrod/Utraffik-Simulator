from unittest import TestCase

from mockito import when, mock, spy

from models.agents.vehicle import Vehicle
from models.agents.vehicle_factory import VehicleFactory
from models.traffic_models.lane_change_model import LaneChangeModel
from models.traffic_models.shared_constants import min_clearance


class LaneChangeModelTest(TestCase):

    def setUp(self):
        self.lane = mock()
        self.target_lane = mock()
        when(self.lane).next_lane().thenReturn(self.target_lane)
        self.vehicle = Vehicle(0, self.lane)
        self.vehicle_should_change_lane = LaneChangeModel.vehicle_should_change_lane

    def test_should_okay_lane_change_if_acceleration_is_less_than_max_acceleration(self):
        vehicle = self.make_lane_change_scenario_with_ample_clearance_for(self.vehicle)
        self.put_acceleration_at_sub_optimal_level(vehicle)
        lane_change_model = self.make_lane_change_incentive_high()
        should_change_lane = lane_change_model.vehicle_should_change_lane(vehicle)
        self.assertTrue(should_change_lane)

    def test_should_not_change_lane_if_acceleration_is_equal_to_max_acceleration(self):
        vehicle = self.make_lane_change_scenario_with_ample_clearance_for(self.vehicle)
        vehicle.acceleration = vehicle.max_acceleration
        self.assertFalse(self.vehicle_should_change_lane(vehicle))

    def test_should_not_okay_lane_change_if_clearance_from_prospective_follower_will_not_be_enough(self):
        vehicle = self.make_lane_change_scenario_with_little_clearance_for(self.vehicle)
        self.put_acceleration_at_sub_optimal_level(vehicle)
        self.assertFalse(self.vehicle_should_change_lane(vehicle))

    def test_should_okay_lane_change_if_clearance_from_prospective_follower_will_be_enough(self):
        vehicle = self.make_lane_change_scenario_with_ample_clearance_for(self.vehicle)
        self.assertTrue(self.vehicle_should_change_lane(vehicle))

    def test_should_not_okay_lane_change_if_lane_change_incentive_is_lower_than_lane_change_threshold(self):
        vehicle = self.make_lane_change_scenario_with_ample_clearance_for(self.vehicle)
        self.put_acceleration_at_sub_optimal_level(vehicle)
        lane_change_model = self.make_lane_change_incentive_low(vehicle)
        should_change_lane = lane_change_model.vehicle_should_change_lane(vehicle)
        self.assertFalse(should_change_lane)

    def test_should_stub_out_incentive(self):
        vehicle = self.make_lane_change_scenario_with_ample_clearance_for(self.vehicle)
        lane_change_model = self.make_lane_change_incentive_low(vehicle)
        incentive = self.get_lane_change_incentive(lane_change_model, vehicle)
        self.assertEqual(incentive, 0.05)

    def get_lane_change_incentive(self, model, requester):
        return  model._LaneChangeModel____calculate_lane_change_incentive(
            requester, requester.follower(), requester.prospective_follower()
        )

    def make_lane_change_incentive_low(self, requester):
        lane_change_model_spy = spy(LaneChangeModel)
        low_incentive = LaneChangeModel.lane_change_threshold / 2.0
        when(lane_change_model_spy)._LaneChangeModel____calculate_lane_change_incentive(
            requester, requester.follower(), requester.prospective_follower()
        ).thenReturn(low_incentive)
        return lane_change_model_spy

    def make_lane_change_incentive_high(self, requester):
        lane_change_model_spy = spy(LaneChangeModel)
        high_incentive = LaneChangeModel.lane_change_threshold * 2
        when(lane_change_model_spy)._LaneChangeModel____calculate_lane_change_incentive(
            requester, requester.follower(), requester.prospective_follower()
        ).thenReturn(high_incentive)
        return lane_change_model_spy

    def make_lane_change_scenario_with_ample_clearance_for(self, requester):
        requester.position = 100
        follower_far_away = VehicleFactory.make_dummy_leader()
        follower_far_away.position = 0
        self.mock_prospective_follower(requester, follower_far_away)
        self.mock_follower(requester, follower_far_away)
        self.mock_leader(requester, VehicleFactory.make_dummy_leader())
        self.mock_prospective_leader(requester, VehicleFactory.make_dummy_leader())
        return requester

    def make_lane_change_scenario_with_little_clearance_for(self, requester):
        follower_nearby = VehicleFactory.make_dummy_follower()
        follower_nearby.position = requester.position - requester.length + (min_clearance / 2)
        self.mock_prospective_follower(requester, follower_nearby)
        return requester

    def mock_prospective_follower(self, requester, follower):
        when(self.target_lane).get_prospective_follower(requester).thenReturn(follower)

    def mock_follower(self, requester, follower):
        when(self.lane).get_follower(requester).thenReturn(follower)

    def mock_leader(self, requester, leader):
        when(self.lane).get_leader(requester).thenReturn(leader)

    def mock_prospective_leader(self, requester, leader):
        when(self.target_lane).get_prospective_leader(requester).thenReturn(leader)

    def put_acceleration_at_sub_optimal_level(self, vehicle):
        vehicle.acceleration = vehicle.max_acceleration / 2