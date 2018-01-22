from setuptools import setup
import codecs
import os

def read_readme():
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()
    return long_description

setup(
      # Basic information
      name='biosim',
      version='0.1.0',

      # Packages to include
      packages=['biosim', 'biosim.tests'],

      # Required packages not included in Python standard library
      requires=['pytest', 'numpy', 'matplotlib', 'pandas', 'textwrap', 'random', 'copy', 'math'],

      # Metadata
      description='A Herbivores and Carnivores Simulation',
      long_description=read_readme(),
      author='Lars Martin Lied, Jon-Fredrik Cappelen, NMBU',
      author_email='lars.martin.boe.lied@nmbu.no, jon-fredrik.blakstad.cappelen@nmbu.no',
      url='https://bitbucket.org/g04_jon_lars/biosim_g04_jon_lars',
      keywords='simulation game',
      license='MIT License',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Science :: Stochastic processes',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        ]
)