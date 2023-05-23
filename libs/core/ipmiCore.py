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

import subprocess

class ipmiCore:

    def __init__(self, host, username, password):
        self._host = host
        self._username = username
        self._password = password
        self._baseCommand = ['ipmitool', '-H', self._host, '-U', self._username, '-P', self._password]

    def _call(self, command):
        try:
            process = subprocess.run(command, capture_output=True, text=True)
            err = process.returncode
            if err != 0:
                return err, process.stderr.split(chr(10))[0]
            else:
                return err, process.stdout

        except FileNotFoundError as ex:
            return -1, ex

    def getChassisPowerStatus(self):
        command = self._baseCommand + ['chassis', 'power', 'status']
        err, out = self._call(command)

        if err != 0:
           return err, out
        else:
            if out is not None:
                line = out.split(chr(10))
                if line is not None and len(line) > 0:
                    if line[0] == 'Chassis Power is on':
                        return 0, 'on'
                    elif line[0] == 'Chassis Power is off':
                        return 0, 'off'

            return -1, out

    def setChassisPower(self, status):
        command = self._baseCommand + ['chassis', 'power', status]
        err, out = self._call(command)

        if err != 0:
            return err, out
        else:
            if out is not None:
                line = out.split(chr(10))
                print(line[0])
                if line is not None and len(line) > 0:
                    if line[0] == 'Chassis Power Control: Up/On':
                        return 0, 'on'
                    elif line[0] == 'Chassis Power is off':
                        return 0, 'off'

            return -1, out
