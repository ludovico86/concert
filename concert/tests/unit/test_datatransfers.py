import numpy as np
from concert.helpers import coroutine, broadcast, inject
from concert.coroutines import generate_sinograms
from concert.tests import TestCase


def producer(consumer):
    for i in range(5):
        consumer.send(i)


def generator():
    for i in range(5):
        yield i


class TestDataTransfers(TestCase):

    def setUp(self):
        super(TestDataTransfers, self).setUp()
        self.data = None
        self.data_2 = None

    @coroutine
    def consume(self):
        while True:
            self.data = yield

    @coroutine
    def consume_2(self):
        while True:
            self.data_2 = yield

    def test_broadcast(self):
        producer(broadcast(self.consume(), self.consume_2()))
        self.assertEqual(self.data, 4)
        self.assertEqual(self.data_2, 4)

    def test_sinogenerator(self):
        n = 4
        ground_truth = np.zeros((n, n, n))

        def image_producer(consumer):
            for i in range(n):
                ground_truth[i] = np.arange(n ** 2).reshape(n, n) * (i + 1)
                consumer.send(ground_truth[i])

        sinograms = np.zeros((n, n, n))
        image_producer(generate_sinograms(sinograms))

        np.testing.assert_almost_equal(sinograms,
                                       ground_truth.transpose(1, 0, 2))

    def test_injection(self):
        inject(generator(), self.consume())
        self.assertEqual(self.data, 4)
