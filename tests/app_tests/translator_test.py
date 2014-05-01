from unittest import TestCase

from mockito import verify, mock, never

from app.events import events
from app.translator import Translator
from models.agents.vehicle import Vehicle
from models.network.lane import Lane
from models.network.two_lane_one_way_edge import TwoLaneOneWayEdge


class TranslatorTest(TestCase):

    def setUp(self):
        self.translator_waiting_event = mock()
        events.E_TRANSLATOR_WAITING.send = self.translator_waiting_event.send

    def xtest_should_translate_all_vehicles_on_given_edges_until_they_reach_their_destinations(self):
        edge, vehicle_1, vehicle_2 = self.make_edge_with_vehicles()
        translator = Translator([edge])
        translator.run()
        while not translator.waiting():
            continue
        self.assertTrue(vehicle_1.arrived)
        self.assertTrue(vehicle_2.arrived)

    def test_should_fire_waiting_event_if_there_are_no_vehicles_on_the_assigned_edges_upon_instantiation(self):
        edge, _, _ = self.make_edge_without_vehicles()
        translator = Translator([edge])
        verify(self.translator_waiting_event).send(sender=translator)

    def test_should_not_fire_waiting_event_if_there_are_vehicles_to_translate_upon_instantiation(self):
        edge, _, _ = self.make_edge_with_vehicles()
        translator = Translator([edge])
        verify(self.translator_waiting_event, never).send(sender=translator)

    def make_edge_without_vehicles(self):
        edge = TwoLaneOneWayEdge(0, 100)
        lane_1 = Lane(0, edge)
        lane_2 = Lane(1, edge)
        return edge, lane_1, lane_2

    def make_edge_with_vehicles(self):
        edge, lane_1, lane_2 = self.make_edge_without_vehicles()
        vehicle_1 = Vehicle(0, lane_1)
        vehicle_2 = Vehicle(1, lane_2)
        return edge, vehicle_1, vehicle_2