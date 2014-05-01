from models.traffic_models.idm import Idm
from models.traffic_models.shared_constants import min_clearance


# FIXME: Shouldn't really be a class. A module with methods is just fine!
class LaneChangeModel:

    __lane_change_threshold = 0.1

    def __init__(self):
        pass

    @classmethod
    def vehicle_should_change_lane(cls, requester):
        if requester.acceleration < requester.max_acceleration:
            if cls.__clearance_between(requester, requester.prospective_follower()) >= min_clearance:
                incentive = cls.__calculate_lane_change_incentive(requester)
                if incentive > cls.__lane_change_threshold:
                    return True
        return False

    @classmethod
    def __calculate_lane_change_incentive(cls, requester):
        requester_acc_gain = cls.__acc_delta_for(requester, requester.prospective_leader())
        prospective_follower_acc_loss = cls.__acc_delta_for(requester.prospective_follower(), requester)
        follower_acc_gain = cls.__acc_delta_for(requester.follower(), requester.leader())
        return requester_acc_gain + requester.politeness * (prospective_follower_acc_loss + follower_acc_gain)

    @classmethod
    def __acc_delta_for(cls, gainer, leader):
        acceleration_before = gainer.acceleration
        acceleration_after = Idm.calculate_acceleration(gainer, leader)
        return acceleration_after - acceleration_before

    @classmethod
    def __clearance_between(cls, leader, follower):
        return leader.position - leader.length - follower.position