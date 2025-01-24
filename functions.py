def can_call(obj, method):
    return hasattr(obj, method) and callable(getattr(obj, method))
