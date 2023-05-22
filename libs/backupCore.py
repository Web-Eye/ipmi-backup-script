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

from libs.common.BufferingSMTPHandler import BufferingSMTPHandler


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

        _mail_handler = BufferingSMTPHandler('localhost', self._config['mail']['fromaddr'], [self._config['mail']['toaddr']], 'ipmi backup', 500)
        _mail_handler.setLevel(logging.WARNING)
        self._logger.addHandler(_mail_handler)

    def run(self):
        self._logger.info('starting backup core...')
