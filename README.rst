pibackup
========


.. image:: https://img.shields.io/pypi/v/schedule.svg
        :target: https://pypi.python.org/pypi/pibackup


Who ever has suffered from corrupted SD-cards, even if new and "high quality" - here's relief.
A scheduled configure-once-and-forget-it backup solution
for smart home systems running on linux base, esp Raspberry Pi.
Covered at date are fhem and iobroker.

Building on the well made pieces of software `rclone' <https://github.com/ncw/rclone>`_ and `schedule <https://github.com/dbader/schedule>`_ .

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

.. code-block:: bash

    $ sudo pip3 install pibackup

.. code-block:: bash

    more to follow...

Documentation
-------------

More to follow.

.. pibackup's documentation at `pibackup.readthedocs.io <https://pibackup.readthedocs.io/>`_.

.. Please also check the FAQ there with common questions.

