from calc_math import func

class Lagrangian:
    def __init__(self, L_function, variables, constants=None):
        self.L = func(L_function, variables, max_derivative=2, constants=constants)
        self.variables = variables

        self.dL_dq       = self.L.derivative_list()[1]      
        self.dL_dqdot    = self.L.derivative_list(1)[1]      
        self.d2L_dqdot2  = self.L.derivative_list(1)[2]      

    def euler_lagrange(self, q, qdot):
        """
        Returns qddot from Euler-Lagrange equation:
        d/dt(∂L/∂qdot) - ∂L/∂q = 0
        => qddot = (∂L/∂q - ∂²L/∂qdot² * qdot) / ∂²L/∂qdot²
        """
        numerator   = self.dL_dq(q, qdot)
        denominator = self.d2L_dqdot2(q, qdot)

        return (numerator - denominator * qdot) / denominator
    
 
q, qdot = q0, qdot0
dt = 0.01
T = 1000
for t in range(T):
    qddot = euler_lagrange(q, qdot)
    q += qdot * dt
    qdot += qddot * dt