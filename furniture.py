import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from pypak import *
pm=PyPak("database")

    
class Handler:
    def onDestroy(self, *args):
        Gtk.main_quit()


builder = Gtk.Builder()
builder.add_from_file("ui.ui")
builder.connect_signals(Handler())

packagelist=builder.get_object('liststore1')

for package in pm.search("",False):
    packagelist.append([package.title, package.description, package.id, package.version, package.repository, package.runtime, package.size['installed'], package.size['download'], package.branch])

window = builder.get_object("window1")
window.show_all()

Gtk.main()


