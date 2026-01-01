import numpy as np
import matplotlib as mtplt
import scipy


class func:
    function_ : any
    max_derivative : int
    functions : list
    variables : list
    constants : dict
    def __init__(self,function_,variables,max_derivative,constants=None):
        self.variables = variables
        self.constants = {}
        if constants:
            self.constants.update(constants)
        self.max_derivative = max_derivative
        self.functions = []
        var = self.variables[0]
        self.functions = [lambda *args: function_(*args,**self.constants)]+([None]*max_derivative)

    def call(self,funct):
        def wrapped(*args):
            return funct(*args, **self.constants)
        return wrapped

    def derivative(self,n,var_index = 0):
        if n == 0:
             return None
        h = 0.001
        order = self.functions[n-1]
        def wrapped(*args):
            args = list(args)
            args_h = args.copy()
            args_h[var_index] += h
            return (order(*args_h) - order(*args)) / h

        return wrapped
    
    def derivative_list(self,var_index=0):
        for i in range(1,self.max_derivative+1):
                self.functions[i] = self.derivative(i,var_index)
        return self.functions
    


        
if __name__ == "__main__":
    f = func(lambda x,y,k: k*(y*np.sin(x)), ["x"],constants= {"k":2}, max_derivative=3)
    f.derivative_list(0)
    x = 2
    y = 2
    print(f"f({x}) = {f.functions[0](x,y)}")
    print("first_derivative, x : ",f.functions[2](x,y))
    print(f.functions)
    f.derivative_list(1)
    print("first_derivative, y : ",f.functions[2](x,y))
    print(f.functions)
