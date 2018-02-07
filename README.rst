pibackup
========


.. image:: https://img.shields.io/badge/pibackup-pypi-green.svg
        :target: https://pypi.python.org/pypi/pibackup


Who ever has suffered from corrupted SD-cards, even if new and "high quality" - here's relief.
A scheduled configure-once-and-forget-it backup solution
for smart home systems running on linux base, esp Raspberry Pi.
Covered at date are fhem and iobroker.

Building on the well made pieces of software `rclone <https://github.com/ncw/rclone>`_ and `schedule <https://github.com/dbader/schedule>`_.

Features
--------
- Install once and forget
- Lightweight background process
- Automatic weekly backup of smart home system
- Taking care of backup hygiene, i.e. keeping only defined number of backups
- Mirroring backups to cloud drive of choice (take what you have, gdrive, dropbox, you name it)
- Tested on Python 3.6

Prerequisites
-------------
Python 3.6 with pip

Usage
-----

Install from PyPi

.. code-block:: bash

    $ sudo pip3 install pibackup

Run config

.. code-block:: bash

    $ pibackup-config
    
    ibackup - smart home backup system
    >>> main
    
    s) Setup config file for pibackup
    c) Configure rclone cloud drive
    a) Add cron job at reboot to start backup
    q) Quit config
    s/c/q>

...and go through the simple three steps within the dialogue:

1. generate config file (enter s)
2. setup rclone (enter c)
3. generate crontab entry to run at boot (enter a)

Just follow the instructions on screen.

.. code-block:: bash

    more to follow...

Finally edit ~/.conf/pibackup/config.json to your liking, especially adapt

1. system type (fhem or iobroker)
2. backup folder name for cloud drive

.. code-block:: json

    {
        "system": {
            "type": "fhem"
        },
        "rclone": {
            "drive_name": "drive:",
            "cloud_path": "/backups/fhem/"
        },
        "schedules": {
            "backup_local": "Wednesday",
            "clean_local": "Thursday",
            "cloud_sync": "Sunday"
        }
    }

    more to follow...

Documentation
-------------

More to follow.

.. pibackup's documentation at `pibackup.readthedocs.io <https://pibackup.readthedocs.io/>`_.

.. Please also check the FAQ there with common questions.

