class OptimizationResult:
    def __init__(self, x_star, f_x_star, norm_gradient, x, elapsed_time_ms, exit_flag, iterations):
        self.x_star = x_star
        self.f_x_star = f_x_star
        self.norm_gradient = norm_gradient
        self.x = x
        self.elapsed_time_ms = elapsed_time_ms
        self.exit_flag = exit_flag
        self.iterations = iterations

        if self.exit_flag == 1:
            self.message = 'Maximum of iterations reached, optimization stopped early'
        else:
            self.message = 'Optimization successfully'

    def print(self):
        print('Summary: ', self.message)
        print('x_star = ', self.x_star)
        print('f(x_star) = {:.10f} '.format(self.f_x_star))
        print('Norm grad(x_star) = {:.10f} '.format(self.norm_gradient))
        print('Elapsed ms: {:.2f}'.format(self.elapsed_time_ms))
        print('Iterations: ', self.iterations)
        print('Exit flag: ', self.exit_flag)
