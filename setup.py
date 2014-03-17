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
      packages = ['fscc', 'fscc.tools'],
      data_files=data_files,
      requires=requirements,
      )
