from unittest import TestCase

from mock import Mock

from models.agents.vehicle import Vehicle
from models.network.lane import Lane


class VehicleTest(TestCase):

    def test_should_add_itself_to_parent_lane_upon_instantiation(self):
        # TODO Implement this once you have figured out the mock stuff
        pass

    def test_should_be_created_with_position_zero(self):
        vehicle = Vehicle(0, Mock(Lane))
        self.assertEqual(vehicle.position, 0)