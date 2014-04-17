from mockito import mock
from models.agents.vehicle import Vehicle


class VehicleFactory:

    def __init__(self):
        pass

    @classmethod
    def make_dummy_leader(cls):
        leader = Vehicle(-1, mock())
        leader.velocity = 33.3
        leader.position = 100000
        return leader

    @classmethod
    def make_dummy_follower(cls):
        follower = Vehicle(-2, mock())
        follower.desired_velocity = 0
        return follower