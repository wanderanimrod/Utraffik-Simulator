from models.traffic_models.idm import Idm
from models.traffic_models.shared_constants import min_clearance


class LaneChangeModel:

    lane_change_threshold = 0.1

    def __init__(self):
        pass

    @classmethod
    def vehicle_should_change_lane(cls, vehicle):
        if vehicle.acceleration < vehicle.max_acceleration:
            prospective_follower = vehicle.prospective_follower()
            if cls.__clearance_between(vehicle, prospective_follower) >= min_clearance:
                follower = vehicle.follower()
                lane_change_incentive = cls.__calculate_lane_change_incentive(vehicle, follower, prospective_follower)
                return True
        return False

    @classmethod
    def __calculate_lane_change_incentive(cls, requester, follower, prospective_follower):
        my_acc_gain = cls.__calculate_acceleration_gain(requester, requester.prospective_leader())
        prospective_follower_acc_gain = cls.__calculate_acceleration_gain(prospective_follower, requester)
        follower_acc_gain = cls.__calculate_acceleration_gain(follower, requester.leader())
        return my_acc_gain + requester.politeness * (prospective_follower_acc_gain + follower_acc_gain)

    @classmethod
    def __calculate_acceleration_gain(cls, gainer, leader):
        acceleration_before = gainer.acceleration
        acceleration_after = Idm.calculate_acceleration(gainer, leader)
        return acceleration_after - acceleration_before

    @classmethod
    def __clearance_between(cls, leader, follower):
        return leader.position - leader.length - follower.position