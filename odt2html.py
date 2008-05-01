#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
# ODF Mobile
#
# License: GPL
# Copyright (c) 2008 ODF Mobile team
#
#
# Last Modified: 2008-05-1 12:24
#
# License Information:
#
# This file is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# at your option.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
################################################################################

import odf2html
import os

class odt2html(odf2html.odf2html):

  xml_files = ('content.xml','meta.xml','styles.xml','settings.xml')
  xslt_file = 'odt.xslt'

if __name__ == "__main__":
  result = odt2html('./InformationForAuthors.odt').run()
  #os.system('firefox %s' % result[0])
