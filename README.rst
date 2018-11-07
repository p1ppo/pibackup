pibackup
========


.. image:: https://img.shields.io/badge/pibackup-pypi-green.svg
        :target: https://pypi.python.org/pypi/pibackup


Who ever has suffered from corrupted SD-cards, even if new and "high quality" - here's relief.
A scheduled *configure-once-and-forget-it* backup solution
for smart home systems running on linux base, e.g. Raspberry Pi.
Covered at date are fhem and iobroker. Feel free to request or contribute extensions.

Building on the well made piece of software `rclone <https://rclone.org/>`_ and `schedule <https://github.com/dbader/schedule>`_.


Core functions and Features
---------------------------
- Create automatic weekly backup of smart home system
- Take care of backup hygiene, i.e. keeping reasonable number of backups and delete excess
- Mirroring backups to cloud drive of choice (take what you have, gdrive, dropbox, box, you name it)
- Install once and forget
- Running as lightweight background process
- Tested on Python >3.5


Prerequisites
-------------
Python >3.5 with pip


Usage
-----

Follow four easy steps:

1. Install from PyPi
2. Run the configuration dialogue
3. If required, customise the config file
4. Reboot and relax

The steps are described below in more detail.


Install from PyPi
^^^^^^^^^^^^^^^^^
.. code-block:: bash

    $ sudo pip3 install pibackup

It is encouraged, though not necessary, to install and execute within a virtual environment.
For further information on this, read about `virtualenv <https://virtualenv.pypa.io/en/latest/>`_.


Run config
^^^^^^^^^^

.. code-block:: bash

    $ pibackup-config

This invokes a simple dialogue to set up the system. Essentially, you execute three steps, which are:
    a. generate a config file (enter s)
    b. setup rclone (enter c)
    c. generate crontab entry to run at boot (enter a)

    
.. code-block:: bash

    pibackup - smart home backup system
    >>> main
    
    s) Setup config file for pibackup
    c) Configure rclone cloud drive
    a) Add cron job at reboot to start backup
    q) Quit config

    s/c/a/q>


On setting up the config file
"""""""""""""""""""""""""""""
.. code-block:: bash

    more to follow...


On configuring rclone
"""""""""""""""""""""

This leads straight into the configuration dialogue of rclone itself. The tool is very well documented `here <https://rclone.org>`_.

Typically remote drives such as Google Drive, Dropbox, Box or OneDrive might be in use at your end and considered for this purpose. You can use pretty much *everything*. There are respective instructions available (as few examples, explore to your liking further options including ftp, local storage, http and what not):

* `Google Drive <https://rclone.org/drive/>`_
* `Dropbox <https://rclone.org/dropbox/>`_
* `Box <https://rclone.org/box/>`_
* `OneDrive <https://rclone.org/onedrive/>`_


Wherever the documentation says run "rclone config", this is what you are actually doing in the pibackup dialogue already.



On adding the cron job
""""""""""""""""""""""

.. code-block:: bash

    more to follow...


Edit config file for customization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The config file is located at ~/.conf/pibackup/config.json.

It looks like this:


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


The three sections describe

1. which *system* type is in use (currently "fhem" or "iobroker" are supported and can be used as values)
2. which parameters to use for *rclone*

    a. The drive name identifies the remote storage location
    b. The cloud path defines which specific storage place to use on the remote storage location

3. Which *schedules* to follow for the main tool actions


On system type
"""""""""""""""""""""""""""""


On rclone parameters 
"""""""""""""""""""""""""""""


On schedules
"""""""""""""""""""""""""""""

Typically you can leave this as is. The parameters are pretty verbose:

*backup_local* schedules the weekday on which the smart phone system backups are run.

*clean_local* schedules the weekday on which the local maintenance on the backup folder is being done.

*cloud_sync* schedules the weekday on which the sync to the cloud drive is performed.



Reboot and feel comfortable...
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. Technical info
.. --------------
.. Essentially, the tool does two things:
..  1. Call periodically the backup command, that is built-in in the smart home system
..  2. Build a wrapper around rclone, and periodically sync the local backups to a defined remote drive
.. 
.. As mentioned before, some maintenance around number of backups kept is also provided, so that you obtain a reasonable reach in the past (e.g. 5 weeks), but don't spam your local (and the remote) drive with outdated backups.


Meta
----

Philipp Cremer - pc01@arcor.de

Distributed under the MIT license. See `LICENSE <https://github.com/p1ppo/pibackup/blob/master/LICENSE>`_ for more information.

https://github.com/p1ppo/pibackup
