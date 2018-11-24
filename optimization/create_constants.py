import pickle
import numpy as np


def get_eps_mach():
    eps = 1.0
    exp = 0
    sum = 1.0 + eps

    while sum != 1:
        eps = eps / 2
        exp = exp - 1
        sum = 1.0 + eps

    return eps

if __name__ == '__main__':

    epsilon_mach = get_eps_mach()
    step_length_derivatives = np.sqrt(epsilon_mach)

    with open('constants.pickle', 'wb') as f:
        save = {
            'epsilon_mach': epsilon_mach,
            'step_length_derivatives': step_length_derivatives
        }
        pickle.dump(save, f, pickle.HIGHEST_PROTOCOL)

