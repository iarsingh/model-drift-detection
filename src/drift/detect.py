def _mean(values):
    return sum(values) / len(values)

def _std(values):
    center = _mean(values)
    variance = sum((value - center) ** 2 for value in values) / len(values)
    return variance ** 0.5 or 1e-9

def detect(reference, current):
    shift = abs(_mean(current) - _mean(reference)) / _std(reference)
    return {"mean_shift": round(shift, 4), "drift": shift >= 2, "retrained": False}
