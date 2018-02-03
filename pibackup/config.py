"""
Shall help to run rclone setup
and put config file for pibackup in place
config file carries info to run backup system
if not present standard parameters shall be used
"""

from pkg_resources import resource_filename
import os


def config_rclone():
    # for mac system
    # rclone_path = resource_filename('pibackup', '../lib/rclone_mac')
    # for raspberry
    rclone_path = resource_filename('pibackup', '../lib/rclone')   
    rclone_abspath = '"' + os.path.abspath(rclone_path) + '"'
    os.system(rclone_abspath + ' config')
    main()


def config_pibackup():
    print('\npibackup - smart home backup system')
    print('>>> main >>> pibackup config file\n')
    print('c) Copy config template to ~/.config/pibackup')
    print('q) Quit config')
    answer = input('c/q> ').lower()
    if answer not in ['c', 'q']:
        config_pibackup()
    if answer == 'c':
        pass
    main()


def main():
    print('\npibackup - smart home backup system')
    print('>>> main\n')
    print('s) Setup config file for pibackup')
    print('c) Configure rclone cloud drive')
    print('q) Quit config')
    answer = input('s/c/q> ').lower()
    if answer not in ['s', 'c', 'q']:
        main()
    if answer == 'c':
        config_rclone()
    elif answer == 's':
        config_pibackup()


main()
