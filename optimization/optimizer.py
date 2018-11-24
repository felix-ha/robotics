import numpy as np
import pickle


class Optimizer():

    def __init__(self):
        with open('constants.pickle', 'rb') as f:
            save = pickle.load(f)
            self.epsilon_mach = save['epsilon_mach']
            self.step_length_derivatives = save['step_length_derivatives']

    def derive(self, f, x):
        h = self.step_length_derivatives
        dimension_domain = len(x)
        result = np.empty(dimension_domain)

        for i in range(dimension_domain):
            e = self.get_unit_vector(dimension_domain,i)
            result[i] = (f(x + h * e) - f(x - h * e)) / (2 * h)

        return result


    def get_unit_vector(self, dimension, index):
        unit_vector = np.zeros([dimension])
        unit_vector[index] = 1
        return unit_vector


if __name__ == '__main__':
    opt = Optimizer()
    d = opt.derive(lambda x: x ** 2, np.array([5]))
    print(d)


