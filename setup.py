from setuptools import setup, find_packages

try:
    with open('README.md') as readme:
        long_description = readme.read()
except IOError:
    long_description = ''

setup(name='vidpy',
      version='0.1.0',
      description='Video editing and compositing in Python',
      long_description=long_description,
      url='https://antiboredom.github.io/vidpy',
      author='Sam Lavigne',
      author_email='lavigne@saaaam.com',
      license='MIT',
      packages=find_packages('vidpy', exclude=['*.mp4', 'docs']),
      install_requires=['pillow'],
      zip_safe=False
)
