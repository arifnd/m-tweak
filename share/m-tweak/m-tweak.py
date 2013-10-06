#!/usr/bin/python
#
#	M Tweak - Manokwari Theme Manager
#	Version		: 0.1
#	Las Update	: 2013/09/21
#
#	Powered by BlankOn Linux Developer 2013
#
#	Developed by:
#	* Ari Effendi <zerosix06@gmail.com>
#	*
#
#	Some code based on:
#	* http://w.blankon.in/7Z
#	* http://w.blankon.in/8Z
#	* http://w.blankon.in/j_
#	* http://w.blankon.in/s_
#	* http://w.blankon.in/t_
#
#  M Tweak is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  M Tweak is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with M Tweak; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

import gettext
import os
import sys

from gi.repository import Gtk
from gi.repository import GObject

from theme import Theme

#if os.geteuid() != 0:
#	print "You not running as root!"
#	sys.exit(1)

app_name = "m-tweak"
app_version = "0.1"
app_developer = '''Ari Effendi <zerosix06@gmail.com>

'''

t = gettext.translation(app_name, '/usr/share/locale')
_ = t.ugettext

class MTweak(Gtk.Window):

	def __init__(self, *args, **kwargs):

		Gtk.Window.__init__(self, *args, **kwargs)
		self.set_border_width(10)
		self.set_size_request(400, 400)
		self.set_position(Gtk.WindowPosition.CENTER)
		self.set_title(_("Manokwari Theme Manager"))
		self.icon = Gtk.IconTheme.get_default().load_icon(app_name, 64, 0)
		self.set_icon(self.icon)
		self.connect("destroy", Gtk.main_quit)
		self.create_widgets()
		self.get_theme()
		self.show_all()

	def create_widgets(self):
		self.treestore = Gtk.TreeStore(Theme.__gtype__)
		self.treeview = Gtk.TreeView()
		self.treeview.set_model(self.treestore)

		cell = Gtk.CellRendererText()
		column = Gtk.TreeViewColumn(_("Theme Name"))
		column.pack_start(cell, True)
		column.set_cell_data_func(cell, self.get_name)
		self.treeview.append_column(column)

		cell = Gtk.CellRendererText()
		column = Gtk.TreeViewColumn(_("Creator"))
		column.pack_start(cell, True)
		column.set_cell_data_func(cell, self.get_creator)
		self.treeview.append_column(column)

		cell = Gtk.CellRendererText()
		column = Gtk.TreeViewColumn(_("Version"))
		column.pack_start(cell, True)
		column.set_cell_data_func(cell, self.get_version)
		self.treeview.append_column(column)

		btnApply = Gtk.Button(_("Apply Theme"))
		btnApply.connect("clicked", self.dialog_confirm)

		btnInstall = Gtk.Button(_("Install New Theme"))
		btnInstall.connect("clicked", self.theme_browse)

		btnClose = Gtk.Button(_("Close"))
		btnClose.connect("clicked", Gtk.main_quit)

		buttonBox = Gtk.HButtonBox()
		buttonBox.set_spacing(15)
		buttonBox.add(btnApply)
		buttonBox.add(btnInstall)
		buttonBox.add(btnClose)

		themeBox = Gtk.VBox()
		themeBox.pack_start(self.treeview, True, True, 0)
		themeBox.pack_start(buttonBox, False, False, 5)

		appIcon = Gtk.Image()
		appIcon.set_from_pixbuf(self.icon)
		appName = Gtk.Label(_("Manokwari Theme Manager")+" "+app_version)
		appDesc = Gtk.Label(_("This application can manage, add, remove Manokwari theme"))
		appCopy = Gtk.Label("(c) 2013 Blankon Linux")
		appUrl = Gtk.Label()
		appUrl.set_markup("<a href='http://www.blankonlinux.or.id'>blankonlinux.or.id</a>")
		appDev = Gtk.Label(_("Developer"))
		appPerson = Gtk.Label(app_developer)

		aboutBox = Gtk.VBox()
		aboutBox.pack_start(appIcon, False, False, 5)
		aboutBox.pack_start(appName, False, False, 0)
		aboutBox.pack_start(appDesc, False, False, 0)
		aboutBox.pack_start(appCopy, False, False, 0)
		aboutBox.pack_start(appUrl, False, False, 0)
		aboutBox.pack_start(appDev, False, False, 5)
		aboutBox.pack_start(appPerson, False, False, 5)

		tab = Gtk.Notebook()
		label = Gtk.Label(_("Themes"))
		tab.append_page(themeBox, label)
		label = Gtk.Label(_("About"))
		tab.append_page(aboutBox, label)

		self.add(tab)

	def get_name(self, column, cell, model, iter, data):
		cell.set_property('text', self.treestore.get_value(iter, 0).name)

	def get_creator(self, column, cell, model, iter, data):
		cell.set_property('text', self.treestore.get_value(iter, 0).creator)

	def get_version(self, column, cell, model, iter, data):
		cell.set_property('text', self.treestore.get_value(iter, 0).version)
		
	def get_folder(self, column, cell, model, iter, data):
		cell.set_property('text', self.treestore.get_value(iter, 0).folder)

	def get_active(self, column, cell, model, iter, data):
		cell.set_property('text', self.treestore.get_value(iter, 0).active)

	def get_theme(self):
		t = Theme()
		for name, creator, version, folder, active in t.theme_list():
			i = Theme()
			i.name = name
			i.creator = creator
			i.version = version
			i.folder = folder
			i.active = active
			self.treestore.append(None, (i,))

	def retrieve_element(self):
		model, treeiter = self.treeview.get_selection().get_selected()
		return model[treeiter][0]

	def theme_browse(self, widget):
		dialog = Gtk.FileChooserDialog(_("Please choose a file"), self,
			Gtk.FileChooserAction.OPEN,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			 Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

		self.theme_filter(dialog)

		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			print "Open clicked"
			print "File selected: " + dialog.get_filename()
		elif response == Gtk.ResponseType.CANCEL:
			print "Cancel clicked"

		dialog.destroy()

	def theme_filter(self, dialog):
		filter_any = Gtk.FileFilter()
		filter_any.set_name(_("Theme files"))
		filter_any.add_pattern("*.zip")
		dialog.add_filter(filter_any)

	def dialog_confirm(self, widget):
		dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.QUESTION,
			Gtk.ButtonsType.YES_NO, _("Are you want to change theme"))
		dialog.format_secondary_text(
			_("After you press OK button theme will change."))
		response = dialog.run()
		if response == Gtk.ResponseType.YES:
			print self.retrieve_element()
		elif response == Gtk.ResponseType.NO:
			print "NO respone"

		dialog.destroy()

if __name__ == "__main__":
	GObject.type_register(Theme)
	MTweak()
	Gtk.main()
