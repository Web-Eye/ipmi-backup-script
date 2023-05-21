# -*- coding: utf-8 -*-
# Copyright 2023 WebEye
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import json
import sys
import os
import argparse


def getDefaultConfigFile():
    if sys.platform == "linux" or sys.platform == "linux2":
        return '/etc/ipmi-backup.config'

    elif sys.platform == "darwin":
        # MAC OS X
        return None

    elif sys.platform == "win32":
        return 'C:\\python\\etc\\ipmi-backup.config'

    return None


def getDefaultLogFile():
    if sys.platform == "linux" or sys.platform == "linux2":
        return '/var/log/ipmi-backup.log'

    elif sys.platform == "darwin":
        # MAC OS X
        return None

    elif sys.platform == "win32":
        return 'C:\\python\\log\\ipmi-backup.log'

    return None


def getConfig(args):
    config = {}
    config_file = args.config
    if os.path.isfile(config_file):
        with open(config_file) as json_data_file:
            config = json.load(json_data_file)

    if 'ipmi' not in config:
        config['ipmi'] = {}

    if 'server' not in config:
        config['server'] = {}

    if 'client' not in config:
        config['client'] = {}

    if 'rsnapshot' not in config:
        config['rsnapshot'] = {}

    if 'log' not in config:
        config['log'] = {}

    if 'mail' not in config:
        config['mail'] = {}

    if args.ipmi_host:
        config['ipmi']['host'] = args.ipmi_host


    print(config)

def main():
    parser = argparse.ArgumentParser(
        description='runner',
        epilog="That's all folks"
    )

    parser.add_argument('-c', '--config',
                        metavar='manual config file',
                        default=getDefaultConfigFile(),
                        type=str)

    parser.add_argument('-ih', '--impi-host',
                        dest='ipmi_host',
                        metavar='impi host',
                        type=str)

    parser.add_argument('-iu', '--impi-user',
                        dest='ipmi_user',
                        metavar='impi username',
                        type=str)

    parser.add_argument('-ip', '--impi-password',
                        dest='ipmi_pass',
                        metavar='impi password',
                        type=str)

    parser.add_argument('-sip ', '--server-ip',
                        dest='server_ip',
                        metavar='server ip',
                        type=str)

    parser.add_argument('-sto', '--server-timeout',
                        dest='server_timeout',
                        metavar='timeout till server is up',
                        type=int,
                        default=120)

    parser.add_argument('-smp', '--server-mountpoint',
                        dest='server_mountpoint',
                        metavar='server mount point',
                        type=str)

    parser.add_argument('-cmp', '--client-mountpoint',
                        dest='client_mountpoint',
                        metavar='client mount point',
                        type=str)

    parser.add_argument('-rss', '--rsnapshot-script',
                        dest='rsnapshot_script',
                        metavar='rsnapshot script',
                        type=str)

    parser.add_argument('-rsc', '--rsnapshot-command',
                        dest='rsnapshot_command',
                        metavar='rsnapschot command',
                        type=str)

    parser.add_argument('-lf', '--log-file',
                        dest='log_file',
                        metavar='manual log file',
                        default=getDefaultLogFile(),
                        type=str)

    parser.add_argument('-ll', '--log-level',
                        dest='log_level',
                        metavar='log level',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        type=str)

    parser.add_argument('-mf', '--mail-fromaddr',
                        dest='mail_addrfrom',
                        metavar='manual mail from address',
                        type=str)

    parser.add_argument('-mt', '--mail-toaddr',
                        dest='mail_toaddr',
                        metavar='mail to address',
                        type=str)

    try:
        args = parser.parse_args()
    except SystemExit:
        sys.exit()

    config = getConfig(args)


if __name__ == '__main__':
    main()
