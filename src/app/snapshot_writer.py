import threading
from time import sleep

from redis import StrictRedis
from settings import REDIS, SNAPSHOTS_DB

db = StrictRedis(host=REDIS['host'], port=REDIS['port'], db=SNAPSHOTS_DB)


class SnapshotWriter(threading.Thread):

    def __init__(self, snapshots_queue):
        super(SnapshotWriter, self).__init__(target=self._write_snapshots_to_db, args=(snapshots_queue,))
        self._stop_signal = threading.Event()

    def _write_snapshots_to_db(self, queue=None):
        while True:
            snapshots = []
            while not queue.empty():
                item = queue.get()
                snapshots.append(item)

            self._store_snapshots(snapshots)

            sleep(0.1)  # Sleep periodically to avoid 100% CPU consumption

            if self._stop_signal.is_set():
                break

    @staticmethod
    def _store_snapshots(snapshots):
        pipeline = db.pipeline()
        for snapshot in snapshots:
            name = 'snapshot_%d' % snapshot['id']
            pipeline.hmset(name, snapshot)
        pipeline.execute()

    def shutdown(self):
        self._stop_signal.set()

    def wait_for_work_to_end(self, timeout=None):
        self._stop_signal.wait(timeout=timeout)
