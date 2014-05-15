from multiprocessing import Queue, Process

from app.translator import Translator
from models.agents.vehicle import Vehicle
from models.network.lane import Lane
from models.network.two_lane_one_way_edge import TwoLaneOneWayEdge


vehicles_queue_1 = Queue()


def start_translator(sub_network, vehicles_queue):
    translator = Translator(sub_network)
    while not translator.is_waiting:
        translator.sweep(10)  # TODO Figure out sim timing


def run():
    sub_net_1 = load_network()
    start_sim_clock()
    process = Process(target=start_translator, args=(sub_net_1, vehicles_queue_1))
    process.start()
    process.join()


def load_network():
    # TODO Should load from network specification files or graph DB.
    edge = TwoLaneOneWayEdge(0, 100)
    lane_1 = Lane(0, edge)
    lane_2 = Lane(1, edge)
    Vehicle(0, lane_1)
    Vehicle(0, lane_2)
    return [edge]


def start_sim_clock():
    pass
