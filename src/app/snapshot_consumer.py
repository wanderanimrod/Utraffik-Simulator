import threading

from redis import StrictRedis

db = StrictRedis(host='localhost', port=6379, db=0)
KILL_SIGNAL = -1


def run(queue):
    threading.Timer(0.1, write_snapshots_to_db, args=[queue]).start()


def write_snapshots_to_db(queue=None):
    snapshots = []
    while not queue.empty():
        item = queue.get()
        if item is KILL_SIGNAL:
            current_thread = threading.current_thread()
            current_thread.cancel()
        else:
            snapshots.append(item)

    _store_snapshots(snapshots)


def _store_snapshots(snapshots):
    pipeline = db.pipeline()
    for snapshot in snapshots:
        name = 'snapshot_%d' % snapshot['id']
        pipeline.hmset(name, snapshot)
    pipeline.execute()