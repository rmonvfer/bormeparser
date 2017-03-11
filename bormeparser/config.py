#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# bormeparser.config.py -
# Copyright (C) 2017 Pablo Castellano <pablo@anche.no>
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

import os.path

try:
    # Python 3
    import configparser
    config = configparser.ConfigParser()
except ImportError:
    import ConfigParser
    config = ConfigParser.ConfigParser()

CONFIG_FILE = os.path.expanduser("~/.bormecfg")
DEFAULTS = {
    'borme_root': os.path.expanduser("~/.bormes")
}

if os.path.isfile(CONFIG_FILE):
    config.read(CONFIG_FILE)
    CONFIG = dict(config["general"])
else:
    CONFIG = DEFAULTS

