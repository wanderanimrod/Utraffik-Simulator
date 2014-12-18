from multiprocessing import Queue
from time import sleep
from unittest import TestCase

from redis import StrictRedis


from app.snapshot_consumer import KILL_SIGNAL
from app import snapshot_consumer


class SnapshotConsumerTest(TestCase):
    def setUp(self):
        self.snapshot_queue = Queue()
        self.db = StrictRedis(host='localhost', port=6379, db=0)

    def test_should_read_snapshots_from_queue_periodically_and_write_them_to_redis_db(self):
        snapshot_one = {'id': 1, 'other_details': 'Vehicle data'}
        snapshot_two = {'id': 2, 'other_details': 'Vehicle data'}
        [self.snapshot_queue.put(item) for item in [snapshot_one, snapshot_two, KILL_SIGNAL]]

        snapshot_consumer.run(self.snapshot_queue)

        sleep(0.5)  # Wait for snapshot writer thread to finish
        snapshots_in_db = [self.db.hgetall(key) for key in ['snapshot_1', 'snapshot_2']]
        expected_snapshots = [self.stringify_id_for(snapshot) for snapshot in [snapshot_one, snapshot_two]]

        self.assertListEqual(snapshots_in_db, expected_snapshots)

    def test_should_stop_reading_snapshots_if_kill_signal_is_put_on_queue(self):
        self.snapshot_queue.put(KILL_SIGNAL)
        snapshot_consumer.run(self.snapshot_queue)
        self.assertTrue(True)  # Tests that we get here

    def stringify_id_for(self, snapshot):
        snapshot.update({'id': str(snapshot['id'])})
        return snapshot

    def tearDown(self):
        self.db.delete('snapshot_1', 'snapshot_2')


