import numpy as np
import calc_math as cm
from plottings import plot_trajectory
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
    pendulum = cm.func(
    function_ = lambda t, theta, omega, g, L: np.array([
        omega,
        -(g/L) * np.sin(theta)
    ]),
    variables=["t","theta","omega"],
    max_derivative=0,
    constants={"g": 9.81, "L": 1.0}
)

    traj = integrate_rk4(pendulum.functions[0], y0=[1, 0], t0=0, dt=0.01, steps=1000)


    # printing first few points
    for t, y in traj[995:]:
        print(t, y)