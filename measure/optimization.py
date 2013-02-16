import logging


class _ScalarOptimizer(object):
    def __init__(self, default, epsilon):
        self.epsilon = epsilon
        self.value = default

    def set_point_reached(self, value):
        return abs(self.value - value) < self.epsilon


class Maximizer(_ScalarOptimizer):
    def __init__(self, epsilon=0.01):
        super(Maximizer, self).__init__(-100000.0, epsilon)

        self.logger = logging.getLogger(__name__)
        self.logger.propagate = True

    def is_better(self, value):
        return value > self.value


class Minimizer(_ScalarOptimizer):
    def __init__(self, epsilon=0.01):
        super(Minimizer, self).__init__(100000.0, epsilon)

        self.logger = logging.getLogger(__name__)
        self.logger.propagate = True

    def is_better(self, value):
        return value < self.value
