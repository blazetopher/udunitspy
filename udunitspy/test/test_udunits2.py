#!/usr/bin/env python

"""
@package udunitspy.test.test_udunits2
@file udunitspy/test/test_udunits2.py
@author Christopher Mueller
@brief 
"""

from udunitspy.udunits2 import Unit

class TestUdunits2Unit:

    def setUp(self):
        pass

    def test_create_unit(self):
        m = Unit('m')
        assert isinstance(m, Unit)

    def test_are_compatible(self):
        m = Unit('m')
        ft = Unit('ft')
        s = Unit('s')

        assert m.are_convertible(ft) == True
        assert m.are_convertible(s) == False

    def test_unit_equivalence(self):
        m = Unit('m')
        m_ = Unit('m')

        assert m == m_

    def test_unit_combination(self):
        m = Unit('m')
        m_ = Unit('m')
        m2=m*m_
        assert m2 == Unit('m2')

    def test_offset(self):
        k = Unit('K')

        # Celsius should be Kelvin - 273.15
        c = k - 273.15
        assert c == Unit('deg_c')

        # Adding 273.15 should bring us back to kelvin
        k_ = c + 273.15
        assert k == k_

    def test_converter(self):
        pass