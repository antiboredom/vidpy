import re
from setuptools import setup, find_packages

def find_version(fname):
    """Attempts to find the version number in the file names fname.
    Raises RuntimeError if not found.
    """
    version = ''
    with open(fname, 'r') as fp:
        reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
        for line in fp:
            m = reg.match(line)
            if m:
                version = m.group(1)
                break
    if not version:
        raise RuntimeError('Cannot find version information')
    return version


try:
    with open('README.rst') as readme:
        long_description = readme.read()
except IOError:
    long_description = ''

__version__ = find_version("vidpy/__init__.py")

setup(name='vidpy',
      version=__version__,
      description='Video editing and compositing in Python',
      long_description=long_description,
      url='https://antiboredom.github.io/vidpy',
      author='Sam Lavigne',
      author_email='lavigne@saaaam.com',
      license='MIT',
      packages=find_packages(),
      install_requires=['pillow'],
      zip_safe=False,
      test_suite='tests'
)
