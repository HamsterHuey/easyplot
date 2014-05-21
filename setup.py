from distutils.core import setup
# from setuptools import setup, find_packages
import codecs
import os
import re

import easyplot

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the relevant file
with codecs.open(os.path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

import easyplot
setup(name='EasyPlot',
      version=easyplot.__version__,
      description='A matplotlib wrapper for fast and easy generation of reusable plots',
      author='Sudeep Mandal',
      author_email='sudeepmandal@gmail.com',
      url='https://github.com/HamsterHuey/easyplot',
      packages=['easyplot'],
      data_files = [('', ['LICENSE.txt']),
                    ('', ['README.html']),
                    ('', ['CHANGELOG.txt']),
                    ('examples', ['examples/ex1_percentage_indicator_stderr.py']),
                    ('examples', ['examples/ex1_percentage_indicator_stdout.py']),
                    ('examples', ['examples/ex1_progress_bar_stderr.py']),
                    ('examples', ['examples/ex1_progress_bar_stdout.py']),
                    ('examples', ['examples/ex2_percent_indicator_allargs.py']),
                    ('examples', ['examples/ex2_progressbar_allargs.py']),
                    ('examples', ['examples/ex3_percentage_indicator_monitor.py']),
                    ('examples', ['examples/ex3_progress_bar_monitor.py']),
                   ],
      install_requires = ['matplotlib'],
      license='MIT',
      platforms='any',
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Development Status :: 4 - Beta',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.1',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
      ],
      long_description = long_description,
      keywords='matplotlib wrapper plot easyplot',

    )