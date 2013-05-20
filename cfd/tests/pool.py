import unittest
from cfd.pool import CFDPool, AlreadyRegisteredException


class PoolTestCase(unittest.TestCase):
    def test_basic_pool(self):
        pool = CFDPool()
        sample_class = object
        pool.register(sample_class)
        with self.assertRaises(AlreadyRegisteredException):
            pool.register(sample_class)