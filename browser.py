import gtkmozembed
import osso
import os
import re
import hildon

from threading import RLock

version_string = "0.0.1"
osso_context = osso.Context("org.maemo.garage.odfmobile.browser", version_string, False)

# If MOZILLA_FIVE_HOME environment variable isn't set, set it and 
# restart ourself. This is a hack to get the task bar icon to work, because
# if we start another script/program the default maemo icon will be shown.
os.environ["MOZILLA_FIVE_HOME"] = "/usr/lib/microb-engine"
os.environ["MOZILLA_HOME"] = "/usr/lib/microb-engine"
os.environ["LD_LIBRARY_PATH"] = "/usr/lib/microb-engine"
#os.execl(sys.argv[0], "oreader", "--mozenv-set")

class Browser(gtkmozembed.MozEmbed):
  browserlock = RLock()
  loading     = False
  app         = None
  msgs        = {}

  def __init__(self, app, profile_path):
    gtkmozembed.push_startup()
    gtkmozembed.set_profile_path(profile_path, "odfmobile_browser_profile")

    gtkmozembed.MozEmbed.__init__(self)
    self.app = app

    # Conect events
    self.connect("open-uri", self.filter_browser_url)
    self.connect("net-start", self.browser_start)
    self.connect("net-state", self.browser_state)
    self.connect("net-stop", self.browser_stop)
    self.set_size_request(24, 0)

  def run(self):
    gtkmozembed.pop_startup()

  def open_url(self, url):
    self.browserlock.acquire()
    try:
      if self.loading:
        self.stop_load()
      self.load_url(url)
    finally:
      self.browserlock.release()

  def open_local_url(self, file_name):
    self.open_url(self.get_local_url() + file_name)

  def get_local_url(self):
    return "file://" + self.app.get_app_dir() + "/data/"

  # browser callback
  def browser_start(self, browser):
    self.browserlock.acquire()
    try:
      self.loading = True
    finally:
      self.browserlock.release()

  # browser callback
  def browser_state(self, browser, flags, status):
    print "got browser_state: " + flags

  # browser callback
  def browser_stop(self, browser):
    self.browserlock.acquire()
    try:
      self.loading = False
    finally:
      self.browserlock.release()

	## Send a message to the javascript running in the browser
  def send_command(self, command, arg):
    command = "javascript:" + command + "('" + str(arg) + "')"
    self.open_url(command)

  ## callback from browser when it tries to open a URL. This is used 
  ## to send stuff back from browser/Javascript to python using 
  ## URLS like http://cmd/play#4
  def filter_browser_url(self, widget, url):
    print "Abrindo %s" % url
    
    if (url.find(self.get_local_url()) == 0) \
    or (url.find("file:") == 0) \
    or (url.find("about:") == 0) \
    or (url.find("javascript:") == 0):
      return False
    
    if url.find("http://cmd/") == 0:
      match = re.compile('http://cmd/(.*?)/(.*)').search(url)
      if match != None:
        if match.group(1) == 'msg':
          options = match.group(2).split('/')
          if ((options[0] == 'add') and (self.msgs.get(options[1]) == None)):
            self.msgs[options[1]] = hildon.hildon_banner_show_animation(self.app.window, None, " Wait... ")
          elif (options[0] == 'remove' and (self.msgs.get(options[1]) != None)):
            self.msgs[options[1]].destroy()
            del(self.msgs[options[1]])
      
      return True

    print "launching external browser: " + url
    osso_rpc = osso.Rpc(osso_context)
    osso_rpc.rpc_run("com.nokia.osso_browser", "/com/nokia/osso_browser", 
      "com.nokia.osso_browser", "open_new_window", (url, ()))
    return True
