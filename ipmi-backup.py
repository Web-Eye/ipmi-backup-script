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

from libs.backupCore import backupCore


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

    if args.ipmi_user:
        config['ipmi']['user'] = args.ipmi_user

    if args.ipmi_pass:
        config['ipmi']['password'] = args.ipmi_pass

    if args.server_host:
        config['server']['host'] = args.server_host

    if args.server_timeout:
        config['server']['timeout'] = args.server_timeout

    if args.server_mountpoint:
        config['server']['mountpoint'] = args.server_mountpoint

    if args.client_mountpoint:
        config['client']['mountpoint'] = args.client_mountpoint

    if args.rsnapshot_script:
        config['rsnapshot']['script'] = args.rsnapshot_script

    if args.rsnapshot_command:
        config['rsnapshot']['command'] = args.rsnapshot_command

    if args.log_file:
        config['log']['filename'] = args.log_file

    if args.log_level:
        config['log']['level'] = args.log_level

    if args.mail_fromaddr:
        config['mail']['fromaddr'] = args.mail_fromaddr

    if args.mail_toaddr:
        config['mail']['toaddr'] = args.mail_toaddr

    if not config['log'].get('filename'):
        config['log']['filename'] = getDefaultLogFile()

    if not config['log'].get('level'):
        config['log']['level'] = 'INFO'

    return config


def validateConfig(config):
    if config is None:
        print("broken config")
        return False

    if config.get('ipmi') is None:
        print("broken config (ipmi)")
        return False

    if config.get('server') is None:
        print("broken config (server)")
        return False

    if config.get('client') is None:
        print("broken config (client)")
        return False

    if config.get('rsnapshot') is None:
        print("broken config (rsnapshot)")
        return False

    if config.get('log') is None:
        print("broken config (log)")
        return False

    if config.get('mail') is None:
        print("broken config (mail)")
        return False

    if config['ipmi'].get('host') is None:
        print("broken config (ipmi.host)")
        return False

    if config['ipmi'].get('user') is None:
        print("broken config (ipmi.user)")
        return False

    if config['ipmi'].get('password') is None:
        print("broken config (ipmi.password)")
        return False

    if config['server'].get('host') is None:
        print("broken config (server.host)")
        return False

    if config['server'].get('timeout') is None:
        print("broken config (server.timeout)")
        return False

    if config['server'].get('mountpoint') is None:
        print("broken config (server.mountpoint)")
        return False

    if config['client'].get('mountpoint') is None:
        print("broken config (client.mountpoint)")
        return False

    if config['rsnapshot'].get('script') is None:
        print("broken config (rsnapshot.script)")
        return False

    if config['rsnapshot'].get('command') is None:
        print("broken config (rsnapshot.command)")
        return False

    if config['log'].get('filename') is None:
        print("broken config (log.filename)")
        return False

    if config['log'].get('level') is None:
        print("broken config (log.level)")
        return False

    if config['mail'].get('fromaddr') is None:
        print("broken config (mail.fromaddr)")
        return False

    if config['mail'].get('toaddr') is None:
        print("broken config (mail.toaddr)")
        return False

    return True


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

    parser.add_argument('-sh ', '--server-host',
                        dest='server_host',
                        metavar='server host',
                        type=str)

    parser.add_argument('-sto', '--server-timeout',
                        dest='server_timeout',
                        metavar='timeout till server is up',
                        type=int)

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
                        type=str)

    parser.add_argument('-ll', '--log-level',
                        dest='log_level',
                        metavar='log level',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        type=str)

    parser.add_argument('-mf', '--mail-fromaddr',
                        dest='mail_fromaddr',
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
    if not validateConfig(config):
        sys.exit()

    b = backupCore(config)
    b.run()


def main2():
    import subprocess

    output = subprocess.run(['ipconfig.exe'], capture_output=True, text=True)
    stout = output.stdout
    s = stout.split(chr(10))
    for l in s:
        print(l)


if __name__ == '__main__':
    main()
