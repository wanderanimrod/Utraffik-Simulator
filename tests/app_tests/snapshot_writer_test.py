from multiprocessing import Queue
from unittest import TestCase

from redis import StrictRedis

from app.snapshot_writer import SnapshotWriter
from settings import SNAPSHOTS_DB, REDIS


class SnapshotConsumerTest(TestCase):
    def setUp(self):
        self.snapshot_queue = Queue()
        self.db = StrictRedis(host=REDIS['host'], port=REDIS['port'], db=SNAPSHOTS_DB)

    def test_should_read_snapshots_from_queue_periodically_and_write_them_to_redis_db(self):
        snapshot_one = {'id': 1, 'other_details': 'Vehicle data'}
        snapshot_two = {'id': 2, 'other_details': 'Vehicle data'}
        [self.snapshot_queue.put(item) for item in [snapshot_one, snapshot_two]]

        writer = SnapshotWriter(self.snapshot_queue)
        writer.start()

        writer.wait_for_work_to_end(timeout=0.3)
        writer.shutdown()

        snapshots_in_db = [self.db.hgetall(key) for key in ['snapshot_1', 'snapshot_2']]
        expected_snapshots = [self.stringify_id_for(snapshot) for snapshot in [snapshot_one, snapshot_two]]

        self.assertListEqual(snapshots_in_db, expected_snapshots)

    def test_should_stop_reading_snapshots_if_shutdown_is_requested(self):
        writer = SnapshotWriter(self.snapshot_queue)
        writer.start()
        writer.shutdown()
        self.assertTrue(True)  # Tests that we get here

    def stringify_id_for(self, snapshot):
        snapshot.update({'id': str(snapshot['id'])})
        return snapshot

    def tearDown(self):
        self.db.delete('snapshot_1', 'snapshot_2')


