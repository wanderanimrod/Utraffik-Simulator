from Queue import Queue

from app.events.events import E_TRANSLATE


vehicle_snapshots_queue = Queue()


class SnapshotRelay:
    def __init__(self):
        E_TRANSLATE.connect(self.__add_snapshot)

    @staticmethod
    def __add_snapshot(sender, **kwargs):
        vehicle_snapshots_queue.put(sender)
        print "Snapshot added for vehicle : ", sender