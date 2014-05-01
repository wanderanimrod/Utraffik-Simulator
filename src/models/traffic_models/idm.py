from models.traffic_models.shared_constants import min_clearance


# FIXME: Shouldn't really be a class.
class Idm:
    T = 1.67
    delta = 4.0

    def __init__(self):
        pass

    # Variable names used as described in Wikipedia entry on IDM
    @classmethod
    def calculate_acceleration(cls, requester, leader):
        if not requester.desired_velocity: return 0.0
        v = requester.velocity
        a = requester.max_acceleration
        b = requester.desired_deceleration
        delta_v = v - leader.velocity
        s = leader.position - requester.position - leader.length
        s_star = min_clearance + (v * cls.T) + ((v * delta_v) / (2 * (a * b) ** 0.5))
        return a * (1 - (v / requester.desired_velocity) ** cls.delta - (s_star / s) ** 2)