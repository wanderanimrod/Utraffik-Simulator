from unittest import TestCase

from mockito import mock, verify

from models.agents.vehicle import Vehicle


class VehicleTest(TestCase):

    def test_should_add_itself_to_parent_lane_upon_instantiation(self):
        # TODO Fix this mocking stuff. Mockito is fake.
        # my_mock = mock()
        # Vehicle(0, my_mock)
        # verify(my_mock).add_vehicle()
        pass

    def test_should_be_created_with_position_zero(self):
        vehicle = Vehicle(0, mock())
        self.assertEqual(vehicle.position, 0)