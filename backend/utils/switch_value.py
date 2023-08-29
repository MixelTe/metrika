def switch_value(inp, out):
    for v, r in out:
        if inp == v:
            return r
    return out[-1][1]
