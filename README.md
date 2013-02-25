udunitspy
==============

Python wrapper library for udunits2

#Prerequisites
*These steps are tailored for a Mac OSX environment.  The library **should** function on linux as well, but modifications to the following setup may be required*

###Required libraries
  * git
  * python
  * uduints

#Homebrew (OSX)

    /usr/bin/ruby -e "$(curl -fsSL https://raw.github.com/gist/323731)"

**Install** git, python, and udunits with Homebrew
    
    brew install git python udunits

##Optional Python Dependencies
These dependencies are optional, but tend to make life a little easier.

# Virtualenv
Virtualenv allows creation of isolated Python environments.  See more [here](http://www.virtualenv.org/en/1.9.X/#).

**Install** virtualenv and virtualenvwrapper modules for your python 2.7 installation
*Note: This may require OSX's XCode (can use XCode 3.3 free version)*

    easy_install --upgrade virtualenv
    easy_install --upgrade virtualenvwrapper

Setup a virtualenv to run coverage-model (use any name you like):

    mkvirtualenv --python=python2.7 udunitspy

Ensure you're 'working in' the virtualenv you just made:

    workon udunitspy

#Pip

You can just use *easy_install* if you prefer.

**Install** pip

    easy_install pip

#ipython
ipython is an 'extended' python shell which provides useful functionality such as tab-complete, history, etc.  If you wish to use it, you can install it by running:

    pip install ipython

##Required Python Dependencies
These dependencies are required for the library to function

#Numpy
The numpy library is finiky about installing as a dependency via setuptools, so ensure you have it installed in your virtualenv by running:

    pip install numpy

#Installation as a library
**Ensure your environment matches the prerequisites prior to running the steps below**

###As a local library
Run the following command:

    pip install udunitspy

###As a project dependency
The library can be included in your project by adding the following to your *setup.py*:

    install_requires = [
        ...,
        udunitspy,
    ],

# Usage
Once the library is installed, you should be able to access and use it from the ipython/python shell:

    In [1]: from udunitspy import Unit

    In [2]: m = Unit('m')

    In [3]: ft = Unit('ft')

    In [4]: m.are_convertible(ft)
    Out[4]: True

    In [5]: m2ft = m.get_converter(ft)

    In [6]: m2ft.evaluate([20, 22.3, 25.6])
    Out[6]: array([ 65.6168  ,  73.162732,  83.989504])

#Source installation (for development)
Clone the git repository:

    git clone https://github.com/blazetopher/udunitspy.git
    cd udunitspy

###Install
Install the uduintspy library for development:

    python setup.py develop

During development, there is no need to reinstall.  Changes to the source are automatically reflected in your working environment.

#Uninstall
***NOTE:** Please ensure these libraries aren't needed by other software before uninstalling!!*  

The library and dependencies can be uninstalled by calling:

    pip uninstall -y numexpr pytest py pytest-cov udunitspy
