from unittest import TestCase

from mockito import mock

from app.events.events import E_TRANSLATE
from app.vehicle_snapshot_relay import SnapshotRelay
from models.agents.vehicle import Vehicle


class SnapshotRelayTest(TestCase):

    def test_should_keep_vehicle_snapshots_for_further_processing(self):
        relay = SnapshotRelay()
        vehicle_1 = Vehicle(0, mock())
        vehicle_2 = Vehicle(1, mock())
        E_TRANSLATE.send(sender=vehicle_1)
        E_TRANSLATE.send(sender=vehicle_2)
        self.assertEqual(relay.all_snapshots(), [vehicle_1, vehicle_2])