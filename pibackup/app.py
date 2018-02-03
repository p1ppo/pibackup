import os
import datetime
from time import sleep
import logging
from pkg_resources import resource_filename

import schedule

from pibackup.helpers import schedule_weekly

# import sys
# from helpers import rclone
# from sh import rsync
# from helpers import terminal_command


# SUDO_PSWD = ""
# INSTALL_DIR = ""

# default on production system, i.e. raspberry
HOME_FOLDER = "/home/pi/"
# for testing on windows development system
# HOME_FOLDER = "/Users/pcremer-surface/"
# for testing on Mac
# HOME_FOLDER = "/Users/philipp/"

# system can be 'fhem' or 'iobroker'
SMART_HOME_SYSTEM = 'fhem'
# OPERATING_FOLDER = HOME_FOLDER + "./fhem.files/"
# BACKUP_FOLDER_PIBACKUP = OPERATING_FOLDER + "./backups/"

if SMART_HOME_SYSTEM == 'fhem':
    BACKUP_FOLDER_SMART_HOME_SYSTEM = "/opt/fhem/backup/"
elif SMART_HOME_SYSTEM == 'iobroker':
    BACKUP_FOLDER_SMART_HOME_SYSTEM = "/opt/iobroker/backup/"

DAY_FOR_BACKUP = "Wednesday"
FILES_TO_KEEP_IN_BACKUP = 5
DAY_FOR_CLEANUP_BACKUP_FOLDER = "Thursday"
# DAY_FOR_LOCAL_MIRRORING = "Friday"
DAY_FOR_CLOUD_MIRRORING = "Sunday"
EXECUTION_TIME = "03:00"
DATE_FOR_REBOOT = 15

# for raspberry
rclone_resource_filename = resource_filename('pibackup', '../lib/rclone')
# for windows
# rclone_resource_filename = resource_filename('pibackup', '../lib/rclone.exe')
# on Mac
# rclone_resource_filename = resource_filename('pibackup', '../lib/rclone')

RCLONE_PATH = '"' + os.path.abspath(rclone_resource_filename) + '"'
RCLONE_DRIVE = 'drive:'
RCLONE_BACKUP_PATH = RCLONE_DRIVE + '/backups/fhem-upstairs/'


def main():
    """ Main routine controlling actions of backup system. """

    # few test calls of functions
    # terminal_command('ls', '-al')
    # terminal_command("echo", "Hallo Welt!")
    # rclone(RCLONE_PATH, "lsd drive:")

    # -----> setup logging <-----
    # check if folder exists, if not create it
    # if not os.path.exists(OPERATING_FOLDER):
    #     os.makedirs(OPERATING_FOLDER)
    # initialize logging
    logging.basicConfig(filename=HOME_FOLDER+'pibackup.log',
                        level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%d/%m/%Y %I:%M:%S %p')

    # example messages from tutorial, just here as a reminder
    # logging.debug('This message should go to the log file')
    # logging.info('So should this')
    # logging.warning('And this, too')

    initialize_jobs()

    while True:
        schedule.run_pending()
        sleep(1)


def initialize_jobs():
    """ Configure scheduling of tasks that shall run periodically. """
    # test job to see whether scheduling is working
    # schedule.every(5).seconds.do(lambda: print('scheduled output...'))

    # initialize backup process
    schedule_weekly(DAY_FOR_BACKUP, EXECUTION_TIME, fhem_backup)
    # schedule_weekly(DAY_FOR_BACKUP, EXECUTION_TIME, iobroker_backup)

    # initialize cleanup of backup folder
    schedule_weekly(DAY_FOR_CLEANUP_BACKUP_FOLDER, EXECUTION_TIME,
                    clean_backup_folder)

    # initialize local mirroring
    # schedule_weekly(DAY_FOR_LOCAL_MIRRORING, EXECUTION_TIME,
    #                 mirror_local_backup_folders)

    # initialize cloud mirroring
    schedule_weekly(DAY_FOR_CLOUD_MIRRORING, EXECUTION_TIME,
                    mirror_local_folder_to_cloud)

    # initialize system reboot
    # scheduling only formally to every day; reboot routine checks whether date
    # is right, as should reboot every 15th of the month
    # schedule.every().day.at('01:00').do(reboot)


def fhem_backup():
    # get command line based perl command to do fhem backup
    directory_path = os.getcwd()
    os.chdir('/opt/fhem/')
    cmd = './fhem.pl 7072 "backup"'
    os.system(cmd)
    os.chdir(directory_path)


def iobroker_backup():
    # do iobroker backup in /opt/iobroker
    directory_path = os.getcwd()
    os.chdir('/opt/iobroker/')
    cmd = 'iobroker backup'
    os.system(cmd)
    os.chdir(directory_path)


def clean_backup_folder():
    # create path for backup folder of smart home system
    path = os.path.join(BACKUP_FOLDER_SMART_HOME_SYSTEM)

    # check if backup folder exists, else create
    if not os.path.isdir(path):
        os.mkdir(path)

    # check number of files in backup folder
    file_list = os.listdir(path)

    # if less than or equal to 5 files do not clean
    if len(file_list) <= FILES_TO_KEEP_IN_BACKUP:
        return

    # create list of files with creation time
    directory_path = os.getcwd()
    os.chdir(path)
    file_list_change_time = [(file, os.path.getctime(file))
                             for file in file_list]
    # for file in file_list:
    #     creation_time = os.path.getctime(file)
    #     file_list_change_time.append((file, creation_time))

    # sort by date or better change time
    file_list_change_time.sort(key=lambda tp: tp[1])

    # delete oldest until 5 left
    for tp in file_list_change_time[:-5]:
        os.remove(tp[0])

    # change back to old directory
    os.chdir(directory_path)


def mirror_local_backup_folders():
    # rsync fhem or iobroker backup folder to home folder based backup folder
    # cmd = ('rsync -va --delete --progress ' +
    #        BACKUP_FOLDER_SMART_HOME_SYSTEM +
    #        ' ' + BACKUP_FOLDER_PIBACKUP)
    # os.system(cmd)
    pass


def mirror_local_folder_to_cloud():
    # rclone home folder based fhem or iobroker folder to gdrive
    # cmd = ('/home/pi/fhem.files/bin/rclone -v sync ' +
    #        '/home/pi/fhem.files/backups/ ' +
    #        'drive:/backups/fhem.upstairs/')
    cmd = (RCLONE_PATH + ' -v sync ' +
           BACKUP_FOLDER_SMART_HOME_SYSTEM + ' ' +
           RCLONE_BACKUP_PATH)
    os.system(cmd)


def reboot():
    reboot_today = datetime.date.today().day == DATE_FOR_REBOOT
    if reboot_today:
        cmd = 'sudo reboot'
        os.system(cmd)
    else:
        pass


if __name__ == "__main__":
    main()
