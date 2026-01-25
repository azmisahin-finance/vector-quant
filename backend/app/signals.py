import numpy as np

def generate_signal(v):
    ret, vol, mom = v
    mag = np.linalg.norm(v)

    if ret > 0 and vol > 1 and mom > 0 and mag > 1.2:
        return "AL"
    if ret < 0 and mom < 0:
        return "SAT"
    return "BEKLE"
