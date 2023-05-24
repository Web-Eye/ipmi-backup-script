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
import decimal
import subprocess
from decimal import Decimal


def mount(filesystem, serverPath, clientPath):
    command = ['mount', '-t', filesystem, serverPath, clientPath]
    return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) == 0


def umount(clientPath):
    command = ['umount', clientPath]
    return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) == 0


def getDiskUsage(path):
    command = ['du', '-sb', path]
    process = subprocess.run(command, capture_output=True, text=True)
    err = process.returncode
    if err == 0:
        du = process.stdout.split(chr(9))
        return int(du[0])

    return 0


def getHumanityDiskUsage(disk_usage):
    unit = 0
    while disk_usage > 1024:
        unit += 1
        disk_usage /= 1024

    sdu = Decimal(disk_usage).quantize(Decimal('0.01'), decimal.ROUND_HALF_UP)

    sunit = {
        0: 'B',
        1: 'KB',
        2: 'MB',
        3: 'GB',
        4: 'TB',
        5: 'PB',
        6: 'EB'
    }[unit]

    return f'{sdu} {sunit}'
