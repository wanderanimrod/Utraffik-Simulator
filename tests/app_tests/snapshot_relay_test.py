from unittest import TestCase

from mockito import mock

from app.events.events import E_TRANSLATE
from app.snapshot_relay import SnapshotRelay
from models.agents.vehicle import Vehicle


class SnapshotRelayTest(TestCase):

    def setUp(self):
        self.relay = SnapshotRelay()
        self.vehicle_1 = Vehicle(0, mock())
        self.vehicle_2 = Vehicle(1, mock())

    def test_should_keep_vehicle_snapshots_for_further_processing(self):
        E_TRANSLATE.send(sender=self.vehicle_1)
        E_TRANSLATE.send(sender=self.vehicle_2)
        self.assertEqual(self.relay.get_all_snapshots(), [self.vehicle_1, self.vehicle_2])

    def test_should_remove_vehicle_all_snapshots_after_they_have_been_fetched(self):
        E_TRANSLATE.send(sender=self.vehicle_1)
        self.relay.get_all_snapshots()
        self.assertEqual(self.relay.get_all_snapshots(), [])