import tempfile
import os
import logging

from unittest import TestCase, mock

from parse import Parser
from logger import getLogger


from tables import meta, header, k1, k2, base, header, trailer, j1, j2, k3, k4, l1, n1

class TestLogger(TestCase):
    def test_get_logger(self):
        logger = getLogger('test')

        self.assertTrue(isinstance(logger.handlers[0], logging.StreamHandler))
        self.assertEqual(logger.handlers[0].formatter.datefmt, '%Y-%m-%d %H:%M:%S')
        self.assertEqual(logging.getLevelName(logger.getEffectiveLevel()), logging.getLevelName(logging.DEBUG))


    def test_logging(self):
        logger = getLogger('test')
        with self.assertLogs(logger) as log:
            logger.info(111)
            self.assertListEqual(log.output, ['INFO:test:111'])
