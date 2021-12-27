import os
import shutil
import sys
from cx_Freeze import setup, Executable

__version__ = '1.0.0'
base = None
if sys.platform == 'win32':
    base = 'Win32'


includes = ['pkg']
packages = ['numpy', 'bs4', 'lxml', 'shutil', 'pkg']

setup(
    name='MigrateAndMask',
    description='Copy all config files to new folders and mask them based on config.json',
    version=__version__,
    executables=[Executable('main.py')],
    options = {'build_exe': {
        'packages': packages,
        'includes': includes,
        'include_msvcr': True,
    }},
)

path = os.path.abspath(os.path.join(os.path.realpath(__file__), os.pardir))
build_path = os.path.join(path, 'build', 'exe.win32-3.7')