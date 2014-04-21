from unittest import TestCase

from mockito import mock, when

from models.agents.vehicle import Vehicle
from models.traffic_models.idm import Idm


class VehicleTest(TestCase):

    # def test_should_add_itself_to_parent_lane_upon_instantiation(self):
        # TODO Fix this mocking stuff. Mockito is fake.
        # pass

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

    def test_should_get_leader_from_current_lane(self):
        when(self.lane).get_leader(self.vehicle).thenReturn(self.mock_vehicle)
        self.assertEqual(self.vehicle.leader(), self.mock_vehicle)

    def test_should_update_velocity_after_translate_using_first_equation_of_motion(self):
        self.vehicle.velocity = 12
        self.fix_idm_acceleration(0.5)
        self.vehicle.translate(100)
        self.assertEqual(self.vehicle.velocity, 62)

    def test_should_update_position_after_translate_using_second_equation_of_motion(self):
        self.fix_idm_acceleration(0.5)
        self.vehicle.velocity = 10
        self.vehicle.position = 10.0
        self.vehicle.translate(10)
        self.assertEqual(self.vehicle.position, 135.0)

    def fix_idm_acceleration(self, acceleration):
        when(Idm).calculate_acceleration(self.vehicle, self.vehicle.leader()).thenReturn(acceleration)