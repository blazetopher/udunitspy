#!/usr/bin/env python

"""
@package udunitspy.test.test_udunits2
@file udunitspy/test/test_udunits2.py
@author Christopher Mueller
@brief 
"""

from udunitspy.udunits2 import Unit, System, DEFAULT_SYSTEM, DEFAULT_UDUNITS_PATH, UdunitsError, Converter
import numpy as np
import pytest

class TestUdunits2Unit:

    def test_create(self):
        m = Unit('m')
        assert isinstance(m, Unit)

        assert str(m) == 'meter'

    def test_copy(self):
        pa = Unit('pa')
        pac = pa.copy()
        assert pa == pac

    def test_are_convertible(self):
        m = Unit('m')
        ft = Unit('ft')
        s = Unit('s')

        # True from a unit
        assert m.are_convertible(ft) == True
        # True from a str
        assert m.are_convertible('ft') == True
        # False from a unit
        assert m.are_convertible(s) == False
        # False from a str
        assert m.are_convertible('s') == False
        # A sequence
        assert m.are_convertible([ft,'s']) == [True, False]

        with pytest.raises(TypeError):
            m.are_convertible(None)

    def test_equivalence(self):
        m = Unit('m')
        m_ = Unit('m')

        assert m == m_

        assert Unit('km2/s') == Unit('km2.s-1') == Unit('km2 s-1')

    def test_pow(self):
        m = Unit('m')
        m2 = Unit('m2')
        assert m2 == pow(m,2)

    def test_invert(self):
        m = Unit('m')
        s = Unit('s')

        assert Unit('m/s') == m * s.invert() == m / s

    def test_root(self):
        m = Unit('m')
        m2 = pow(m, 2)
        assert m2.root(1) == m2
        assert m2.root(2) == m

    def test_log(self):

        # Using milliwatt example from:
        # http://www.unidata.ucar.edu/software/udunits/udunits-2/udunits2lib.html#index-ut_005flog-65
        mW=Unit('milliWatt')

        bel_1_mW = mW.log(10)
        assert str(bel_1_mW) == 'lg(re 0.001 W)'

        decibel_1_mW = bel_1_mW * 0.1
        assert str(decibel_1_mW) == '0.1 lg(re 0.001 W)'

    def test_combination(self):
        m = Unit('m')
        m_ = Unit('m')
        m2=m*m_
        assert m2 == Unit('m2')
        assert m2 == pow(m,2)

        s = Unit('s')
        ms=m/s
        assert ms == Unit('m/s')

    def test_offset(self):
        k = Unit('K')

        # Celsius should be Kelvin - 273.15
        c = k - 273.15
        assert c == Unit('deg_c')

        # Adding 273.15 should bring us back to kelvin
        k_ = c + 273.15
        assert k == k_

        # Use offsets to go from m to km and cm
        m = Unit('m')
        assert m*1000 == Unit('km')
        assert m/100 == Unit('cm')
        assert str(-m) == '-1 m'

    def test_same_system(self):
        assert Unit('m').same_system(Unit('ft'))

    def test_errors(self):
        with pytest.raises(UdunitsError) as ex:
            Unit('no-exist-unit')
            assert ex.message.contains('UT_UNKNOWN')

        m = Unit('m')
        with pytest.raises(NotImplementedError):
            m.map_to_name('blah')

        with pytest.raises(NotImplementedError):
            m.unmap_to_name('blah')

        with pytest.raises(NotImplementedError):
            m.map_name_to('blah')

        with pytest.raises(NotImplementedError):
            m.unmap_name_to('blah')

class TestUdunits2Converter:

    def test_create(self):
        day = Unit('day')
        yr = Unit('yr')
        day2yr = Converter(day,yr)

        assert day2yr.get_expression() == '0.00273791*x'

    def test_convert_single(self):
        k = Unit('K')
        c = Unit('deg_c')

        k2c = k.get_converter(c)

        np.testing.assert_almost_equal(k2c(23.5), -249.65, decimal=2)
        np.testing.assert_almost_equal(k2c(288.2), 15.05, decimal=2)
        np.testing.assert_almost_equal(k2c(273.15), 0.0, decimal=1)

    def test_convert_sequence(self):
        m = Unit('m')
        ft = Unit('ft')

        m2ft = m.get_converter(ft)
        assert '3.28084*x' == m2ft.get_expression()

        ft2m = Converter('ft',m)
        assert '0.3048*a' == ft2m.get_expression('a')

        sqm2sqft = (m*m).get_converter((ft*ft))
        assert '10.7639*x' == sqm2sqft.get_expression()

        inarr = np.array([2.8, 3.5, 19.2, 312])

        # Verify output of m2ft is what we expect
        outarr = m2ft(inarr)
        np.testing.assert_array_almost_equal(outarr, np.array([9.186352, 11.48294, 62.992128, 1023.62208]), decimal=6)

        # Verify output of ft2m is what we expect
        outarr = ft2m(inarr)
        np.testing.assert_array_almost_equal(outarr, np.array([0.85344, 1.0668 , 5.85216, 95.0976]), decimal=5)

        outarr = sqm2sqft(inarr)
        np.testing.assert_array_almost_equal(outarr, np.array([30.13892, 37.67365, 206.66688, 3358.3368]), decimal=5)

        with pytest.raises(TypeError):
            m.get_converter(None)

    def test_convert_ndarray(self):
        lb2g = Converter('lb','g')

        inarr = np.arange(10).reshape(2, 5)
        valarr = np.array([[ 0.0, 453.592, 907.184, 1360.776, 1814.368],
                      [2267.96, 2721.552, 3175.144, 3628.736, 4082.328]])

        outarr = lb2g(inarr)
        assert outarr.shape == (2, 5)
        np.testing.assert_array_almost_equal(outarr, valarr, decimal=3)

        # Add an 'empty' outer dimension - this will get squeezed out!!
        inarr2 = inarr.copy().reshape(1,2,5)
        outarr2 = lb2g(inarr2)
        assert outarr2.shape == (2, 5)
        np.testing.assert_array_almost_equal(outarr2, valarr, decimal=3)

        # Slice the array down to 1 value, it will come out as a single value
        np.testing.assert_almost_equal(lb2g(inarr2[:,1,2]), 3175.144, decimal=3)


    def test_combine_converters(self):
        s = Unit('s')
        min = Unit('min')
        hr = Unit('hr')

        s2min = s.get_converter(min)
        min2hr = min.get_converter(hr)

        s2hr = s.get_converter(hr)

        s2min2hr = s2min.combine(min2hr)

        assert s2hr.get_expression('x') == s2min2hr.get_expression('x')

        np.testing.assert_almost_equal(min2hr(s2min.evaluate(10)), s2min2hr(10), decimal=7)

        with pytest.raises(TypeError):
            s2min.combine('10')

    def test_errors(self):
        s = Unit('s')
        min = Unit('min')

        s2min = s.get_converter(min)

        with pytest.raises(TypeError):
            s2min.combine('10')

        with pytest.raises(TypeError):
            Converter(s, None)

        with pytest.raises(TypeError):
            fake = object
            fake.this = None
            Converter(s, fake)

class TestUdunits2System:

    def test_system(self):
        s = DEFAULT_SYSTEM
        assert s.get_unit_by_name('meter') == Unit('m')
        assert s.get_unit_by_symbol('ft') == Unit('ft')
        assert s.get_dimensionless_unit_one() == Unit('1')

