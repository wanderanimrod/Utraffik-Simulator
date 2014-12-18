import threading
from time import sleep

from redis import StrictRedis

db = StrictRedis(host='localhost', port=6379, db=0)
KILL_SIGNAL = -1


def run(queue):
    threading.Thread(target=write_snapshots_to_db, args=(queue,)).start()


def write_snapshots_to_db(queue=None):
    while True:
        kill = False
        snapshots = []
        while not queue.empty():
            item = queue.get()
            kill = True if item is KILL_SIGNAL else snapshots.append(item)

        _store_snapshots(snapshots)

        sleep(0.1)  # Sleep periodically to avoid 100% CPU time

        if kill:
            break


def _store_snapshots(snapshots):
    pipeline = db.pipeline()
    for snapshot in snapshots:
        name = 'snapshot_%d' % snapshot['id']
        pipeline.hmset(name, snapshot)
    pipeline.execute()