import numpy as np
from typing import Union
class point:
    pos : np.ndarray
    m : float
    q : float
    vel : np.ndarray
    next: Union['point',None]

    def __init__(self,pos,m,q,v):
        self.m = m
        self.q = q
        self.pos = np.array(pos, dtype=float)
        self.vel = np.array(v, dtype=float)
        # previous position used for velocity recomputation in Verlet integration
        self.prev_pos = np.array(self.pos, dtype=float)
        # default collision radius (can be overridden per-point)
        self.radius = 0.5
    
    @property
    def inv_mass(self):
        return 0 if self.m == 0 else 1/self.m

    def constraint(self,other,dist):
        """Enforce distance constraint between self and other point."""
        delta = other.pos - self.pos
        d = np.linalg.norm(delta)
        if d == 0:
            return  # Avoid division by zero
        difference = (d - dist) / d
        correction = 0.5 * difference * delta
        self.pos += correction
        other.pos -= correction

    def collisions(self,other,rest_coeff): 
        """Handle elastic collision between self and other point.""" 
        delta = other.pos - self.pos 
        d = np.linalg.norm(delta) 
        if d == 0: return # Avoid division by zero 
        normal = delta / d 
        relative_velocity = self.vel - other.vel 
        vel_along_normal = np.dot(relative_velocity, normal) 
        if vel_along_normal > 0: return # Points are moving apart 
        impulse_magnitude = -(1 + rest_coeff) * vel_along_normal 
        impulse_magnitude /= (1 / self.m + 1 / other.m) 
        impulse = impulse_magnitude * normal 
        self.vel += impulse / self.m 
        other.vel -= impulse / other.m

class chain:
    head : Union[point,None]
    tail : Union[point,None]
    length : int

    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def add_point(self,p:point):
        if self.head is None:
            self.head = p
            self.tail = p
        else:
            self.tail.next = p
            self.tail = p
        self.length += 1

    def stiffness(self):
        """Apply stiffness constraints along the chain."""
        p1 = self.head
        while p1 and p1.next:
            p2 = p1.next
            rest_length = np.linalg.norm(p2.pos - p1.pos)
            p1.constraint(p2, rest_length)
            p1 = p2
    