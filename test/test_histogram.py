import unittest
import random

from heare.histograms import Histogram, Max, Min, MaxAtPercentile, MinAtPercentile, Shift, Scale


class HistogramTests(unittest.TestCase):
    def test_happy_path(self):
        h = Histogram[int](max_size=100)
        self.assertEqual(0, len(h._data))
        for i in range(50):
            h.observe(random.randint(0, 100))
        self.assertEqual(50, len(h._data))
        for i in range(100):
            h.observe(random.randint(0, 100))
        self.assertEqual(100, len(h._data))
        data = list(sorted(h._data))
        self.assertEqual(data[0], h.percentile(0.0))
        self.assertEqual(data[-1], h.percentile(1.0))
        self.assertEqual(data[50], h.percentile(0.5))

        h = h + h.clone()
        self.assertEqual(100, len(h._data))
        data = list(sorted(h._data))
        self.assertEqual(data[0], h.percentile(0.0))
        self.assertEqual(data[-1], h.percentile(1.0))
        self.assertEqual(data[50], h.percentile(0.5))

    def test_adjustments(self):
        h = Histogram[float](max_size=100)
        for i in range(100):
            h.observe(random.random())
        data = list(sorted(h._data))

        v = h.percentile(0.0)
        adjusted = Max(h, v)
        self.assertEqual(data[0], adjusted.sample())
        adjusted = MaxAtPercentile(h, 0.0)
        self.assertEqual(data[0], adjusted.sample())

        v = h.percentile(1.0)
        adjusted = Min(h, v)
        self.assertEqual(data[-1], adjusted.sample())
        adjusted = MinAtPercentile(h, 1.0)
        self.assertEqual(data[-1], adjusted.sample())

        v = h.percentile(0.5)
        adjusted = Shift(h, 10)
        self.assertEqual(v + 10, adjusted.percentile(0.5))

        adjusted = Scale(h, 10)
        self.assertEqual(v * 10, adjusted.percentile(0.5))

    def test_composed_adjustments(self):
        h = Histogram[float](max_size=100)
        for i in range(100):
            h.observe(random.random())
        data = list(sorted(h._data))

        v = h.percentile(0.5)
        adjusted = Max(h, v)
        adjusted = Min(adjusted, v)
        self.assertEqual(data[50], adjusted.sample())
        self.assertEqual(data[50], adjusted.percentile(0.4))
        self.assertEqual(data[50], adjusted.percentile(0.6))

