from .calc_math import func
import numpy as np
from . import plottings

class Lagrangian:
    def __init__(self, L_function, variables, constants=None, damper = 0):
        self.L = func(L_function, variables, max_derivative=2, constants=constants)
        self.variables = variables
        print(self.L)
        self.dL_dq       = self.L.derivative_list()[1]      
        self.dL_dqdot    = self.L.derivative_list(1)[1]      
        self.d2L_dqdot2  = self.L.derivative_list(1)[2]
        self.damper = damper
    
    def mixed_d2L_dq_dqdot(self, q, qdot):
        """
        Compute B = ∂²L/∂q ∂qdot via finite difference of dL_dqdot along q.
        This is: (dL_dqdot(q+h, qdot) - dL_dqdot(q, qdot)) / h
        """
        h = 0.001
        f = self.dL_dqdot
        # evaluate at q and q+h (preserving any constants via your func)
        v0 = f(q, qdot)
        v1 = f(q + h, qdot)
        return (v1 - v0) / h

    def qddot(self, q, qdot):
        """
        Return scalar q'' given q and qdot.
        """
        # C = ∂L/∂q
        C = self.dL_dq(q, qdot)

        # B = ∂²L/(∂q ∂qdot)
        B = self.mixed_d2L_dq_dqdot(q, qdot)

        # A = ∂²L/∂qdot² (effective mass term)
        A = self.d2L_dqdot2(q, qdot)

        # numeric safety
        eps = 1e-12
        if abs(A) < eps:
            raise ZeroDivisionError("Effective mass (∂²L/∂qdot²) nearly zero; problem ill-conditioned.")

        return ((C - B * qdot) / A) - self.damper*qdot


if __name__ == "__main__":
    L_obj = lambda x, xdot, m, g,k: 0.5*m*xdot**2-0.5*k*x**2
    lag = Lagrangian(L_obj, variables=("x","xdot"),constants={"m":1.0,"g":9.8,"k":0.5},damper=0)
    

# Plot angle over time
