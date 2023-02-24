def encode_var(n_e, n_j, j, x, y):
    return j * n_e**2 + x * n_e + y + 1

def decode_var(k, n_e):
    y = (k - 1) % n_e
    x = ((k - 1 - y) // n_e) % n_e
    j = (k - 1 - y - x * n_e) // (n_e * n_e)
    return j, x, y

def at_least_one(vars_list):
    clause = [str(v) for v in vars_list]
    clause.append('0')
    return ' '.join(clause)
