import setuptools
import sys

import pip

pip_version = tuple([int(x) for x in pip.__version__.split('.')[:3]])
if pip_version < (9, 0, 1) :
    raise RuntimeError('Version of pip less than 9.0.1, breaking python ' \
                       'version requirement support')

with open('version.txt', 'rb') as h:
    version = h.read().decode('utf-8').rstrip('\n')


setuptools.setup(
    name = 'nvim_session',
    version = version,
    py_modules = ['nvim_session'],
    python_requires = '>=3.6',
    entry_points = {
        'console_scripts': [
            'nvim-sess=nvim_session:entry_point'
        ]
    },

    author = 'lf',
    author_email = 'github@lfcode.ca',
    description = 'Utility for managing dtach sessions for neovim',
    license = 'MIT',
    keywords = 'neovim'.split(' '),
    url = 'https://github.com/lf-/nvim-session'
)
