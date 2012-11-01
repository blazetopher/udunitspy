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
try:
    from setuptools import setup, Extension, find_packages
    from setuptools.command.build_ext import build_ext
except:
    from distutils.core import setup, Extension
    from distutils.command.build_ext import build_ext


from distutils.command.build import build

import os

# Custom build ordering ensuring that build_ext occurs BEFORE build_py - otherwise, the swig compiled udunits2_c.py is not included
class ext_build(build):
    sub_commands = [('build_ext', build.has_ext_modules)] + build.sub_commands

cmdclass = {'build': ext_build}

udunits_module = Extension('_udunits2_c',
    sources=['src/udunitspy/udunits2_c.i'],
    swig_opts=['-c++', '-I/usr/local/include/'],
    include_dirs=['/usr/local/include/'],
    library_dirs=['/usr/local/lib/'],
    libraries=['udunits2'])

xml_dir = 'etc/udunits'
xml_files = [os.path.join(xml_dir, f) for f in os.listdir(xml_dir)]

dist = setup(name='udunitspy',
    version='0.1',
    description='Python wrapper for UDUNITS2',
    author='OOI CI',
    author_email='cmueller@asascience.com',
    url='',
    cmdclass=cmdclass,
    ext_modules = [udunits_module],
    package_dir={'':'src'},
    packages=['udunitspy'],
    data_files=[('etc/udunits', xml_files),],
    install_requires = [
        'numexpr==2.0.1',
    ],
)