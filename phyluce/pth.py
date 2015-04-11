#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(c) 2015 Brant Faircloth || http://faircloth-lab.org/
All rights reserved.

This code is distributed under a 3-clause BSD license. Please see
LICENSE.txt for more information.

Created on 11 April 2015 16:57 CDT (-0500)
"""

import os
import sys
import ConfigParser

def get_user_path(program, binary):
    config = ConfigParser.ConfigParser()
    config.read([os.path.join(sys.prefix, 'config/phyluce.conf'), os.path.expanduser('~/.phyluce.conf')])
    # ensure program is in list
    pth = config.get(program, binary)
    # expand path as necessary
    expand_pth = os.path.abspath(os.path.expanduser(os.path.expandvars(pth)))
    return expand_pth


def get_user_param(section, param):
    config = ConfigParser.ConfigParser()
    config.read([os.path.join(sys.prefix, 'config/phyluce.conf'), os.path.expanduser('~/.phyluce.conf')])
    return config.get(section, param)