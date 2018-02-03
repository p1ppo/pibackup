import os
import schedule


def rclone(rclone_path, parameter):
    os.system(rclone_path + ' ' + parameter)


def terminal_command(command, parameter=''):
    """
    Serves to execute shell commands. Simply pass command and
    parameters as strings.
    Sudo commands can be executed as well. format is
    echo SUDO_PSWD | sudo -S command parameters.
    """
    # os.system("ls -al")
    # os.system("echo " + SUDO_PSWD + " | sudo -S echo " + text)
    command_string = str(command + " " + parameter)
    os.system(command_string)


def schedule_weekly(day, time, func):
    day = day.lower()
    if day == "monday":
        schedule.every().monday.at(time).do(func)
    elif day == "tuesday":
        schedule.every().tuesday.at(time).do(func)
    elif day == "wednesday":
        schedule.every().wednesday.at(time).do(func)
    elif day == "thursday":
        schedule.every().thursday.at(time).do(func)
    elif day == "friday":
        schedule.every().friday.at(time).do(func)
    elif day == "saturday":
        schedule.every().saturday.at(time).do(func)
    elif day == "sunday":
        schedule.every().sunday.at(time).do(func)
