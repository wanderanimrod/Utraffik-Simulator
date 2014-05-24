from multiprocessing import Process
from time import time, sleep

from app.clock import Clock
from app.translator import Translator
from models.agents.vehicle import Vehicle
from models.network.lane import Lane
from models.network.two_lane_one_way_edge import TwoLaneOneWayEdge


def start_translator(sub_network, sim_start_time):
    translator = Translator(sub_network)
    clock = Clock().start(at=sim_start_time)
    while not translator.is_waiting:
        translator.sweep(clock.time_elapsed())


def run():
    sub_net_1 = load_network()
    sim_start_time = time()
    process = Process(target=start_translator, args=(sub_net_1, sim_start_time))
    process.start()
    start = time()
    while time() - start < 16:
        print "Checking for output"
        sleep(1)
    process.join()


def load_network():
    edge = TwoLaneOneWayEdge(0, 100)
    lane_1 = Lane(0, edge)
    lane_2 = Lane(1, edge)
    Vehicle(0, lane_1)
    Vehicle(0, lane_2)
    return [edge]