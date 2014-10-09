from Queue import Queue
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

         Also, in the case of the tests, it will not work with an instance of multiprocessing.Queue.
         It only works with Queue.Queue. This should be the first point of examination if snapshot relaying
         doesn't work in the multiprocess environment the production code is meant to run in.

         This is very strange. WHAT DOES PYTHON DO WHEN YOU ASSIGN A NEW INSTANCE OF A CLASS TO A VARIABLE
         THAT IT DOESN'T DO WHEN A VARIABLE IS NOT CREATED FOR THE INSTANCE??

        """
    def test_should_put_vehicle_snapshot_on_the_sim_queue_when_translation_event_is_fired(self):
        snapshots = Queue()
        _ = SnapshotRelay(snapshots)  # See notes about this line at the start of the method
        vehicle = Vehicle(0, mock())
        E_TRANSLATE.send(sender=vehicle)
        self.assertEqual(snapshots.get_nowait(), vehicle)