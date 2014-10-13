from redis import StrictRedis

db = StrictRedis(host='localhost', port=6379, db=0)
KILL_SIGNAL = -1


def _store_snapshots(snapshots):
    pipeline = db.pipeline()
    for snapshot in snapshots:
        name = 'snapshot_%d' % snapshot['id']
        pipeline.hmset(name, snapshot)
    pipeline.execute()


def run(queue):
    kill = False
    while True:
        snapshots = []
        while not queue.empty():
            item = queue.get()
            kill = True if item is KILL_SIGNAL else snapshots.append(item)

        _store_snapshots(snapshots)

        if kill:
            break

