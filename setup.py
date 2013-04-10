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
    from setuptools import setup, Extension
    from setuptools.command.bdist_egg import bdist_egg
except:
    from distutils.core import setup, Extension


from distutils.command.build import build as build_

import os
# Custom build ordering ensuring that build_ext occurs BEFORE build_py - otherwise, the swig compiled udunits2_c.py is not included
class ext_build(build_):
    sub_commands = [('build_ext', build_.has_ext_modules)] + build_.sub_commands

class egg_install(bdist_egg):
    def run(self):
        self.run_command('build_ext')
        bdist_egg.run(self)

include_dirs = [
        '/usr/include',
        '/usr/local/include',
        ]
if 'C_INCLUDE_PATH' in os.environ:
    include_dirs = os.environ['C_INCLUDE_PATH'].split(':') + include_dirs

lib_dirs = [
        '/lib',
        '/usr/lib',
        '/usr/local/lib',
        ]
if 'LD_LIBRARY_PATH' in os.environ:
    lib_dirs = os.environ['LD_LIBRARY_PATH'].split(':') + lib_dirs


cmdclass = {'build': ext_build, 'bdist_egg':egg_install}

udunits_module = Extension('_udunits2_c',
    sources=['udunitspy/udunits2_c.i'],
    swig_opts=['-c++'] + ['-I%s' % i for i in include_dirs],
    include_dirs=include_dirs,
    library_dirs=lib_dirs,
    libraries=['udunits2','expat'])

xml_dir = 'etc/udunits'
xml_files = [os.path.join(xml_dir, f) for f in os.listdir(xml_dir)]

classifiers = ''' Intended Audience :: Science/Research
Intended Audience :: Developers
Intended Audience :: Education
Operating System :: OS Independent
Programming Language :: Python
Topic :: Scientific/Engineering
Topic :: Education
Topic :: Software Development :: Libraries :: Python Modules'''
setup(name='udunitspy',
    version='0.0.6',
    description='Python wrapper for UDUNITS2',
    long_description=open('DESC.txt').read(),
    license='LICENSE.txt',
    author='Christopher Mueller',
    author_email='cmueller@asascience.com',
    url='https://github.com/blazetopher/udunitspy/',
    cmdclass=cmdclass,
    ext_modules = [udunits_module],
    classifiers=classifiers.split('\n'),
    packages=['udunitspy', 'udunitspy.test'],
    data_files=[('etc/udunits', xml_files),],
    install_requires = [
        'numexpr==2.1',
        'pytest==2.3.2',
        'pytest-cov==1.6',
    ],
)


