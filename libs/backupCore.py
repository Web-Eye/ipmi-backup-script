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
import logging
import logging.handlers
import os.path
import subprocess
import sys
import time

from libs.common.BufferingSMTPHandler import BufferingSMTPHandler
from libs.common.fsTools import mount, umount, getDiskUsage, getHumanityDiskUsage
from libs.common.netTools import canPing
from libs.core.ipmiCore import ipmiCore


class backupCore:

    def __init__(self, config):
        self._config = config

        self._logger = logging.getLogger()
        _log_handler = logging.FileHandler(self._config['log']['filename'])
        _str_log_level = self._config['log']['level']
        _log_level = getattr(logging, _str_log_level)
        self._logger.setLevel(_log_level)
        _log_handler.setLevel(_log_level)

        _log_format = logging.Formatter('%(asctime)s - %(levelname)-8s - %(message)s')
        _log_handler.setFormatter(_log_format)

        self._logger.addHandler(_log_handler)

        _mail_handler = BufferingSMTPHandler('localhost', self._config['mail']['fromaddr'],
                                             [self._config['mail']['toaddr']], 'ipmi backup', 500)
        _mail_handler.setLevel(logging.DEBUG)
        self._logger.addHandler(_mail_handler)

        ipmiDict = self._config['ipmi']
        self._ipmi = ipmiCore(ipmiDict['host'], ipmiDict['user'], ipmiDict['password'])

    def startIPMIServer(self):
        server_host = self._config['server']['host']
        server_timeout = self._config['server']['timeout']
        err, status = self._ipmi.getChassisPowerStatus()
        self._logger.debug(f'ipmi.getChassisPowerStatus() returns {err}, {status}')
        if err != 0:
            return False

        if status == 'on':

            self._logger.debug(f'mutual exclusion: can\'t ping {server_host}, but chassis power status is on')
            return False

        err, status = self._ipmi.setChassisPower('on')
        self._logger.debug(f'ipmi.setChassisPower() returns {err}, {status}')
        if err != 0:
            return False

        if status != 'on':
            self._logger.debug(f'unable to power on server {server_host}....')
            return False

        timeout = time.time() + server_timeout
        while True:
            time.sleep(0.25)
            if time.time() > timeout:
                break
            if canPing(server_host):
                break

        if not canPing(self._config['server']['host']):
            self._logger.debug(f'timeout: start server {server_host}....')
            return False

        return True

    def stopIPMIServer(self):
        err, status = self._ipmi.setChassisPower('soft')
        self._logger.debug(f'ipmi.setChassisPower() returns {err}, {status}')

    def getHumanityTime(self, time_elapsed):
        mm, ss = divmod(time_elapsed, 60)
        hh, mm = divmod(mm, 60)

        if hh > 0 and mm > 0 and ss > 0:
            return f'{hh} hours, {mm} minutes and {ss} seconds'
        elif mm > 0 and ss > 0:
            return f'{mm} minutes and {ss} seconds'
        elif ss > 0:
            return f'{ss} seconds'

        return 'no time'

    def getAverageSpeed(self, disk_usage, time_elapsed):
        avg = disk_usage / time_elapsed
        return f'{getHumanityDiskUsage(avg)}/s'

    def executeSnapshot(self):

        self._logger.info('start rsnapshot')
        rsnapshot_script = self._config['rsnapshot']['script']
        rsnapshot_command = self._config['rsnapshot']['command']

        start_time = time.time()
        command = ['/usr/bin/rsnapshot', '-c', rsnapshot_script, rsnapshot_command]
        process = subprocess.run(command, capture_output=True, text=True)
        err = process.returncode
        if err != 0:
            self._logger.critical(f'rsnapshot returned {err}, {process.stderr.split(chr(10))[0]}')
            return

        time_elapsed = time.time() - start_time
        ht = self.getHumanityTime(time_elapsed)
        disk_usage = getDiskUsage(os.path.join(self._config['rsnapshot']['root_folder'], f'{rsnapshot_command}.0'))
        hdu = getHumanityDiskUsage(disk_usage)
        hAverageSpeed = self.getAverageSpeed(disk_usage, time_elapsed)

        self._logger.info(f'stored {hdu} in {ht} ({hAverageSpeed})')



    def shuttingDown(self, status):
        self._logger.info('Shutting down backup core...')
        logging.shutdown()
        sys.exit(status)

    def run(self):
        server_ip = self._config['server']['host']
        self._logger.info('starting backup core...')
        self._logger.debug(f'ping {server_ip}')
        if not canPing(server_ip):
            self._logger.info(f'server {server_ip} is down, try tp start it.')
            if not self.startIPMIServer():
                self._logger.critical(f'Unable to start server {server_ip}')
                self.shuttingDown(1)

        self._logger.debug(f'server {server_ip} is up.')

        server_mountpoint = self._config['server']['mountpoint']
        client_mountpoint = self._config['client']['mountpoint']
        serverPath = f'{server_ip}:{server_mountpoint}'

        if not os.path.ismount(client_mountpoint):
            self._logger.debug(f'mounting {serverPath} to {client_mountpoint}')
            if not mount('nfs', serverPath, client_mountpoint):
                self._logger.critical('unable to mount.')
                # self._logger.info(f'shutting down server {server_ip}.')
                # self.stopIPMIServer()
                self.shuttingDown(1)
        else:
            self._logger.debug(f'already mounted {serverPath} to {client_mountpoint}')

        self.executeSnapshot()
        self._logger.debug(f'unmounting {server_mountpoint} to {client_mountpoint}')
        if not umount(client_mountpoint):
            self._logger.critical('unable to umount.')
            self.shuttingDown(1)

        self._logger.info(f'shutting down server {server_ip}.')
        self.stopIPMIServer()
        self.shuttingDown(1)
