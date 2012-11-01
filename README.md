udunitspy
==============

Python wrapper library for udunits2

#Prerequisites
*These steps are tailored for a Mac OSX environment.  The library **should** function on linux as well, but modifications to the following setup may be required*

**Install the following if not yet present:**

**Install** git 1.7.7:
*Download the Mac or Linux installer and run it*

*OS Packages and package management:*
For Mac, use homebrew

    /usr/bin/ruby -e "$(curl -fsSL https://raw.github.com/gist/323731)"

  * python 2.7
  * udunits


**Install** python and udunits with Homebrew
    
    brew install python udunits
    
**Python packages and environment management:**

**Install** pip

    easy_install pip

**Install** virtualenv and virtualenvwrapper modules for your python 2.7 installation
*Note: This may require Mac's XCode (use XCode 3.3 free version*

    easy_install --upgrade virtualenv
    easy_install --upgrade virtualenvwrapper


Setup a virtualenv to run coverage-model (use any name you like):

    mkvirtualenv --python=python2.7 udunitspy

Ensure you're 'working in' the virtualenv you just made:

    workon udunitspy

#Numpy
The numpy library is finiky about installing as a dependency via setuptools, so ensure you have it installed in your virtualenv by running:

    pip install numpy

#ipython (optional)
ipython is an 'extended' python shell which provides useful functionality such as tab-complete, history, etc.  If you wish to use it, you can install it by running:

    pip install ipython

#Source installation (for development)
Clone the git repository:

    git clone https://github.com/blazetopher/udunitspy.git
    cd udunitspy

###iutil
The iutil shell script installs/uninstalls the udunitspy library for development purposes

Run the *iutil* shell script with no arguments to install the library:

    iutil

**Rerun the *inst* script (with no arguments) after changes are made to install the changes to your working environment**

###Uninstall
The library and dependencies can be uninstalled by calling the *iutil* script with the argument 'u':

    iutil u

Access/use the library as described in **Usage** below.

#Installation as a library
**Ensure your environment matches the prerequisites prior to running the steps below**

###As a local library
Run the following commands:

    pip install https://github.com/blazetopher/udunitspy/tarball/master#egg=udunitspy-0.1

###As a project dependency
The library can be included in your project by adding the following to your *setup.py*:

    dependency_links = [
        ...,
        'https://github.com/blazetopher/udunitspy/tarball/master#egg=udunitspy-0.1,
    ],
    install_requires = [
        ...,
        udunitspy==0.1,
    ],

# Usage
Once the library is installed, you should be able to access and use it from the ipython/python shell:

    In [1]: from udunitspy.udunits2 import Unit

    In [2]: m = Unit('m')

    In [3]: ft = Unit('ft')

    In [4]: m.are_convertible(ft)
    Out[4]: True

    In [5]: m2ft = m.get_converter(ft)

    In [6]: m2ft.evaluate([20, 22.3, 25.6])
    Out[6]: array([ 65.6168  ,  73.162732,  83.989504])