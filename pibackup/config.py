"""
Shall help to run rclone setup
and put config file for pibackup in place
config file carries info to run backup system
if not present standard parameters shall be used
"""

from pkg_resources import resource_filename
import os
import pathlib


HOME_DIR = str(pathlib.Path.home()) + '/'


def config_rclone():
    # for mac system
    # rclone_path = resource_filename('pibackup', '../lib/rclone_mac')
    # for raspberry
    print('\n\n\npibackup - smart home backup system')
    print('>>> main >>> rclone config\n')
    rclone_path = resource_filename('pibackup', '../lib/rclone')
    rclone_abspath = '"' + os.path.abspath(rclone_path) + '"'
    os.system(rclone_abspath + ' config')
    return


def user_output(lines):
    line_length = max(map(lambda item: len(item), lines))
    print('\n' * 3)
    print('-' * line_length)
    for line in lines:
        print(line)
    print('-' * line_length)
    return


def config_pibackup():
    answer = ''
    while answer != 'q':
        print('\n\n\npibackup - smart home backup system')
        print('>>> main >>> pibackup config file\n')
        print('c) Copy config template to ~/.config/pibackup')
        print('q) Quit config')
        answer = input('c/q> ').lower()
        # if answer not in ['c', 'q']:
            # config_pibackup()
        if answer == 'c':
            config_file_template = resource_filename('pibackup', './config.json')
            config_file_path = HOME_DIR + '.config/pibackup/config.json'

            if not os.path.exists(HOME_DIR + '.config/pibackup/'):
                cmd = 'mkdir -p ' + HOME_DIR + '.config/pibackup'
                os.system(cmd)

            if not os.path.exists(config_file_path):
                cmd = 'cp ' + config_file_template + ' ' + config_file_path
                os.system(cmd)
                user_output(['>>> created config file at ' + config_file_path,
                             'Please edit in text editor of your choice',
                             'Make sure to enter right system (fhem or iobroker)',
                             'Please specify also backup directory on cloud drive'])
                break
            else:
                user_output(['>>> config file already exists at ' + config_file_path])
                break
    return


def add_cron_job():
    from crontab import CronTab
    cron = CronTab(user=True)
    job = cron.new(command='/usr/local/bin/pibackup &')
    job.every_reboot()
    cron.write()
    user_output(['>>> Added new cron job to user cron table'])
    return


def main():
    answer = ''
    while answer != 'q':
        print('\n\n\npibackup - smart home backup system')
        print('>>> main\n')
        print('s) Setup config file for pibackup')
        print('c) Configure rclone cloud drive')
        print('a) Add cron job at reboot to start backup')
        print('q) Quit config')
        answer = input('s/c/q> ').lower()
        # if answer not in ['s', 'c', 'q']:
            # main()
        if answer == 'c':
            config_rclone()
        elif answer == 's':
            config_pibackup()
        elif answer == 'a':
            add_cron_job()
    user_output(['After configuration you can run pibackup through reboot or',
                 '> pibackup &',
                 '> disown'
                 ])


if __name__ == "__main__":
    main()

