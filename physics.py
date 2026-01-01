import euler_lag
import numpy as np
from calc_math import func
import matplotlib.pyplot as plt
import plottings
import points

# we use just 2 D

def polar_cart(vec):
    x = vec[0]*np.cos(vec[1])
    y = vec[1]*np.sin(vec[0])
    return np.array([x,y])

def cart_polar(vec):
    r = np.sqrt(vec[0]**2 + vec[1]**2)
    theta = np.arctan2(vec[1], vec[0])
    return np.array([r, theta])

def potential_energy(obj_pos):
    r = np.linalg.norm(obj_pos)
    if r == 0:
        return 0
    return -1/r
        