from models.agents.vehicle import Vehicle


class Idm:
    T = 1.67
    delta = 4.0
    
    def __init__(self):
        pass

    # Variable names used as described in Wikipedia entry on IDM
    @classmethod
    def calculate_acceleration(cls, follower, leader):
        if not follower.desired_velocity: return 0.0
        v = follower.velocity
        a = follower.max_acceleration
        b = follower.desired_deceleration
        delta_v = v - leader.velocity
        s = leader.position - follower.position - leader.length
        s_star = Vehicle.min_clearance + (v * cls.T) + ((v * delta_v) / (2 * (a * b) ** 0.5))
        return a * (1 - (v / follower.desired_velocity) ** cls.delta - (s_star / s) ** 2)