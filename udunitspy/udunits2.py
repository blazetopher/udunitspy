"""
Adapted from python-udunits: https://code.google.com/p/python-udunits/

Copyright (C) 2011  Constantine Khroulev

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

===

Author: Christopher Mueller
Copyright (C) UC Regents 2012
"""

from copy import deepcopy
import udunitspy.udunits2_c as ut
from udunitspy.udunits2_c import UT_ASCII
import os
import numexpr as ne
import sys
import logging
try:
    # Python 2.7
    from logging import NullHandler
except ImportError:
    # Python < 2.7
    import logging
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass
log = logging.getLogger()
log.addHandler(NullHandler())

# Udunits2 Errors - from udunits2.h
ERROR_LOOKUP = {
    0: 'UT_SUCCESS:  Success',
    1: 'UT_BAD_ARG:  An argument violates the function\'s contract',
    2: 'UT_EXISTS:  Unit, prefix, or identifier already exists',
    3: 'UT_NO_UNIT:  No such unit exists',
    4: 'UT_OS:  Operating-system error.  See \'errno\'',
    5: 'UT_NOT_SAME_SYSTEM:  The units belong to different unit-systems',
    6: 'UT_MEANINGLESS:  The operation on the unit(s) is meaningless',
    7: 'UT_NO_SECOND:  The unit-system doesn\'t have a unit named \'second\'',
    8: 'UT_VISIT_ERROR:  An error occurred while visiting a unit',
    9: 'UT_CANT_FORMAT:  A unit can\'t be formatted in the desired manner',
    10: 'UT_SYNTAX:  String unit representation contains syntax error',
    11: 'UT_UNKNOWN:  String unit representation contains unknown word',
    12: 'UT_OPEN_ARG:  Can\'t open argument-specified unit database',
    13: 'UT_OPEN_ENV:  Can\'t open environment-specified unit database',
    14: 'UT_OPEN_DEFAULT:  Can\'t open installed, default, unit database',
    15: 'UT_PARSE:  Error parsing unit specification',
}

def _make_error_message(from_name, error_num, message=None):
    return '{0} resulted in udunits error {1}{2}'.format(from_name, ERROR_LOOKUP[error_num], ': '+message if message else '')

class UdunitsError(Exception):
    def __init__(self, from_name, error_num, message=None):
        Exception.__init__(self, _make_error_message(from_name, error_num, message))

class System:
    """Unit system (ut_system).
    """
    
    def __init__(self, path=None, empty=False):
        """Creates a unit system
        """
        if empty:
            self.this = ut.new_system()
        elif path:
            self.this = ut.read_xml(path)
        else:
            self.this = ut.read_xml(None)

        if not self.this:
            raise UdunitsError(System.__init__.__name__, ut.get_status())

    def get_unit_by_name(self, name):
        ret = Unit(system=self.this)
        ret.this = ut.get_unit_by_name(self.this, name)
        if not ret.this:
            raise UdunitsError(System.get_unit_by_name.__name__, ut.get_status(), 'No unit with name \'{0}\' in system'.format(name))

        return ret

    def get_unit_by_symbol(self, symbol):
        ret = Unit(system=self.this)
        ret.this = ut.get_unit_by_symbol(self.this, symbol)
        if not ret.this:
            raise UdunitsError(System.get_unit_by_symbol.__name__, ut.get_status(), 'No unit with symbol \'{0}\' in system'.format(symbol))

        return ret

    def add_name_prefix(self, name, value):
        res = ut.add_name_prefix(self.this, name, value)
        if res: # anything other than 0
            raise UdunitsError(System.add_name_prefix.__name__, ut.get_status())

    def add_symbol_prefix(self, symbol, value):
        res = ut.add_symbol_prefix(self.this, symbol, value)
        if res: # anything other than 0
            raise UdunitsError(System.add_symbol_prefix.__name__, ut.get_status())

    def new_base_unit(self):
        res = ut.new_base_unit(self.this)
        if not res:
            raise UdunitsError(System.new_base_unit.__name__, ut.get_status())

        return res

    def new_dimensionless_unit(self):
        ret = Unit(system=self.this)
        ret.this = ut.new_dimensionless_unit(self.this)
        if not ret.this:
            raise UdunitsError(System.new_dimensionless_unit.__name__, ut.get_status())

        return ret

    def get_dimensionless_unit_one(self):
        ret = Unit(system=self.this)
        ret.this = ut.get_dimensionless_unit_one(self.this)
        if not ret.this:
            raise UdunitsError(System.get_dimensionless_unit_one.__name__, ut.get_status())

        return ret

