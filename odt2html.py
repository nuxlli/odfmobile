#!/usr/bin/env python

import odf2html
import os

class odt2html(odf2html.odf2html):

  xml_files = ('content.xml','meta.xml','styles.xml','settings.xml')
  xslt_file = 'odt.xslt'

if __name__ == "__main__":
  result = odt2html('./InformationForAuthors.odt').run()
  #os.system('firefox %s' % result[0])
