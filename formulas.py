import numpy as np
k = 9e9  # Coulomb's constant
G = 6.67430e-11  # Gravitational constant
g = 9.8
point_list = []
def potential_energy(r,m,q,type,K=0):
    r = np.linalg.norm(r)
    if type == 'gravity':
        return -G * m / r  # Gravitational potential energy
    elif type == 'electrostatic':
        return k * q / r  # Electrostatic potential energy
    elif type == 'spring':
        return 0.5 * K * r**2  # Spring potential energy
    elif type == 'earth':
        return m * g * r
    else:
        raise ValueError("Unknown interaction type")

def kinetic_energy(v, m):
    return 0.5 * m * np.dot(v, v)

def force(r,m,q,type,K=0):
    r_norm = np.linalg.norm(r)
    if r_norm == 0:
        return np.zeros_like(r)  # Avoid division by zero
    r_hat = r / r_norm
    if type == 'gravity':
        return -G * m / r_norm**2 * r_hat  # Gravitational force
    elif type == 'electrostatic':
        return k * q / r_norm**2 * r_hat  # Electrostatic force
    elif type == 'spring':
        return -K * r  # Spring force
    elif type == 'earth':
        return np.array([0, -m*g])  # Gravitational force near Earth's surface
    else:
        raise ValueError("Unknown interaction type")

if __name__ == "__main__":
    # Example usage
    pass