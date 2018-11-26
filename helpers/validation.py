def prepare_validation(func):
    def wrapper(obj, key, value):
        try:
            obj.errors
        except AttributeError:
            obj.errors = []
        return func(obj, key, value)

    return wrapper
