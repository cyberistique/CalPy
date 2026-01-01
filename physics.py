from .points import point,wall,DistanceConstraint,random_point
import numpy as np
from typing import Union
from .plottings import *
from .formulas import force,potential_energy,kinetic_energy

dt = 0.01  # Time step
class System:
    def __init__(self, gravity= False,coulomb=False,earth = False, coeff_restitution= 0.9, w=20, h=20):
        self.points = []
        self.walls = [
            wall([-w/2, -h/2], [w/2, -h/2]),
            wall([w/2, -h/2], [w/2, h/2]),
            wall([w/2, h/2], [-w/2, h/2]),
            wall([-w/2, h/2], [-w/2, -h/2])
        ]
        self.gravity = gravity
        self.coulomb = coulomb
        self.earth = earth
        self.coeff_restitution = coeff_restitution
        self.width = w
        self.height = h
        self.constraints = []
        self.totalenergy = 0

    def add_point(self, point: point):
        self.points.append(point)

    def update(self,frame):
        self.totalenergy = 0
        for p in self.points:
            p.acc[:] = 0
            if self.earth and p.inv_mass > 0:
                p.acc += force(p.pos, p.m, p.q, 'earth') * p.inv_mass
            if self.coulomb and p.q != 0:
                for other in self.points:
                    if other is not p and other.q != 0:
                        p.acc += force(other.pos - p.pos, p.m, p.q * other.q, 'electrostatic') * p.inv_mass
                        self.totalenergy += potential_energy(other.pos - p.pos, p.m, p.q * other.q, 'electrostatic') * 0.5  # each pair counted twice
            if self.gravity and p.inv_mass > 0:
                for other in self.points:
                    if other is not p and other.inv_mass != 0:
                        p.acc += force(other.pos - p.pos, p.m*other.m, q=0, type='gravity') * p.inv_mass
                        self.totalenergy += potential_energy(other.pos - p.pos, p.m*other.m, q=0, type='gravity') * 0.5  # each pair counted twice
            self.totalenergy += kinetic_energy(p.vel, p.m)
            p.vel += p.acc*dt
            p.prev_pos = np.array(p.pos, dtype=float)
            p.pos += p.vel*dt

        for _ in range(5):
            for c in self.constraints:
                c.solve()

        # Handle collisions
        for i in range(len(self.points)):
            for j in range(i + 1, len(self.points)):
                self.points[i].collisions(self.points[j], self.coeff_restitution)
            for wall in self.walls:
                wall.collisions(self.points[i], self.coeff_restitution)
        return self.points,self.totalenergy


if __name__ == "__main__":
    from .plottings import animate
    import random

    # 1. Initialize System (Gravity on, medium restitution)
    sys = System( coeff_restitution=1.0, w=20, h=20)

    # 2. Define 5 particles with random properties
    for i in range(10):

        p = random_point(xlim=(-8,8), ylim=(-8,8), mrange=(0.5,2.0), qrange=(-1e-5,1e-5), vrange=(-10,10), arange=(-1,1))
        p.radius = 0.25
        
        sys.add_point(p)

    # 3. Add one fixed "obstacle" in the middle (mass = 0)
    anchor = point(pos=[0, -2], m=0, q=0, v=[0, 0], a=[0, 0])

    anchor.radius = 0.25
    sys.add_point(anchor)

    print(f"Simulation started with {len(sys.points)} particles.")
    animate(sys)