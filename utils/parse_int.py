def parse_int(v: str):
    try:
        return int(v), True
    except Exception:
        return 0, False
