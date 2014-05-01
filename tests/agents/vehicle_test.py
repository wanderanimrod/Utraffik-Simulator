from unittest import TestCase

from mockito import mock, when, verify, never

from models.agents.vehicle import Vehicle
from models.agents.vehicle_factory import dummy_leader
from models.traffic_models.idm import Idm
from models.traffic_models.lane_change_model import LaneChangeModel


class VehicleTest(TestCase):

    def setUp(self):
        self.lane = mock()
        self.target_lane = mock()
        when(self.lane).next_lane().thenReturn(self.target_lane)
        self.vehicle = Vehicle(0, self.lane)
        self.mock_vehicle = mock()

    def test_should_be_created_with_position_zero(self):
        self.assertEqual(self.vehicle.position, 0)

    def test_should_add_itself_to_parent_lane_upon_instantiation(self):
        vehicle = Vehicle(0, self.lane)
        verify(self.lane).add_vehicle(vehicle)

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

    def test_should_update_acceleration_after_translate_to_acceleration_returned_by_idm(self):
        self.fix_idm_acceleration(0.6)
        self.vehicle.translate(1)
        self.assertEqual(self.vehicle.acceleration, 0.6)

    def test_should_change_lane_after_translate_if_lane_change_is_okay(self):
        vehicle, new_lane, _ = self.translate(self.vehicle, change_lane=True)
        self.assertEqual(vehicle.lane, new_lane)

    def test_should_remove_itself_from_current_lane_after_lane_change(self):
        vehicle, _, old_lane = self.translate(self.vehicle, change_lane=True)
        verify(old_lane).remove_vehicle(vehicle)

    def test_should_add_itself_to_target_lane_after_lane_change(self):
        vehicle, new_lane, _ = self.translate(self.vehicle, change_lane=True)
        verify(new_lane).insert_vehicle_at_current_position(vehicle)

    def test_should_not_change_lanes_if_no_lane_change_occurred_during_translate(self):
        vehicle, new_lane, old_lane = self.translate(self.vehicle, change_lane=False)
        verify(new_lane, never).insert_vehicle_at_current_position(vehicle)
        verify(old_lane, never).remove_vehicle(vehicle)
        self.assertEqual(vehicle.lane, old_lane)

    def test_should_go_to_the_end_of_current_lane_and_wait_if_next_translation_would_put_it_off_the_lane(self):
        lane_length = 10
        self.lane.length = lane_length
        vehicle, _, _ = self.translate(self.vehicle, change_lane=False, time_delta=6)
        self.assertEqual(vehicle.position, lane_length)

    def test_should_say_it_has_arrived_when_it_gets_to_the_end_of_the_lane(self):
        lane_length = 10
        self.lane.length = lane_length
        vehicle, _, _ = self.translate(self.vehicle, change_lane=False, time_delta=6)
        self.assertTrue(vehicle.arrived)

    def fix_idm_acceleration(self, acceleration):
        when(Idm).calculate_acceleration(self.vehicle, self.vehicle.leader()).thenReturn(acceleration)

    def translate(self, vehicle, change_lane=None, time_delta=1):
        when(LaneChangeModel).vehicle_should_change_lane(vehicle).thenReturn(change_lane)
        when(vehicle).leader().thenReturn(dummy_leader)
        vehicle.translate(time_delta)
        return vehicle, self.target_lane, self.lane