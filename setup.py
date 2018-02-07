from setuptools import setup

config = {
    'name': 'pibackup',
    'version': '0.0.10',
    'author': 'p1ppo',
    'packages': ['pibackup', 'lib'],
    'include_package_data': True,
    'description': ('Scheduled cloud backup for Raspberry Pi running smart ' +
                    'home systems like fhem or iobroker'),
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
