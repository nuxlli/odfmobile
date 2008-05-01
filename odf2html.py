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

import os
import sys
import re
import zipfile
import md5

class odf2html:
  """
    Process of the standard ODF files and turn them into html using XSLT.
  """

  processed = 0
  result    = ()

  def __init__(self, filepath, cached = 0):
    self.file_path  = os.path.abspath(os.path.expanduser(filepath))
    self.home_cache = os.path.abspath(os.path.expanduser('~/.oreader'))

    self.xslt_file      = '%s/%s'  % (os.path.dirname(__file__), self.xslt_file)
    self.cache_path     = '%s/%s/' % (self.home_cache, md5.new(self.file_path).hexdigest())
    self.cache_merge    = self.cache_path + 'merge.xml'
    self.cache_final    = self.cache_path + 'final.html'
    self.cache_pictures = self.cache_path + '/Pictures/'

    self.cached = cached

  # TODO: Adicionar tratamento de cache verificando a data em que a pasta foi 
  #       criada, e data de modificacao do arquivo para tratar o cache corretamente
  def run(self):
    # Clean cache and create folder cache
    os.system('rm -R %s 2>/dev/null' % self.cache_path)
    os.makedirs(self.cache_pictures)

    merge_content = ''
    merge_content += "<?xml version='1.0' encoding='UTF-8'?>\n"
    merge_content += "<office:document xmlns:office='urn:oasis:names:tc:opendocument:xmlns:office:1.0'>\n"

    # Read files in odf file (zip format)
    re_xml = re.compile(r'^(<\?xml version=[^\n]*?\n)')
    zip    = zipfile.ZipFile(self.file_path)
    for i in self.xml_files:
      merge_content += re_xml.sub("", zip.read(i))

    merge_content += "</office:document>\n"

    # Create merge file
    fm = file(self.cache_merge,"w")
    fm.write(merge_content)
    fm.close()
    del merge_content

    # Extract Pictures
    imgs = [elem for elem in zip.namelist() if elem.find("Pictures/") == 0]
    for img in imgs:
      fh = file(self.cache_path + img, "w")
      fh.write(zip.read(img))
      fh.close()

    # close file
    zip.close()
    del zip

    os.system('xsltproc -o %s %s %s' % (self.cache_final, self.xslt_file, self.cache_merge))

    self.processed = 1
    self.result    = (self.cache_final, self.cache_path)