# Check various locations for a default UDUNITS2 library
# Pip installed location
DEFAULT_UDUNITS_PATH = os.path.realpath(os.path.join(sys.prefix, 'etc','udunits','udunits2.xml'))
if not os.path.exists(DEFAULT_UDUNITS_PATH):
    # Development
    DEFAULT_UDUNITS_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), '..','etc','udunits','udunits2.xml'))
if not os.path.exists(DEFAULT_UDUNITS_PATH):
    # Installed by udunits library
    DEFAULT_UDUNITS_PATH = '/usr/local/share/udunits/udunits2.xml'

log.info('Using udunits2.xml database: %s', DEFAULT_UDUNITS_PATH)
DEFAULT_SYSTEM = System(path=DEFAULT_UDUNITS_PATH)

class Unit:
    """Unit class (ut_unit).
    """

    def __init__(self, spec = "", system=None, encoding=None):
        """Initialize a unit. Calls ut_parse().
        """
        if not system and isinstance(system, (str, unicode)):
            system = System(path=system)
        self.system = system or DEFAULT_SYSTEM
        self.this = ut.parse(self.system.this, spec, encoding or UT_ASCII)

        if not self.this:
            raise UdunitsError(Unit.__init__.__name__, ut.get_status())

    def copy(self):
        result = Unit(system=self.system)
        result.this = ut.clone(self.this)

        return result

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<units of '%s'>" % self.__str__()

    def format(self, encoding = UT_ASCII):
        """Return a string representation. Calls ut_format().
        """
        _, result = ut.format(self.this, 2048, encoding)

        return result

    def multiply_or_divide(self, x, multiply = True):
        if multiply:
            function = ut.multiply
        else:
            function = ut.divide
        
        result = Unit(system=self.system)

        if isinstance(x, (int, long, float)):
            if not multiply:
                x = 1.0/x
            result.this = ut.scale(x, self.this)
        elif isinstance(x, Unit):
            result.this = function(self.this, x.this)

        return result

    def __mul__(self, x):
        return self.multiply_or_divide(x, True)

    def __rmul__(self, x):
        return self.__mul__(x)

    def __div__(self, x):
        return self.multiply_or_divide(x, False)

    def __pow__(self, x):
        result = Unit(system=self.system)
        result.this = ut.pow(self.this, int(x))
        return result

    def __sub__(self, x):
        result = Unit(system=self.system)
        result.this = ut.offset(self.this, x)
        return result

    def __neg__(self):
        result = Unit(system=self.system)
        result.this = self.multiply_or_divide(-1)
        return result

    def __add__(self, x):
        return self.__sub__(-x)

    def __cmp__(self, other):
        return ut.compare(self.this, other.this)

    def set_second(self,):
        ut.set_second(self.this)

    def map_to_name(self, name):
        raise NotImplementedError('Not implemented at this time')

    def unmap_to_name(self, name):
        raise NotImplementedError('Not implemented at this time')

    def map_name_to(self, name):
        raise NotImplementedError('Not implemented at this time')

    def unmap_name_to(self, name):
        raise NotImplementedError('Not implemented at this time')

    @property
    def name(self):
        tmp = ut.get_name(self.this, UT_ASCII)
        if tmp:
            return tmp

        return self.format()

    @property
    def symbol(self):
        return ut.get_symbol(self.this, UT_ASCII)

    def is_dimensionless(self):
        return bool(ut.is_dimensionless(self.this))

    def same_system(self, unit):
        return bool(ut.same_system(self.this, unit.this))

    def are_convertible(self, unit):
        if hasattr(unit, '__iter__'):
            return [self.are_convertible(x) for x in unit]

        if isinstance(unit, (str, unicode)):
            unit = Unit(spec=unit, system=self.system)
        elif isinstance(unit, Unit):
            unit = unit
        else:
            raise TypeError('\'unit\' must be a str or Unit. Got: {0}'.format(unit))

        return bool(ut.are_convertible(self.this, unit.this))

    def get_converter(self, unit):
        if isinstance(unit, (str, unicode)):
            unit = Unit(spec=unit, system=self.system)
        elif isinstance(unit, Unit):
            unit = unit
        else:
            raise TypeError('\'unit\' must be a str or Unit. Got: {0}'.format(unit))

        if self.are_convertible(unit):
            return Converter(self.this, unit.this)

    def invert(self):
        result = Unit(system=self.system)
        result.this = ut.invert(self.this)
        return result

    def root(self, n):
        result = Unit(system=self.system)
        result.this = ut.root(self.this, int(n))
        return result

    def log(self, base):
        result = Unit(system=self.system)
        result.this = ut.log(float(base), self.this)
        return result

