import sys
import numpy as np
from typing import Union
from .plottings import *

dt = 0.01

class point:
    pos : np.ndarray
    m : float
    q : float
    vel : np.ndarray
    acc : np.ndarray
    next: Union['point',None]

    def __init__(self,pos,m,q,v,a):
        self.m = m
        self.q = q
        self.pos = np.array(pos, dtype=float)
        self.vel = np.array(v, dtype=float)
        self.acc = np.array(a, dtype=float)
        # previous position used for velocity recomputation in Verlet integration
        self.prev_pos = np.array(self.pos, dtype=float)
        # default collision radius (can be overridden per-point)
        self.radius = 0.5
    
    
    @property
    def inv_mass(self):
        return 0 if self.m == 0 else 1/self.m

    def constraint(self,other,dist,stiffness):
        """Enforce distance constraint between self and other point."""
        delta = other.pos - self.pos
        d = np.linalg.norm(delta)
        if d == 0:
            return  # Avoid division by zero
        w1 = self.inv_mass
        w2 = other.inv_mass
        wsum = w1 + w2
        if wsum == 0:
            return
        difference = (d - dist) / d
        correction = 0.5 * difference * delta * stiffness
        self.pos += correction * w1 / wsum
        other.pos -= correction * w2/ wsum
        self.vel = (self.pos - self.prev_pos) / dt
        other.vel = (other.pos - other.prev_pos) / dt

    def collisions(self,other,rest_coeff): 
        """Handle elastic collision between self and other point.""" 
        delta = other.pos - self.pos 
        d = np.linalg.norm(delta) 
        if d == 0: return # Avoid division by zero 
        if d > self.radius + other.radius: return # No collision
        normal = delta / d
        overlap = self.radius + other.radius - d
        wsum = self.inv_mass + other.inv_mass
        if wsum > 0:
        # Move particles apart proportional to their mass
        # Anchor (m=0 -> inv_mass=0) won't move at all!
            self.pos -= normal * (overlap * self.inv_mass / wsum)
            other.pos += normal * (overlap * other.inv_mass / wsum)

        relative_velocity = self.vel - other.vel 
        vel_along_normal = np.dot(relative_velocity, normal) 
        if vel_along_normal > 0: return # Points are moving apart 
        impulse_magnitude = -(1 + rest_coeff) * vel_along_normal 
        impulse_magnitude /= (self.inv_mass + other.inv_mass) 
        impulse = impulse_magnitude * normal 
        self.vel += impulse * self.inv_mass
        other.vel -= impulse * other.inv_mass


class DistanceConstraint:
    def __init__(self, p1, p2, length,stiffness = 1.0):
        self.p1 = p1
        self.p2 = p2
        self.length = length
        self.stiffness = stiffness

    def solve(self):
        self.p1.constraint(self.p2, self.length,self.stiffness)

class wall:
    def __init__(self, p1, p2):
        self.p1 = np.array(p1, dtype=float)
        self.p2 = np.array(p2, dtype=float)
        self.dir = self.p2 - self.p1
        self.dir /= np.linalg.norm(self.dir)
        self.normal = np.array([-self.dir[1], self.dir[0]])

    def collisions(self, point: point, rest_coeff):
        to_point = point.pos - self.p1
        dist = np.dot(to_point, self.normal)
        if abs(dist) < point.radius:
            # Project point out of wall
            point.pos += self.normal * (point.radius - dist)
            # Reflect velocity
            vel_along_normal = np.dot(point.vel, self.normal)
            if vel_along_normal < 0:
                point.vel -= (1 + rest_coeff) * vel_along_normal * self.normal


def random_point(xlim, ylim, mrange, qrange, vrange, arange):
        """
        Generate a random point within given ranges.

        :param xlim: range for x position (min, max)
        :param ylim: range for y position (min, max)
        :param mrange: range for mass (min, max)
        :param qrange: range for charge (min, max)
        :param vrange: velocity range (min, max)
        :param arange: acceleration range (min, max)
        """
        import random
        positon = np.array([random.uniform(*xlim), random.uniform(*ylim)], dtype=float)
        mass = random.uniform(*mrange)
        charge = random.uniform(*qrange)
        velocity = np.array([random.uniform(*vrange), random.uniform(*vrange)], dtype=float)
        acceleration = np.array([random.uniform(*arange), random.uniform(*arange)], dtype=float)
        return point(positon, mass, charge, velocity, acceleration)

if __name__ == "__main__":
    pass