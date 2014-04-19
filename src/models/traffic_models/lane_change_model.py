from models.agents.vehicle import Vehicle
from models.traffic_models.idm import Idm


class LaneChangeModel:

    def __init__(self):
        pass

    @staticmethod
    def vehicle_should_change_lane(vehicle):
        pass

    @classmethod
    def __calculate_lane_change_incentive(cls, requester, follower, prospective_follower):
        prospective_leader = requester.lane.get_prospective_leader(requester)
        my_acc_gain = cls.__calculate_acceleration_gain(requester, prospective_leader)
        prospective_follower_acc_gain = cls.__calculate_acceleration_gain(prospective_follower, requester)
        leader = requester.lane.get_leader(requester)
        follower_acc_gain = cls.__calculate_acceleration_gain(follower, leader)
        return my_acc_gain + requester.politeness * (prospective_follower_acc_gain + follower_acc_gain)

    @classmethod
    def __calculate_acceleration_gain(cls, gainer, leader):
        acceleration_before = gainer.acceleration
        acceleration_after = Idm.calculate_acceleration(gainer, leader)
        return acceleration_after - acceleration_before