class Converter:
    """Unit converter class (cv_converter).
    """
        
    def __init__(self, unit_1=None, unit_2=None, trivial=False, inverse=False,
                 scale=None, offset=None, base=None, power=None):
        """Initialize a converter.
        """
        if trivial:
            self.this = ut.cv_get_trivial()
        elif inverse:
            self.this = ut.cv_get_inverse()
        elif scale is not None and offset is not None:
            self.this = ut.cv_get_galilean(scale, offset)
        elif scale is not None:
            self.this = ut.cv_get_scale(scale)
        elif offset is not None:
            self.this = ut.cv_get_offset(offset)
        elif base is not None:
            self.this = ut.cv_get_log(base)
        elif power is not None:
            self.this = ut.cv_get_pow(power)
        else:
            if unit_1 is None or unit_2 is None:
                raise TypeError('\'unit_1\' and \'unit_2\' cannot be None')

            if isinstance(unit_1, str):
                unit_1 = Unit(unit_1)
            if isinstance(unit_2, str):
                unit_2 = Unit(unit_2)
            self.this = ut.get_converter(unit_1.this, unit_2.this)

        if self.this is None:
            raise UdunitsError(Converter.__init__.__name__, ut.get_status())

    def __call__(self, x):
        if isinstance(x, Converter):
            self.combine(x)
        elif isinstance(x, (int, long, float)):
            return ut.cv_convert_double(self.this, float(x))
        elif hasattr(x, '__iter__'):
            return self._evaluate(x)

    def combine(self, other):
        if not isinstance(other, Converter):
            raise TypeError('\'other\' must be of type Converter')

        result = Converter(trivial=True)
        result.this = ut.cv_combine(other.this, self.this)
        if not result.this:
            raise UdunitsError(Converter.__call__.__name__, ut.get_status(), 'ut_cv_combine failure')

        return result

    def get_expression(self, variable=None):
        if variable is None:
            variable = 'x'
        elif not isinstance(variable, str):
            raise TypeError('If specified, \'variable\' must be of type str')
        _, result = ut.cv_get_expression(self.this, 2048, variable)
        return result

    def evaluate(self, value):
        return self(value)

    def _evaluate(self, value):
        x = deepcopy(value)
        expr = self.get_expression('x')
        ret = ne.evaluate(expr)

        ret = ret.squeeze()
        if ret.size == 1:
            if ret.ndim == 0:
                ret = ret[()]
            else:
                ret = ret[0]

        return ret

    def __repr__(self):
        return "<unit converter: %s>" % self.__str__()

    def __str__(self):
        return "y = %s" % self.get_expression("x")