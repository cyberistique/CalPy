import numpy as np
from . import calc_math as cm
from .plottings import timeVScoordinate, phaseSpace
from .euler_lag import Lagrangian
from . import plottings

def to_array(y):
    """Convert scalar or list to numpy array."""
    if isinstance(y, (int, float)):
        return np.array([y], dtype=float)
    return np.array(y, dtype=float)

def integrate_euler(f, y0, t0, dt, steps):
    """
    Euler ODE Integrator
    f: function f(t, y) returning derivative
    y0: initial state (scalar or list/array)
    """
    y = to_array(y0)
    t = t0

    traj = [(t, y.copy())]

    for _ in range(steps):
        dydt = to_array(f(t, y))
        y = y + dt * dydt
        t += dt
        traj.append((t, y.copy()))

    return traj

def integrate_rk4(f, y0, t0, dt, steps):
    """
    Runge–Kutta 4 Integrator (standard for physics)
    """
    y = to_array(y0)
    t = t0

    traj = [(t, y.copy())]

    for _ in range(steps):

        k1 = to_array(f(t,*y))
        k2 = to_array(f(t+dt/2.0,  *y + dt*k1/2.0))
        k3 = to_array(f(t+dt/2.0,  *y + dt*k2/2.0))
        k4 = to_array(f(t+dt,     *y + dt*k3))

        y = y + dt*(k1 + 2*k2 + 2*k3 + k4) / 6.0
        t += dt

        traj.append((t, y.copy()))

    return traj



if __name__ == "__main__":
    L_obj = lambda x, xdot, m, g,k: 0.5*m*xdot**2-0.5*k*x**2
    lag = Lagrangian(L_obj, variables=("x","xdot"),constants={"m":1.0,"g":9.8,"k":0.5},damper=0)

    q = 0        # initial angle
    qdot = 100     # initial angular velocity
    dt = 0.01
    steps = 2000

    trajectory = []

    trajectory = integrate_rk4(lag.qddot, [q, qdot], 0, dt, steps)

    print("Final state:", q, qdot)

# Extract arrays for plotting
    angles = [s[0] for s in trajectory]
    vels   = [s[1] for s in trajectory]
    time   = np.arange(len(trajectory)) * dt

    plottings.timeVScoordinate(time, angles, qname="x")
    plottings.phaseSpace(angles, vels, qname="x", qdotname="xdot")
