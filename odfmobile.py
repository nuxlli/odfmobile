#!/usr/bin/python

# Standart lib
import sys, os, osso, hildon, gtk, gobject
import gtkmozembed

# Working it thereding
from threading import Thread
gtk.gdk.threads_init()

# Project libs
from odt2html import *
from browser import *

version_string = "0.0.1"
osso_context = osso.Context("org.maemo.garage.odfmobile", version_string, False)

class oReader(hildon.Program):
  document  = None

  def __init__(self):
    hildon.Program.__init__(self)

    self.home_dir = os.path.abspath(os.path.expanduser('~/.odfmobile'))
    if not os.path.exists(self.home_dir):
      os.makedirs(self.home_dir)
    
    self.window = hildon.Window()
    self.window_in_fullscreen = False
    self.window.connect("destroy", self.close)
    self.window.connect("key-press-event", self.on_key_press)
    self.window.connect("window-state-event", self.on_window_state_change)

    # Browser
    self.browser = Browser(self, self.home_dir)
    self.browser.open_local_url('index.html')
    self.window.add(self.browser)

    # Menu
    self.menu = gtk.Menu()

    item = gtk.ImageMenuItem(stock_id="gtk-open")
    item.connect("activate", self.open_file)
    self.menu.append(item)

    item = gtk.ImageMenuItem(stock_id="gtk-quit")
    item.connect("activate", self.close)
    self.menu.append(item)

    self.window.set_menu(self.menu)

    # File dialog
    # obs: hildon.FileChooserDialog not implement filters
    self.dlg = hildon.FileChooserDialog(self.window, gtk.FILE_CHOOSER_ACTION_OPEN);
   
    # TODO: Adicionar filtro de tipos de arquivo, para isso e necessario construi
    # um novo FileChooserDialog para hildon pois o padrao nao implementa esta funcinalidade
    #self.dlg = gtk.FileChooserDialog("Filename", self.window, 
    #  gtk.FILE_CHOOSER_ACTION_OPEN, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, 
    #  gtk.STOCK_OPEN, gtk.RESPONSE_OK))
    #self.dlg.set_default_response(gtk.RESPONSE_OK)

    # Filter for files
    #self.filter = gtk.FileFilter()
    #self.filter.set_name("ODF files")
    #self.filter.add_pattern("*.odt")
    #self.filter.add_pattern("*.odp")
    #self.filter.add_pattern("*.ods")
    #self.dlg.add_filter(self.filter)

  # Change state windows, alternate fullscreen and not fullscreen
  def on_window_state_change(self, widget, event, *args):
    if event.new_window_state & gtk.gdk.WINDOW_STATE_FULLSCREEN:
      self.window_in_fullscreen = True
    else:
      self.window_in_fullscreen = False

  # Working key press events
  def on_key_press(self, widget, event, *args):
    if event.keyval == gtk.keysyms.F6:
      if self.window_in_fullscreen:
        self.window.unfullscreen ()
      else:
        self.window.fullscreen ()
    # Zoom
    elif event.keyval == gtk.keysyms.F8 or event.keyval == gtk.keysyms.F7: # or self.document['opened']:
      if event.keyval == gtk.keysyms.F8:
        self.browser.open_url("javascript:decreaseFont()")
      else:
        self.browser.open_url("javascript:increaseFont()")

  # Open files dialog
  def open_file(self, target):

    response = self.dlg.run()
    self.dlg.hide()

    if response == gtk.RESPONSE_OK:
      self.close_document()
      self.document = {
        "document": self.dlg.get_filename(),
        "processed": 0,
        "opened": 0,
        "paths": '',
        "title": '',
      }
      self.open_document()

  def finalize_open(self, odf):
    # Wait process file
    banner = hildon.hildon_banner_show_animation(self.window, None, " Opening... ")
    while odf.processed == 0: continue
    banner.destroy()

    gobject.idle_add(self.open_url, 'file://%s' % odf.result[0])
    self.document['paths'] = odf.result

    self.close_button = gtk.ImageMenuItem(stock_id="gtk-close")
    self.close_button.connect("activate", self.close_document)
    self.menu.insert(self.close_button, 1)
    self.menu.show_all()
    self.document['opened'] = self.document['processed'] = 1

  def open_url(self, url):
    self.browser.open_url(url)

  def open_document(self, target = None):
    if self.document['opened'] == 0:
      odf = odt2html(self.document['document'])
      #odf.run()
      #self.finalize_open(odf)

      Thread(target=odf.run).start()
      Thread(target=self.finalize_open, args=(odf,)).start()

  def alert(self, target = None):
      self.browser.send_command('alert', 'Abrindo!!!');

  def close_document(self, target = None):
    if self.document != None:
      if len(self.document['paths']) > 0:
        os.system('rm -Rf %s' % self.document['paths'][1])
      self.browser.open_local_url('index.html')
      self.document = None

      # Remove close menu
      self.menu.remove(self.close_button)
      self.menu.show_all()

  def get_app_dir(self):
    path = os.path.abspath(os.path.dirname(sys.argv[0]))
    if os.path.exists(path + "/odfmobile.py"):
      return path
    else:
      return "/usr/share/odfmobile"

  def show_settings_dialog(self):
    pass

  def run(self):
    self.window.show_all()
    gtk.main()
    self.browser.run()

  def close(self, target):
    self.close_document()
    self.dlg.destroy()
    gtk.gdk.threads_leave()
    gtk.main_quit()

if __name__ == "__main__":
  oReader().run()
