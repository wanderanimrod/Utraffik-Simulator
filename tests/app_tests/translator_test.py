from unittest import TestCase

from mockito import verify, mock, never

from app.events import events
from app.translator import Translator
from models.network.lane import Lane
from models.network.two_lane_one_way_edge import TwoLaneOneWayEdge


class TranslatorTest(TestCase):

    def setUp(self):
        self.translator_waiting_event = mock()
        events.E_TRANSLATOR_WAITING.send = self.translator_waiting_event.send

    def test_should_fire_waiting_event_if_there_are_no_vehicles_on_the_assigned_edges_upon_instantiation(self):
        edge, _, _ = self.make_edge_without_vehicles()
        translator = Translator([edge])
        verify(self.translator_waiting_event).send(sender=translator)

    def test_should_not_fire_waiting_event_if_there_are_vehicles_to_translate_upon_instantiation(self):
        edge, _, _ = self.make_edge_with_mock_vehicles()
        translator = Translator([edge])
        verify(self.translator_waiting_event, never).send(sender=translator)

    def test_sweep_should_translate_all_vehicles_on_given_edges_once(self):
        edge, vehicle_1, vehicle_2 = self.make_edge_with_mock_vehicles()
        translator = Translator([edge])
        translator.sweep(5)
        verify(vehicle_1, times=1).translate(5)
        verify(vehicle_2, times=1).translate(5)

    def test_should_use_sim_time_as_time_delta_for_translate_during_first_call_to_sweep(self):
        edge, vehicle, _ = self.make_edge_with_mock_vehicles()
        translator = Translator([edge])
        sim_time = 2
        translator.sweep(sim_time)
        verify(vehicle).translate(sim_time)

    def test_should_use_difference_between_sim_time_and_last_translate_time_as_time_delta_for_translate(self):
        edge, vehicle, _ = self.make_edge_with_mock_vehicles()
        translator = Translator([edge])
        translator.sweep(2)
        translator.sweep(5)
        verify(vehicle).translate(5 - 2)

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