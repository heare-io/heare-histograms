import unittest

from heare.histograms import Group
from utils import generate_test_histogram


class GroupTests(unittest.TestCase):
    def test_happy_path(self):
        h1, _ = generate_test_histogram(100, int)
        h2, _ = generate_test_histogram(10, int)
        h3, _ = generate_test_histogram(200, int)

        group = Group()
        group += 'h1', h1
        group += 'h2', h2
        group += 'h3', h3

        expl = group.explain_sample()
        self.assertEqual(3, len(expl['elements']))
        self.assertEqual(
            expl['total'],
            sum([el['total'] for el in expl['elements']])
        )

    def test_subgroups(self):
        h1, _ = generate_test_histogram(100, int)
        h2, _ = generate_test_histogram(10, int)
        h3, _ = generate_test_histogram(200, int)

        group = Group()
        group += 'h1', h1
        group += 'h2', h2
        group += 'h3', h3

        h4, _ = generate_test_histogram(100, int)
        h5, _ = generate_test_histogram(10, int)
        h6, _ = generate_test_histogram(200, int)
        subgroup = Group()
        subgroup += 'h4', h4
        subgroup += 'h5', h5
        subgroup += 'h6', h6
        group += 'subgroup', subgroup

        expl = group.explain_sample()
        self.assertEqual(4, len(expl['elements']))
        self.assertEqual(
            expl['total'],
            sum([el['total'] for el in expl['elements']])
        )
        # assert subgroup total matches
        self.assertEqual(
            expl['elements'][-1]['total'],
            sum([el['total'] for el in expl['elements'][-1]['elements']])
        )

    def test_group_operators(self):
        h1, _ = generate_test_histogram(100, int)
        h2, _ = generate_test_histogram(10, int)
        h3, _ = generate_test_histogram(200, int)

        group = Group()
        group += 'h1', h1
        group += 'h2', h2
        group += 'h3', h3

        h4, _ = generate_test_histogram(100, int)
        h5, _ = generate_test_histogram(10, int)
        h6, _ = generate_test_histogram(200, int)
        subgroup = Group(name='subgroup')
        subgroup += 'h4', h4
        subgroup += 'h5', h5
        subgroup += 'h6', h6

        group2 = group + subgroup
        expl = group2.explain_sample()
        self.assertEqual(4, len(expl['elements']))
        self.assertEqual(
            expl['total'],
            sum([el['total'] for el in expl['elements']])
        )
        # assert subgroup total matches
        self.assertEqual(
            expl['elements'][-1]['total'],
            sum([el['total'] for el in expl['elements'][-1]['elements']])
        )

