pibackup
========


.. image:: https://img.shields.io/badge/pibackup-pypi-green.svg
        :target: https://pypi.python.org/pypi/pibackup


Who ever has suffered from corrupted SD-cards, even if new and "high quality" - here's relief.
A scheduled *configure-once-and-forget-it* backup solution
for smart home systems running on linux base, e.g. Raspberry Pi.
Covered at date are fhem and iobroker. Feel free to request or contribute extensions.

Building on the well made pieces of software `rclone <https://rclone.org/>`_ and `schedule <https://github.com/dbader/schedule>`_.


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


1. Install from PyPi
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: bash

    $ sudo pip3 install pibackup

It is encouraged, though not necessary, to install and execute within a virtual environment.
For further information on this, read about `virtualenv <https://virtualenv.pypa.io/en/latest/>`_ or `venv <https://docs.python.org/3/library/venv.html>`_.


2. Run config
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Simply invoke from the command line:

.. code-block:: bash

    $ pibackup-config



This calls a dialogue to set up the system. Essentially, you follow three steps, which are:
- generate a config file (enter s)
- setup rclone (enter c)
- generate a crontab entry to start the process at boot (enter a)


The dialogue looks like this.

.. code-block:: bash

    ***********************************************
    ***   pibackup - smart home backup system   ***
    ***********************************************
    >>> main
    
    s) Setup config file for pibackup
    c) Configure rclone cloud drive
    a) Add cron job at reboot to start backup
    q) Quit config
    
    s/c/a/q> 

Navigate by entering the respective letter. Start with creating the config file:

On setting up the config file
"""""""""""""""""""""""""""""

.. code-block:: bash
    
    ***********************************************
    ***   pibackup - smart home backup system   ***
    ***********************************************
    >>> main >>> pibackup config file
    
    c) Copy config template to ~/.config/pibackup
    q) Quit this page (go back)
    
    c/q>

Entering "c" creates a copy of the config file in the home directory.

Do this and return to the main screen with "q".

After this, in the main screen, enter "c" to navigate to the rclone setup.


On configuring rclone
"""""""""""""""""""""

This leads straight into the configuration dialogue of rclone itself. As pibackup is a wrapper using rclone, you are now interacting with rclone directly.

The tool is very well documented `here <https://rclone.org>`_. Please have a peek and check the section related to the backup storage you want to use. Typically remote drives such as Google Drive, Dropbox, Box or OneDrive might be in use at your end and considered for storing the backup. While you can use pretty much *everything*, please find links to popular choices:

- `Google Drive <https://rclone.org/drive/>`_
- `Dropbox <https://rclone.org/dropbox/>`_
- `Box <https://rclone.org/box/>`_
- `OneDrive <https://rclone.org/onedrive/>`_


As mentioned above: Wherever the documentation asks you to run "rclone config", this is what you are actually doing in the pibackup dialogue already.



On adding the cron job
""""""""""""""""""""""

Back in the main dialogue, select "a" to amend the crontab, which adds an entry to start the backup process at every reboot.

If you want to double check, do this with:

.. code-block:: bash

    $ crontab -l




3. Edit config file for customization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

- which *system* type is in use
- which parameters to use for *rclone*
- Which *schedule* to follow for the main tool actions


On system type
"""""""""""""""""""""""""""""
Currently the system *types* "fhem" or "iobroker" are supported and can be used as values.


On rclone parameters 
"""""""""""""""""""""""""""""
The *drive name* identifies the remote storage location you created in the rclone setup. Please enter the name you used there. Please include the colon at the end, like "drive:" (in the documentation examples it is often "remote:")


The *cloud path* specifies the folder on the remote drive. Choose to your liking.



On schedules
"""""""""""""""""""""""""""""

Typically you can leave this as is. The parameters are pretty verbose:

- *backup_local* schedules the weekday on which the smart phone system backups are run.
- *clean_local* schedules the weekday on which the local maintenance on the backup folder is being done.
- *cloud_sync* schedules the weekday on which the sync to the cloud drive is performed.



4. Reboot and feel comfortable...
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Nice, you did something good for yourself. Congrats and enjoy.

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
