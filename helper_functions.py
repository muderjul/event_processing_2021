from event import Event


def lift(v: Event):
    return {"max": v.value, "arg": v.key}


def combine(a, b):
    return a if a["max"] >= b["max"] else b


def lower(c):
    return c["arg"]
