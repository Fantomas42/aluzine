"""Setup script of aluzine"""
from setuptools import find_packages
from setuptools import setup

__version__ = '1.0'
__license__ = 'BSD License'

__author__ = 'Fantomas42'
__email__ = 'fantomas42@gmail.com'

__url__ = 'https://github.com/Fantomas42/aluzine'


setup(
    name='aluzine',
    version=__version__,

    description='Automation of the time stamping, because we are not aluzine',
    long_description=open('README.rst').read(),
    keywords='time clock, time stamp',

    author=__author__,
    author_email=__email__,
    url=__url__,

    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Libraries :: Python Modules'],

    license=__license__,
    include_package_data=True,
    zip_safe=False,
    install_requires=['beautifulsoup4>=4.4',
                      'requests>=2.18'],

    entry_points={
        'console_scripts': [
            'aluz-in=aluzine.scripts.in:cmdline',
            'aluz-out=aluzine.scripts.out:cmdline'
            ]
    }
)
