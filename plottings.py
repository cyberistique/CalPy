import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter
import numpy as np
from PIL import Image

def timeVScoordinate(time,q,qname="θ"):
    plt.figure(figsize=(10,4))
    plt.plot(time, q)
    plt.title(f"{qname}vs Time")
    plt.xlabel("Time (s)")
    plt.ylabel(f"{qname}")
    plt.grid(True)
    plt.show()

# Plot phase space (θ vs θ̇)
def phaseSpace(q,qdot,qname="θ", qdotname="θ̇*"):
    plt.figure(figsize=(5,5))
    plt.plot(q,qdot)
    plt.title(f"Phase Space ({qname} vs {qdotname})")
    plt.xlabel(f"{qname}")
    plt.ylabel(f"{qdotname}")
    plt.grid(True)
    plt.show()

def animate(system):
    fig, axis = plt.subplots()
    line, = axis.plot([], [],marker='o',linestyle='none')
    axis.set_xlim(-system.width/2,system.width/2)
    axis.set_ylim(-system.height/2,system.height/2)
    axis.set_aspect('equal')
    text_obj = axis.text(0.5, 0.5, '', transform=axis.transAxes)
    def update(frame):
        total_energy = system.update(frame)[1]
        xs = [p.pos[0] for p in system.points]
        ys = [p.pos[1] for p in system.points]
        line.set_data(xs, ys)
        text_obj.set_text(f'total_energy={total_energy:.2f}')
        return line, text_obj
    ani = animation.FuncAnimation(
        fig, update, frames=300, interval=20)
    plt.show()