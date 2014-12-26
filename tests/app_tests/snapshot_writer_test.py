from multiprocessing import Queue
from time import sleep
from unittest import TestCase

from redis import StrictRedis

import settings


PROD_SNAPSHOTS_DB = settings.SNAPSHOTS_DB
settings.SNAPSHOTS_DB = 10

from app.snapshot_writer import SnapshotWriter
from settings import SNAPSHOTS_DB, REDIS


class SnapshotWriterTest(TestCase):
    def setUp(self):
        self.snapshot_queue = Queue()
        self.db = StrictRedis(host=REDIS['host'], port=REDIS['port'], db=SNAPSHOTS_DB)
        self.writer = SnapshotWriter(self.snapshot_queue)

    def test_should_read_snapshots_from_queue_periodically_and_write_them_to_redis_db(self):
        self.writer.start()

        snapshot_one = {'id': 1, 'other_details': 'Vehicle data', 'time': 1.0}
        snapshot_two = {'id': 2, 'other_details': 'Vehicle data', 'time': 1.0}
        [self.snapshot_queue.put(item) for item in [snapshot_one, snapshot_two]]

        sleep(0.3)
        self.writer.shutdown()

        snapshots_in_db = [self.db.hgetall(key) for key in ['snapshot_1:1.000000', 'snapshot_2:1.000000']]
        expected_snapshots = [self.redisify_snapshot(snapshot) for snapshot in [snapshot_one, snapshot_two]]

        self.assertListEqual(snapshots_in_db, expected_snapshots)

    def test_should_write_snapshot_with_key_a_concatenation_of_vehicle_id_and_time_stamp_to_six_decimal_places(self):
        self.writer.start()

        snapshot = {'id': 1, 'other_details': 'Vehicle data', 'time': 1.123459881213}
        self.snapshot_queue.put(snapshot)

        sleep(0.1)
        self.writer.shutdown()

        self.assertTrue('snapshot_1:1.123460' in self.db.keys("*"))

    def test_should_stop_reading_snapshots_if_shutdown_is_requested(self):
        writer = SnapshotWriter(self.snapshot_queue)
        writer.start()
        writer.shutdown()
        self.assertTrue(True)  # Tests that we get here

    def redisify_snapshot(self, snapshot):
        snapshot.update({'id': str(snapshot['id']), 'time': "%.1f" % snapshot['time']})
        return snapshot

    def tearDown(self):
        for key in self.db.keys("*"):
            self.db.delete(key)


settings.SNAPSHOTS_DB = PROD_SNAPSHOTS_DB