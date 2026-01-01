🧮 CalPy
=========

A Modular Particle Physics Simulation Engine in Python
--------
CalPy is a lightweight, extensible physics simulation engine for modeling the dynamics of point particles under classical forces such as gravity and electrostatics. It is designed for experimentation, visualization, and learning in computational physics.

The engine supports modular force models, numerical integrators, and animated visualizations using NumPy and Matplotlib.

✨ Features

🔹 Point-particle dynamics in 2D space

🔹 Classical force models:

Gravitational force

Electrostatic (Coulomb) force

🔹 Modular architecture (forces, integrators, plotting separated)

🔹 Numerical time integration (Euler-based)

🔹 Animated visualization of particle motion

🔹 Easily extensible for new forces and integrators

📁 Project Structure
```CalPy/
├── Physics.py        # Core physics engine
├── points.py         # Particle class and state definitions
├── formulas.py       # Force equations (gravity, electrostatics)
├── integrator.py     # Numerical integration methods
├── plottings.py      # Visualization and animation utilities
└── main.py           # Example simulation runner
```
🚀 Getting Started
--------
Requirements
```
Python 3.9+
NumPy
Matplotlib
```

Install dependencies:
```
pip install numpy matplotlib
```
Running a Simulation
--------
```
from Calc_math.Physics import System
from Calc_math.points import random_point, point
from Calc_math.plottings import animate


def main():
    sim = System(coeff_restitution=1.0, w=20, h=20)

    # 2. Define 10 particles with random properties
    for i in range(10):
        p = random_point(xlim=(-8, 8), ylim=(-8, 8), mrange=(0.5, 2.0), qrange=(-1e-5, 1e-5), vrange=(-10, 10), arange=(-1, 1))
        p.radius = 0.25
        sim.add_point(p)

    # 3. Add one fixed "obstacle" in the middle (mass = 0)
    anchor = point(pos=[0, -2], m=0, q=0, v=[0, 0], a=[0, 0])

    anchor.radius = 0.25
    sim.add_point(anchor)

    print(f"Simulation started with {len(sim.points)} particles.")
    animate(sim)


if __name__ == "__main__":
    main()
```

This will run a default simulation of interacting particles and display an animated visualization of their motion.

📊 Example Output
--------

![giphy](https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExMTI2YzZ3am5ramZxeHl2ZGpxbDlpOWxqbm9hdWFkbHZ4eTM5NG9tbSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/O9DO7khSB6bvo539gk/giphy.gif)

🧠 Physics Model
--------
Each particle is defined by:

- Position
- Velocity
- Mass
- Charge

At each timestep:

- Net force on each particle is computed
- Acceleration is calculated using Newton’s laws (future functionality will have option to use lagrangian mechanics for acceleration calcultation)
- Particle states are updated via numerical integration
- Positions are visualized dynamically

📌 Planned Improvements

- ⚡ Energy conservation diagnostics
- 🧲 External field support (uniform E/B fields)
- 🖥️ Command-line interface (CLI)
- 🌐 Web-based interactive interface (Flask)
- 🎥 Export animations to GIF or MP4

🎓 Motivation

This project was built to explore computational physics, numerical methods, and simulation design, bridging concepts from classical mechanics with practical scientific computing.






