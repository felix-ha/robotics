import time
from optimization.optimizer import Optimizer
from optimization.optimization_result import OptimizationResult
import numpy as np


class GradientDescent(Optimizer):
    def __init__(self, max_iterations=1000, constant_step_length=0.001, epsilon_gradient=0.001):
        Optimizer.__init__(self)
        self.max_iterations = max_iterations
        self.constant_step_length = constant_step_length
        self.epsilon_gradient = epsilon_gradient


    def optimize(self, f, x_0):
        x = np.array([x_0])
        exit_flag = 0
        start = time.time()

        gradient = self.derive(f, x_0)
        norm_gradient = np.linalg.norm(gradient)
        x_current = x_next = x_0

        iterations = 0
        while distance_to_destination >= self.epsilon_gradient:
            direction = - gradient / norm_gradient
            x_next = x_current + self.constant_step_length * direction

            gradient = self.derive(f, x_next)
            x_current = x_next

            x_tcp, y_tcp = self.robot.forward_kinematic(x_current)
            coordinates_tcp = np.array([x_tcp, y_tcp])
            distance_to_destination = np.linalg.norm(coordinates_tcp - self.coordinates_destination)

            x = np.concatenate((x, np.array([x_current])), axis=0)
            iterations += 1

            if iterations >= self.max_iterations:
                exit_flag = 1
                break

        end = time.time()
        elapsed_time_ms = (end - start) * 1000
        x_star = x_next
        f_x_star = f(x_star)

        return OptimizationResult(x_star=x_star,
                                  f_x_star=f_x_star,
                                  norm_gradient=np.linalg.norm(gradient),
                                  x=x,
                                  elapsed_time_ms=elapsed_time_ms,
                                  exit_flag=exit_flag,
                                  iterations=iterations)
