import os
import datetime
from time import sleep
import logging
from pkg_resources import resource_filename
import json
import pathlib

import schedule

from pibackup.helpers import schedule_weekly

import sys
# from helpers import rclone
# from sh import rsync
# from helpers import terminal_command


HOME_FOLDER = str(pathlib.Path.home()) + '/'


# -----> setup logging <-----
# initialize logging
logging.basicConfig(filename=HOME_FOLDER+'pibackup.log',
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%d/%m/%Y %I:%M:%S %p')
# example messages from tutorial, just here as a reminder
# logging.debug('This message should go to the log file')
# logging.info('So should this')
# logging.warning('And this, too')

try:
    config_file = open(HOME_FOLDER + '.config/pibackup/config.json', 'r')
except:
    config_file_path = resource_filename('pibackup', './config.json')
    config_file = open(config_file_path, 'r')

config_json = config_file.read()
config_data = json.loads(config_json)
config_file.close()


# default on production system, i.e. raspberry
# HOME_FOLDER = config_data['folders']['home']

# system can be 'fhem' or 'iobroker'
SMART_HOME_SYSTEM = config_data['system']['type']
# OPERATING_FOLDER = HOME_FOLDER + "fhem.files/"
# BACKUP_FOLDER_PIBACKUP = OPERATING_FOLDER + "backups/"

if SMART_HOME_SYSTEM == 'fhem':
    BACKUP_FOLDER_SMART_HOME_SYSTEM = "/opt/fhem/backup/"
elif SMART_HOME_SYSTEM == 'iobroker':
    BACKUP_FOLDER_SMART_HOME_SYSTEM = "/opt/iobroker/backups/"
else:
    logging.warning('>>> system entry not valid (use "fhem" or "iobroker")')
    logging.warning('>>> stopping execution of backup system')
    sys.exit()

# DAY_FOR_BACKUP = "Wednesday"
DAY_FOR_BACKUP = config_data['schedules']['backup_local']
FILES_TO_KEEP_IN_BACKUP = 5
# DAY_FOR_CLEANUP_BACKUP_FOLDER = "Thursday"
DAY_FOR_CLEANUP_BACKUP_FOLDER = config_data['schedules']['clean_local']
# DAY_FOR_LOCAL_MIRRORING = "Friday"
# DAY_FOR_CLOUD_MIRRORING = "Sunday"
DAY_FOR_CLOUD_MIRRORING = config_data['schedules']['cloud_sync']
EXECUTION_TIME = "03:00"
DATE_FOR_REBOOT = 15

# for raspberry
rclone_resource_filename = resource_filename('pibackup', '../lib/rclone')
# for windows
# rclone_resource_filename = resource_filename('pibackup', '../lib/rclone.exe')
# on Mac
# rclone_resource_filename = resource_filename('pibackup', '../lib/rclone')
RCLONE_PATH = '"' + os.path.abspath(rclone_resource_filename) + '"'
RCLONE_DRIVE = config_data['rclone']['drive_name']
if RCLONE_DRIVE[-1] != ":": RCLONE_DRIVE += ":"
RCLONE_BACKUP_PATH = RCLONE_DRIVE + config_data['rclone']['cloud_path']


def main():
    """ Main routine controlling actions of backup system. """
    initialize_jobs()
    while True:
        schedule.run_pending()
        sleep(1)


def initialize_jobs():
    """ Configure scheduling of tasks that shall run periodically. """
    # test job to see whether scheduling is working
    # schedule.every(5).seconds.do(lambda: print('scheduled output...'))

    # initialize backup process
    if SMART_HOME_SYSTEM == "fhem":
        schedule_weekly(DAY_FOR_BACKUP, EXECUTION_TIME, fhem_backup)
    elif SMART_HOME_SYSTEM == "iobroker":
        schedule_weekly(DAY_FOR_BACKUP, EXECUTION_TIME, iobroker_backup)

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
    cmd = 'sudo iobroker backup'
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
        try:
            # os.remove(tp[0])
            os.system('sudo rm ' + tp[0])
            logging.debug('Deleted excess old file: ' + tp[0])
        except:
            logging.info('Could not delete old file ' + tp[0])
            logging.info('Please add user to sudoers group')

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
