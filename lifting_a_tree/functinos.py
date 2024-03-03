from math import pi


def cone_vol(r : float, R : float, h : float) -> float:
    return h * pi / 3 * (r**2 + R*r + R**2)


def cone_point(r : float, R : float, h : float) -> float:
    h2 = h * R / (R - r)
    h1 = h2 - h
    
    p1 = h1 / 3 + h
    p2 = h2 / 3
    
    v2 = cone_vol(0, R, h2)
    v1 = cone_vol(0, r, h1)
    
    return (v2 * p2 - v1 * p1) / (v2 + v1)
    
"""
def motor_torque(v : float) -> float:
    """