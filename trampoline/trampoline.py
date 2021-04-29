def simple_factorial(n):
    if n == 0:
        return 1
    return simple_factorial(n-1) * n


def trampoline(fn):
    def _(*args, **kwargs):
        result = fn(*args, **kwargs)
        while callable(result):
            result = result()
        return result
    return _


def iterable_factorial(n):
    def _(f, n):
        if n == 0:
            return f
        return lambda: _(f*n, n - 1)
    return _(1, n)


try:
    simple_factorial(5000)
except Exception as e:
    print(e)

print(
    trampoline(iterable_factorial)(5000)
)
