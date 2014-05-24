from distutils.core import setup
# from setuptools import setup, find_packages
import codecs
import os
import re
import glob

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
                    ('', ['DESCRIPTION.rst']),
                    ('', ['README.md']),
                    ('', ['README.rst']),
                    ('', ['README.html']),
                    ('', ['CHANGELOG.txt']),
                    ('images', glob.glob('images/*.png')),
                    ('docs', glob.glob('docs/*.ipynb')),
                   ],
      # requires = ['matplotlib'],
      license='MIT',
      platforms='any',
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Development Status :: 4 - Beta',
          'Programming Language :: Python :: 2.7',
      ],
      long_description = long_description,
      keywords='matplotlib wrapper plot easyplot',

    )