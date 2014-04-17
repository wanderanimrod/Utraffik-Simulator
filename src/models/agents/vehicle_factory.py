from models.agents.vehicle import Vehicle


class VehicleFactory:

    def __init__(self):
        pass

    @classmethod
    def make_dummy_leader(cls):
        leader = Vehicle(-1)
        leader.velocity = 33.3
        leader.position = 100000
        return leader
