#!/usr/bin/python
#
#	m-tweak.py
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

from gi.repository import Gtk
from gi.repository import GObject

class Theme(GObject.GObject):
	name = GObject.property(type=str)
	creator = GObject.property(type=str)
	version = GObject.property(type=str)

	def __init__(self):
		GObject.GObject.__init__(self)

	def __repr__(self):
		return "%s, %s" % (self.get_property("name"), self.get_property("version"))

class MTweak(Gtk.Window):

	def __init__(self, *args, **kwargs):
		Gtk.Window.__init__(self, *args, **kwargs)
		self.set_border_width(10)
		self.set_size_request(400, 400)
		#self.set_position(GTK_WIN_POS_CENTER)
		self.set_title("M-Tweak")
		self.connect("destroy", Gtk.main_quit)
		self.create_widgets()
		self.get_theme()
		self.show_all()

	def create_widgets(self):
		self.treestore = Gtk.TreeStore(Theme.__gtype__)
		self.treeview = Gtk.TreeView()
		self.treeview.set_model(self.treestore)

		cell = Gtk.CellRendererText()
		column = Gtk.TreeViewColumn("Theme Name")
		column.pack_start(cell, True)
		column.set_cell_data_func(cell, self.get_name)
		self.treeview.append_column(column)

		cell = Gtk.CellRendererText()
		column = Gtk.TreeViewColumn("Creator")
		column.pack_start(cell, True)
		column.set_cell_data_func(cell, self.get_creator)
		self.treeview.append_column(column)

		cell = Gtk.CellRendererText()
		column = Gtk.TreeViewColumn("Version")
		column.pack_start(cell, True)
		column.set_cell_data_func(cell, self.get_version)
		self.treeview.append_column(column)

		btnApply = Gtk.Button("Apply Theme")
		btnApply.connect("clicked", self.dialog_confirm)
		#btnApply.connect("clicked", self.retrieve_element)

		btnInstall = Gtk.Button("Install New Theme")
		btnInstall.connect("clicked", self.theme_browse)

		btnClose = Gtk.Button("Close")
		btnClose.connect("clicked", Gtk.main_quit)

		buttonBox = Gtk.HButtonBox()
		buttonBox.set_spacing(15)
		buttonBox.add(btnApply)
		buttonBox.add(btnInstall)
		buttonBox.add(btnClose)

		themeBox = Gtk.VBox()
		themeBox.pack_start(self.treeview, True, True, 0)
		themeBox.pack_start(buttonBox, False, False, 5)

		aboutBox = Gtk.VBox()

		tab = Gtk.Notebook()
		label = Gtk.Label("Themes")
		tab.append_page(themeBox, label)
		label = Gtk.Label("About")
		tab.append_page(aboutBox, label)

		self.add(tab)

	def get_name(self, column, cell, model, iter, data):
		cell.set_property('text', self.treestore.get_value(iter, 0).name)

	def get_creator(self, column, cell, model, iter, data):
		cell.set_property('text', self.treestore.get_value(iter, 0).creator)

	def get_version(self, column, cell, model, iter, data):
		cell.set_property('text', self.treestore.get_value(iter, 0).version)

	def get_theme(self):
		for name, creator, version in [("Goolge", "Remon", "1.0"), ("Embun", "Dono", "0.1")]:
			t = Theme()
			t.name = name
			t.creator = creator
			t.version = version
			self.treestore.append(None, (t,))

	def retrieve_element(self, widget):
		model, treeiter = self.treeview.get_selection().get_selected()
		if treeiter:
			print "You selected", model[treeiter][0]

	def theme_browse(self, widget):
		dialog = Gtk.FileChooserDialog("Please choose a file", self,
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
		filter_any.set_name("Theme files")
		filter_any.add_pattern("*.zip")
		dialog.add_filter(filter_any)

	def dialog_confirm(self, widget):
		dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.QUESTION,
			Gtk.ButtonsType.YES_NO, "Are you want to change theme")
		dialog.format_secondary_text(
			"After you press OK button theme wil change.")
		response = dialog.run()
		if response == Gtk.ResponseType.YES:
			print "QUESTION dialog closed by clicking YES button"
		elif response == Gtk.ResponseType.NO:
			print "QUESTION dialog closed by clicking NO button"

		dialog.destroy()

if __name__ == "__main__":
	GObject.type_register(Theme)
	MTweak()
	Gtk.main()
