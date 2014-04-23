# -*- coding: utf-8 -*-
import unittest

from il2_commons.targets import TargetTypes, TargetPriorities


class TargetsTestCase(unittest.TestCase):

    def test_target_types(self):
        data = [(x.name, x.value) for x in TargetTypes.constants()]
        self.assertEqual(data, [('destroy', 0),
                                ('destroy_bridge', 1),
                                ('destroy_area', 2),
                                ('recon', 3),
                                ('escort', 4),
                                ('cover', 5),
                                ('cover_area', 6),
                                ('cover_bridge', 7), ])

    def test_target_priorities(self):
        data = [(x.name, x.value) for x in TargetPriorities.constants()]
        self.assertEqual(data, [('primary', 0),
                                ('secondary', 1),
                                ('hidden', 2), ])