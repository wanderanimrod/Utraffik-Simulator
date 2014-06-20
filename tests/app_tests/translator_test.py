from unittest import TestCase

from mockito import verify, mock

from app.events.events import E_END_OF_JOURNEY
from app.translator import Translator
from models.network.lane import Lane
from models.network.two_lane_one_way_edge import TwoLaneOneWayEdge


class TranslatorTest(TestCase):

    def setUp(self):
        self.translator_waiting_event = mock()

    def tearDown(self):
        """ Disconnect all receivers of the end of journey event so translators created in previously run tests do not
         receive events fired by vehicles belonging to translators of other tests.
        """
        E_END_OF_JOURNEY.receivers = []

    def test_should_be_waiting_when_all_assigned_vehicles_get_to_end_of_their_journeys(self):
        edge, vehicle_1, vehicle_2 = self.make_edge_with_mock_vehicles()
        translator = Translator([edge])
        vehicle_1.translate = lambda time_elapsed, time_now: E_END_OF_JOURNEY.send(sender=vehicle_1)
        vehicle_2.translate = lambda time_elapsed, time_now: E_END_OF_JOURNEY.send(sender=vehicle_2)
        translator.sweep(self.FakeClock(1))
        self.assertTrue(translator.is_waiting)

    def test_should_be_waiting_if_there_are_no_vehicles_on_the_assigned_edges_upon_instantiation(self):
        edge, _, _ = self.make_edge_without_vehicles()
        translator = Translator([edge])
        self.assertTrue(translator.is_waiting)

    def test_should_not_be_waiting_if_there_are_vehicles_to_translate_upon_instantiation(self):
        edge, _, _ = self.make_edge_with_mock_vehicles()
        translator = Translator([edge])
        self.assertFalse(translator.is_waiting)

    def test_sweep_should_translate_all_vehicles_on_given_edges_once(self):
        edge, vehicle_1, vehicle_2 = self.make_edge_with_mock_vehicles()
        translator = Translator([edge])
        translator.sweep(self.FakeClock(5))
        verify(vehicle_1, times=1).translate(5, 0)
        verify(vehicle_2, times=1).translate(5, 0)

    def test_should_pass_time_elapsed_directly_to_translate_function(self):
        edge, vehicle, _ = self.make_edge_with_mock_vehicles()
        translator = Translator([edge])
        translator.sweep(self.FakeClock(2))
        verify(vehicle).translate(2, 0)
        translator.sweep(self.FakeClock(4))
        verify(vehicle).translate(4, 0)

    def make_edge_without_vehicles(self):
        edge = TwoLaneOneWayEdge(0, 100)
        lane_1 = Lane(0, edge)
        lane_2 = Lane(1, edge)
        return edge, lane_1, lane_2

    def make_edge_with_mock_vehicles(self):
        edge, lane_1, lane_2 = self.make_edge_without_vehicles()
        first = mock()
        second = mock()
        lane_1.add_vehicle(first)
        lane_2.add_vehicle(second)
        return edge, first, second

    class FakeClock():

        def __init__(self, fixed_time_elapsed):
            self.fixed_time_elapsed = fixed_time_elapsed

        def time_elapsed(self):
            return self.fixed_time_elapsed

        def now(self):
            return 0