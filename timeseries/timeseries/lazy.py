# from TimeSeries import TimeSeries

class LazyOperation:
    """
    A lazy evaluation class. The LazyOperation object takes in a function and remembers it without doing computation
    use eval() to actually compute the operation.

    Methods
    -------
    eval():
        Evaluate a function(operation)

    """

    def __init__(self, function, *args, **kwargs):
        self._function = function
        self._args = args
        self._kwargs = kwargs
        
    def eval(self):
        # Recursively eval() lazy args
        new_args = [a.eval() if isinstance(a,LazyOperation) else a for a in self._args]
        new_kwargs = {k:v.eval() if isinstance(v,LazyOperation) else v for k,v in self._kwargs}
     
        return self._function(*new_args, **new_kwargs)

"""
A lazy evaluation decorator
"""
def lazy(function):
    def create_thunk(*args, **kwargs):
        return LazyOperation(function, *args, **kwargs)
    return create_thunk

# @lazy
# def lazy_add(a, b):
#     return a+b

# @lazy
# def lazy_mul(a, b):
#     return a*b



if __name__ == "__main__":
	t1 = TimeSeries(range(0,4), range(1,5))
	t2 = TimeSeries(range(1,5), range(2,6))
	t = check_length(t1,t2)
	print(t.eval())
