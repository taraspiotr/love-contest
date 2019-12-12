import math

K = 32

def update_ratings(r1, r2, first_won=True):
    r1_, r2_ = math.pow(10, r1 / 400), math.pow(10, r2 / 400)
    e1, e2 = r1_ / (r1_ + r2_), r2_ / (r1_ + r2_)
    s1, s2 = (1, 0) if first_won else (0, 1)
    return r1 + int(K * (s1 - e1)), r2 + int(K * (s2 - e2))

