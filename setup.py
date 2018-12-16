#!/usr/bin/env python
# -------------------------------------------------------------------------- #
# Copyright (c) 2015, Borja Sotomayor
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# - Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
#
# - Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# - Neither the name of The University of Chicago nor the names of its
#   contributors may be used to endorse or promote products derived from this
#   software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# -------------------------------------------------------------------------- #

from setuptools import setup, find_packages
import sys

sys.path.insert(0, './src')
from twitterharvester import RELEASE


eps = ['twitter-harvester = twitterharvester:cmd.main']

setup(name='twitter-harvester',
      version=RELEASE,
      description='A simple command-line tool for harvesting tweets',
      author='Borja Sotomayor',
      author_email='borja@cs.uchicago.edu',
      url='http://people.cs.uchicago.edu/~borja/',
      package_dir = {'': 'src'},
      packages=find_packages("src"),
      python_requires='>=3.5',

      install_requires = [ "twitter >= 1.18.0", "click >= 6.7" ],

      setup_requires = [ "setuptools_git >= 1.0" ],

      entry_points = {
        'console_scripts': eps
        },

      zip_safe = False,

      license="BSD",
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'Intended Audience :: Education',
          'License :: OSI Approved :: BSD License',
          'Operating System :: POSIX',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3 :: Only',
          ]
     )
