from setuptools import setup

setup(name='cONMan',
      version='0.1',
      description='File transfer Application',
      url='https://github.com/akash-deep/cONMan/',
      author='akash-deep',
      author_email='akashdeepmandal1995@gmail.com',
      license='',
      packages=['conman'],
      install_requires=[
          'pyftpdlib',
	  'ftplib',
          'netifaces',
          'python-nmap',
          'python-tk',
      ],
      zip_safe=False)
