import os
from distutils.core import setup

if os.name == 'nt':
    requirements = ['win32']
    data_files=[('DLLs', ['cfscc.dll'])]
else:
    requirements = []
    data_files=[('DLLs', ['libcfscc.so', 'libcfscc.so.6'])]

setup(name='pyfscc',
      version='1.1.0',
      url='https://github.com/commtech/pyfscc',
      author='William Fagan',
      author_email='willf@commtech-fastcom.com',
      description='Library for the FSCC family of serial cards.',
      long_description=__doc__,
      packages = ['fscc', 'fscc.tools'],
      data_files=data_files,
      requires=requirements,
      )
