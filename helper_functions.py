def lift(v):
    return {"max": v["m"], "arg": v["a"]}


def combine(a, b):
    return a if a["max"] >= b["max"] else b


def lower(c):
    return c["arg"]
