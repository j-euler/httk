# 
#    The high-throughput toolkit (httk)
#    Copyright (C) 2012-2015 Rickard Armiento
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Reads the file httk.cfg in the root of the httk tree and the user's .httk.cfg.
If none of them is found it uses the httk.cfg.default.
"""

import sys
import os.path
import inspect

try:
    # Python 2
    import ConfigParser as configparser
except ImportError:
    # Python 3
    import configparser

_realpath = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))

config = configparser.ConfigParser()
config_files = []

internal_cfgpathstr = os.path.join(_realpath, 'httk.cfg')
config.read([internal_cfgpathstr])

httk_root_cfg = config.get('general','httk_root')
httk_root = os.path.join(_realpath,httk_root_cfg)

global_cfgpathstr = os.path.join(httk_root, 'httk.cfg')
local_cfgpathstr = os.path.expanduser('~/.httk.cfg')

config.read([global_cfgpathstr, local_cfgpathstr])
    