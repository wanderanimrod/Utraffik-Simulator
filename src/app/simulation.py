from multiprocessing import Process, Queue
from time import time

from redis import StrictRedis
import signal

from app.clock import Clock
from app.snapshot_relay import SnapshotRelay
from app.snapshot_writer import SnapshotWriter
from app.translator import Translator
from models.agents.vehicle import Vehicle
from models.network.lane import Lane
from models.network.two_lane_one_way_edge import TwoLaneOneWayEdge
from settings import SNAPSHOTS_DB, REDIS


def start_sub_sim(sub_network, sim_start_time):
    translator = Translator(sub_network)
    clock = Clock().start(at=sim_start_time)

    vehicle_snapshots = Queue()
    snapshot_writer_command_queue = Queue()
    _ = SnapshotRelay(vehicle_snapshots)
    writer = SnapshotWriter(vehicle_snapshots, snapshot_writer_command_queue)
    writer.start()

    while not translator.is_waiting:
        translator.sweep(clock)
        # Check for stop/pause commands and act accordingly

    snapshot_writer_command_queue.put(signal.SIGTERM)
    print "*" * 20, "Shutting down snapshot writer ...", "*" * 20
    writer.join()

    print "Sub-sim finished."


def run():
    clean_db()
    print "Sim starting..."
    sub_net_1 = load_network()
    sim_start_time = time()
    process = Process(target=start_sub_sim, args=(sub_net_1, sim_start_time))
    process.start()
    process.join()

    print "Sim finished!"


def clean_db():
    db = StrictRedis(host=REDIS['host'], port=REDIS['port'], db=SNAPSHOTS_DB)
    db.flushdb()


def load_network():
    edge = TwoLaneOneWayEdge(0, 10)
    lane_1 = Lane(0, edge)
    lane_2 = Lane(1, edge)
    Vehicle(0, lane_1)
    Vehicle(1, lane_2)
    return [edge]


def start():
    pass


def stop():
    # Interrupt the simulator and kill the processes
    pass


def pause():
    # Interrupt the sim and pause the clocks
    pass


# run()