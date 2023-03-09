from setuptools import setup
import os
import re

# Get version string from module
init_path = os.path.join(os.path.dirname(__file__), "bbase/__init__.py")
with open(init_path, "r", encoding="utf8") as f:
    version = re.search(r"__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M).group(1)
setuptools.setup(
    name='bbase',
    install_requires=['numpy'],
    version='0.0.1',
    author='Emile Jacquard',
    author_email='emile.jacquard@maths.ox.ac.uk',
    url='https://github.com/emilejacquard/bbase',
    packages=['bbase']
)
