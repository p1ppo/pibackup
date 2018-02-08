from setuptools import setup
import os
import sys


if sys.argv[-1] == "publish":
    os.system('python3 setup.py sdist bdist_wheel')
    os.system('python3 -m twine upload --skip-existing dist/*')
    sys.exit()


here = os.path.abspath(os.path.dirname(__file__))


about = {}
with open(os.path.join(here, "pibackup", "__version__.py"), "r") as f:
    exec(f.read(), about)

with open('README.rst', 'r') as f:
    readme = f.read()


config = {
    'name': about['__title__'],
    'version': about['__version__'],
    'author': about['__author__'],
    'packages': ['pibackup', 'lib'],
    'include_package_data': True,
    'description': ('Scheduled cloud backup for Raspberry Pi running smart ' +
                    'home systems like fhem or iobroker'),
    'long_description': readme,
    'license': about['__license__'],
    # 'zip_safe': False,
    # 'py_modules': [''],
    'package_data': {
        'lib': ['rclone', '*.json'],
        '': ['*.json']
    },
    'entry_points': {
        'console_scripts': [
            'pibackup = pibackup.app:main',
            'pibackup-config = pibackup.config:main'
        ]
    },
    # 'scripts': ['bin/bin-script'],
    'install_requires': ['schedule', 'python-crontab'],
}

setup(**config)
