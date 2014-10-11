from multiprocessing import Queue
from unittest import TestCase

from mockito import mock

from app.events.events import E_TRANSLATE
from app.snapshot_relay import SnapshotRelay

from models.agents.vehicle import Vehicle


class SnapshotRelayTest(TestCase):

    """
        A note about this line: relay = SnapshotRelay(snapshots)
        The SnapshotRelay object will not put anything on its internal queue if when it is instantiated,
         the instance is not assigned to an variable.

         This is very strange. WHAT DOES PYTHON DO WHEN YOU ASSIGN A NEW INSTANCE OF A CLASS TO A VARIABLE
         THAT IT DOESN'T DO WHEN A VARIABLE IS NOT CREATED FOR THE INSTANCE??
        """
    def test_should_put_vehicle_snapshot_on_the_sim_queue_when_translation_event_is_received(self):
        snapshots = Queue()
        _ = SnapshotRelay(snapshots)  # See notes about this line at the start of the method

        mock_lane = mock()
        mock_lane.id = 10
        vehicle = Vehicle(0, mock_lane)

        E_TRANSLATE.send(sender=vehicle)

        expected_snapshot = {'acc': 0.0, 'position': 0.0, 'lane': mock_lane.id, 'id': 0, 'velocity': 0.0}
        self.assertEqual(snapshots.get(), expected_snapshot)