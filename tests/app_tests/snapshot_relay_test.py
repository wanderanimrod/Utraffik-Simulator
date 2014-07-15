from Queue import Queue
from unittest import TestCase
from mockito import mock
from app.events.events import E_TRANSLATE
from app.snapshot_relay import SnapshotRelay, vehicle_snapshots_queue, ReferenceRelay
from models.agents.vehicle import Vehicle


class SnapshotRelayTest(TestCase):

    def test_should_put_vehicle_snapshot_on_the_sim_queue_when_translation_event_is_fired(self):
        SnapshotRelay()
        vehicle = Vehicle(0, mock())
        E_TRANSLATE.send(sender=vehicle)
        self.assertEqual(vehicle_snapshots_queue.get_nowait(), vehicle)

    def test_reference_relay(self):
        q = Queue()
        relay = ReferenceRelay(q)
        vehicle = Vehicle(0, mock())
        E_TRANSLATE.send(sender=vehicle)
        self.assertEqual(q.get_nowait(), vehicle)