from supermutes.readonly import readonly


def return_readonly(func):
    "Decorator for making the output of a function/method readonly"
    def wrapped(*args, **kwargs):
        response = func(*args, **kwargs)
        return readonly(response)
    return wrapped
