from app.events.events import E_TRANSLATE


class SnapshotRelay:
    def __init__(self, snapshots):
        self._snapshots = snapshots
        E_TRANSLATE.connect(self._add_snapshot)

    def _add_snapshot(self, sender, **kwargs):
        time = kwargs['timestamp']
        self._snapshots.put(_take_snapshot_of(sender, time))


def _take_snapshot_of(vehicle, at):
    return {'id': vehicle.id, 'lane': vehicle.lane.id, 'position': vehicle.position,
            'velocity': vehicle.velocity, 'acc': vehicle.acceleration, 'time': at}