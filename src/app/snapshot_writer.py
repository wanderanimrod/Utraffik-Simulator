from multiprocessing import Process
from time import sleep

from redis import StrictRedis
import signal

from settings import REDIS, SNAPSHOTS_DB

db = StrictRedis(host=REDIS['host'], port=REDIS['port'], db=SNAPSHOTS_DB)


class SnapshotWriter(Process):
    def __init__(self, snapshots_queue, command_queue):
        super(SnapshotWriter, self).__init__(target=self._write_snapshots_to_db, args=(snapshots_queue, command_queue))
        self.shutdown_requested = False

    def _write_snapshots_to_db(self, snapshots_queue=None, command_queue=None):
        while True:
            snapshots = []
            while not snapshots_queue.empty():
                item = snapshots_queue.get()
                snapshots.append(item)

            if snapshots:
                self._store_snapshots(snapshots)
                del snapshots[:]

            if not command_queue.empty():
                command = command_queue.get()
                if command is signal.SIGTERM:
                    break

            # sleep(0.1)

    @staticmethod
    def _store_snapshots(snapshots):
        pipeline = db.pipeline()
        for snapshot in snapshots:
            name = 'snapshot_%d:%f' % (snapshot['id'], snapshot['time'])
            pipeline.hmset(name, snapshot)
        pipeline.execute()

    # def shutdown(self):
    #     self._stop_signal.set()
    #     self.shutdown_requested = True
    #     print "*" * 20, "Signal is set = ", self.shutdown_requested, "*" * 20