from unittest import TestCase

from mockito import mock

from models.agents.vehicle import Vehicle
from models.agents.vehicle_factory import VehicleFactory


class IdmTest(TestCase):

    def setUp(self):
        self.lane = mock()
        self.vehicle = Vehicle(0, self.lane)
        self.leader_far_away = VehicleFactory.make_dummy_leader()
        self.leader_nearby = VehicleFactory.make_dummy_leader()
        self.leader_nearby.position = 6

    def test_should_return_maximum_acceleration_if_leader_is_far_away(self):
        acceleration = self.calculate_acceleration(self.vehicle, self.leader_far_away)
        self.assertAlmostEqual(acceleration, self.vehicle.max_acceleration)
    
    def test_should_not_accelerate_if_vehicle_has_reached_desired_velocity(self):
        self.vehicle.velocity = self.vehicle.desired_velocity
        acceleration = self.calculate_acceleration(self.vehicle, self.leader_far_away)
        self.assertAlmostEqual(acceleration, 0, places=3)
    
    def test_should_not_accelerate_when_leader_is_nearby(self):
        acceleration = self.calculate_acceleration(self.vehicle, self.leader_nearby)
        self.assertAlmostEqual(acceleration, 0)
    
    def test_should_accelerate_normally_when_leader_is_far_away_and_desired_velocity_is_not_reached(self):
        self.vehicle.velocity = self.vehicle.desired_velocity / 2
        acceleration = self.calculate_acceleration(self.vehicle, self.leader_far_away)
        self.assertAlmostEqual(acceleration, 0.684, places=3)
    
    def test_should_decelerate_when_leader_is_nearby(self):
        self.vehicle.velocity = 10.0
        self.leader_nearby.position = 50
        acceleration = self.calculate_acceleration(self.vehicle, self.leader_nearby)
        self.assertAlmostEqual(acceleration, -2.056, places=3)
        
    def test_should_not_throw_an_error_if_desired_velocity_of_vehicle_is_zero(self):
        self.vehicle.desired_velocity = 0.0
        acceleration = self.calculate_acceleration(self.vehicle, self.leader_far_away)
        self.assertEqual(acceleration, 0.0)

    def calculate_acceleration(self, requester, leader):
        return requester._Vehicle__calculate_acceleration(leader)