from unittest import TestCase

from mockito import when, mock

from models.agents.vehicle import Vehicle
from models.agents.vehicle_factory import VehicleFactory


class LaneChangeModelTest(TestCase):

    def setUp(self):
        self.lane = mock()
        self.target_lane = mock()
        when(self.lane).get_next_lane().thenReturn(self.target_lane)
        self.vehicle = Vehicle(0, self.lane)
        self.follower_nearby = VehicleFactory.make_dummy_leader()
        self.follower_far_away = VehicleFactory.make_dummy_leader()
        self.follower_far_away.position = 0
        self.make_should_change_lane_method_visible(self.vehicle)
    
    def test_should_okay_lane_change_if_acceleration_is_less_than_max_acceleration(self):
        self.vehicle.position = 100
        when(self.target_lane).get_prospective_follower(self.vehicle).thenReturn(self.follower_far_away)
        self.vehicle.acceleration = self.vehicle.max_acceleration / 2
        should_change_lane = self.vehicle.should_change_lane()
        self.assertTrue(should_change_lane)

    def test_should_not_change_lane_if_acceleration_is_equal_to_max_acceleration(self):
        self.vehicle.acceleration = self.vehicle.max_acceleration
        should_change_lane = self.vehicle.should_change_lane()
        self.assertFalse(should_change_lane)

    def test_should_not_okay_lane_change_if_clearance_from_prospective_follower_will_not_be_enough(self):
        self.follower_nearby.position = self.vehicle.position - self.vehicle.length + (Vehicle.min_clearance / 2)
        when(self.target_lane).get_prospective_follower(self.vehicle).thenReturn(self.follower_nearby)
        should_change_lane = self.vehicle.should_change_lane()
        self.assertFalse(should_change_lane)

    def make_should_change_lane_method_visible(self, vehicle):
        vehicle.should_change_lane = vehicle._Vehicle__should_change_lane