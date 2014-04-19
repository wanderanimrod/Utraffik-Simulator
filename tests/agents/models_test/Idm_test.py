from unittest import TestCase

from mockito import mock, when

from models.agents.vehicle import Vehicle
from models.agents.vehicle_factory import VehicleFactory


class IdmTest(TestCase):

    def test_should_return_maximum_acceleration_if_leader_is_far_away(self):
        lane = mock()
        leader_far_away = VehicleFactory.make_dummy_leader()
        when(lane.get_leader()).thenReturn(leader_far_away)
        vehicle = Vehicle(0, lane)
        acceleration = vehicle._Vehicle__calculate_acceleration(leader_far_away)
        self.assertAlmostEqual(acceleration, vehicle.max_acceleration)