import matplotlib.pyplot as plt

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