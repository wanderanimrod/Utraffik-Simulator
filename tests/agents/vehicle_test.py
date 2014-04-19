from unittest import TestCase

from mockito import mock, when

from models.agents.vehicle import Vehicle


class VehicleTest(TestCase):

    # def test_should_add_itself_to_parent_lane_upon_instantiation(self):
        # TODO Fix this mocking stuff. Mockito is fake.
        # pass

    # TODO Test that it delegate next_lane function to it lane

    def setUp(self):
        self.lane = mock()
        self.target_lane = mock()
        when(self.lane).next_lane().thenReturn(self.target_lane)
        self.vehicle = Vehicle(0, self.lane)
        self.mock_vehicle = mock()

    def test_should_be_created_with_position_zero(self):
        self.assertEqual(self.vehicle.position, 0)

    def test_should_get_prospective_follower_from_target_lane(self):
        when(self.target_lane).get_prospective_follower(self.vehicle).thenReturn(self.mock_vehicle)
        self.assertEqual(self.vehicle.prospective_follower(), self.mock_vehicle)

    def test_should_get_prospective_leader_from_target_lane(self):
        when(self.target_lane).get_prospective_leader(self.vehicle).thenReturn(self.mock_vehicle)
        self.assertEqual(self.vehicle.prospective_leader(), self.mock_vehicle)

    def test_should_get_follower_from_current_lane(self):
        when(self.lane).get_follower(self.vehicle).thenReturn(self.mock_vehicle)
        self.assertEqual(self.vehicle.follower(), self.mock_vehicle)