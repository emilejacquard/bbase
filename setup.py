from setuptools import setup, find_packages
from bbase import __version__

setuptools.setup(
    name='bbase',
    install_requires=['numpy>=1.24.2'],
    python_requires=">=3.10",
    version=__version__,
    author='Emile Jacquard',
    author_email='emile.jacquard@maths.ox.ac.uk',
    packages=find_packages(),
    url='https://github.com/emilejacquard/bbase',
)
