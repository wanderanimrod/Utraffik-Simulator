from mockito import mock
from models.agents.vehicle import Vehicle


class VehicleFactory:

    def __init__(self):
        pass

    @staticmethod
    def make_dummy_leader():
        leader = Vehicle(-1, mock())
        leader.velocity = 33.3
        leader.position = 100000
        return leader

    @staticmethod
    def make_dummy_follower():
        follower = Vehicle(-2, mock())
        follower.desired_velocity = 0
        return follower


dummy_leader = VehicleFactory.make_dummy_leader()
dummy_follower = VehicleFactory.make_dummy_follower()