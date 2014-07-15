from Queue import Queue

from app.events.events import E_TRANSLATE


class SnapshotRelay:
    def __init__(self, snapshots):
        self.__snapshots = snapshots
        E_TRANSLATE.connect(self.__add_snapshot)

    def __add_snapshot(self, sender, **kwargs):
        self.__snapshots.put(sender)