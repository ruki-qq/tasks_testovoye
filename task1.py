def strict(func):
    def wrapper(*args, **kwargs):
        varnames = func.__code__.co_varnames[:func.__code__.co_argcount]
        variables = zip(varnames, args)
        vartypes = func.__annotations__
        for varname, varvalue in variables:
            if type(varvalue) is not vartypes[varname]:
                raise TypeError(f"Wrong type for {varname}: expected {vartypes[varname]}, got {type(varvalue)}")
        return func(*args, **kwargs)

    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b

print(sum_two(4, 5))
