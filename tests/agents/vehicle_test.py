from unittest import TestCase

from mockito import mock, when, verify

from models.agents.vehicle import Vehicle
from models.agents.vehicle_factory import dummy_leader, dummy_follower
from models.traffic_models.idm import Idm
from models.traffic_models.lane_change_model import LaneChangeModel
from tests.helper import BetterMock, spy_on, expect


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
        when(self.vehicle).prospective_follower().thenReturn(self.mock_vehicle)
        self.assertEqual(self.vehicle.prospective_follower(), self.mock_vehicle)

    def test_should_get_prospective_leader_from_target_lane(self):
        when(self.vehicle).prospective_leader().thenReturn(self.mock_vehicle)
        self.assertEqual(self.vehicle.prospective_leader(), self.mock_vehicle)

    def test_should_get_follower_from_current_lane(self):
        when(self.vehicle).follower().thenReturn(self.mock_vehicle)
        self.assertEqual(self.vehicle.follower(), self.mock_vehicle)

    def test_should_get_leader_from_current_lane(self):
        when(self.vehicle).leader().thenReturn(self.mock_vehicle)
        self.assertEqual(self.vehicle.leader(), self.mock_vehicle)

    def test_should_update_velocity_after_translate_using_first_equation_of_motion(self):
        # when(self.vehicle).leader().thenReturn(dummy_leader)
        # when(self.vehicle).follower().thenReturn(dummy_follower)
        # when(self.vehicle).prospective_follower().thenReturn(dummy_follower)
        # when(self.vehicle).prospective_leader().thenReturn(dummy_leader)
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
        vehicle, new_lane, _ = self.translate_and_change_lane(self.vehicle)
        self.assertEqual(vehicle.lane, new_lane)

    def test_should_remove_itself_from_current_lane_after_lane_change(self):
        pass

    def dummy_function(self, car):
        print "DUMMY CALLED"
        print car

    def test_should_add_itself_to_target_lane_after_lane_change(self):
        vehicle, new_lane, _ = self.translate_and_change_lane(self.vehicle)
        verify(new_lane).add_vehicle(vehicle)

    def test_should_sth(self):
        lane = BetterMock()
        target_lane = BetterMock()
        spy_on(lane, 'next_lane').and_return(target_lane)
        vehicle = Vehicle(0, lane)
        vehicle.leader = lambda: dummy_leader
        vehicle.prospective_leader = lambda: dummy_leader
        vehicle.prospective_follower = lambda: dummy_follower
        vehicle.follower = lambda: dummy_follower
        lane_change_model = BetterMock()
        spy_on(lane_change_model, 'vehicle_should_change_lane').and_return(True)
        vehicle.translate(1)
        expect(lane, 'add_vehicle').to_have_been_called_with(vehicle)
        pass

    def test_should_verify(self):
        # lane = MyMock()
        # vehicle = Vehicle(lane)
        # verify(lane).remove_vehicle(self.vehicle)
        pass

    def fix_idm_acceleration(self, acceleration):
        when(Idm).calculate_acceleration(self.vehicle, self.vehicle.leader()).thenReturn(acceleration)

    def translate_and_change_lane(self, vehicle):
        when(LaneChangeModel).vehicle_should_change_lane(vehicle).thenReturn(True)
        when(vehicle).leader().thenReturn(dummy_leader)
        self.vehicle.translate(1)
        return vehicle, self.target_lane, self.lane