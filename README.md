OOICI Coverage Model
==============

Initial coverage model implementation

Reference Information: https://confluence.oceanobservatories.org/display/CIDev/R2+Construction+Data+Model+Implementation


#Prerequisites

This assumes basic development environment setup (git, directory structure). Please follow the
"New Developers Tutorial" for basic steps.


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

#Installation
**Ensure you are in a virtualenv prior to running the steps below**

From the *udunitspy* directory, run the following commands:

    pip install https://github.com/blazetopher/udunitspy/tarball/master#egg=udunitspy-0.1'

Once those steps complete, you should be able to import the udunits from the python shell:

    ipython # or python
    from udunitspy.udunits2 import Unit
    m = Unit('m')
    ft = Unit('ft')
    m2ft = m.get_converter(ft)
    m2ft.evaluate([10,15,20])