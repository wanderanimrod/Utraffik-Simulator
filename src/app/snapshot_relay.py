from app.events.events import E_TRANSLATE


class SnapshotRelay:

    def __init__(self):
        self.__snapshots = []
        E_TRANSLATE.connect(self.__add_snapshot)

    def __add_snapshot(self, sender, **kwargs):
        self.__snapshots.append(sender)

    def get_all_snapshots(self):
        snapshots = self.__snapshots
        self.__snapshots = []
        return snapshots