from unittest import TestCase

from mockito import mock, when

from models.agents.vehicle import Vehicle
from models.agents.vehicle_factory import VehicleFactory


class IdmTest(TestCase):

    def setUp(self):
        self.lane = mock()
        self.vehicle = Vehicle(0, self.lane)
        self.leader_far_away = VehicleFactory.make_dummy_leader()

    def test_should_return_maximum_acceleration_if_leader_is_far_away(self):

        when(self.lane.get_leader()).thenReturn(self.leader_far_away)
        acceleration = self.calculate_acceleration(self.vehicle, self.leader_far_away)
        self.assertAlmostEqual(acceleration, self.vehicle.max_acceleration)
    
    def test_should_not_accelerate_if_vehicle_has_reached_desired_velocity(self):
        self.vehicle.velocity = self.vehicle.desired_velocity
        acceleration = self.calculate_acceleration(self.vehicle, self.leader_far_away)
        self.assertAlmostEqual(acceleration, 0)

    def calculate_acceleration(self, requester, leader):
        acc = requester._Vehicle__calculate_acceleration(leader)
        return round(acc, 6)