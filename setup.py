from setuptools import setup, find_packages

setup(name='dlogging',
      version='0.1',
      description='Distributed Logging Library',
      url='https://github.com/BenjiBackslash/dlogging',
      author='Hanan Wiener',
      author_email='hanan888@gmail.com',
      license='MIT',
      packages=find_packages(exclude=['contrib', 'docs', 'test*']),
      install_requires=['PyMongo==3.7.1', 'pyyaml==3.13'],
      zip_safe=False)
