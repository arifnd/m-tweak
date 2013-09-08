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

class Theme (GObject.GObject):
	name = GObject.property(type=str)
	creator = GObject.property(type=str)
	version = GObject.property(type=str)

	def __init__(self):
		GObject.GObject.__init__(self)

	def __repr__(self):
		return "%s, %s" % (self.get_property("name"), self.get_property("version"))

class MTweak (Gtk.Window):

	def __init__(self, *args, **kwargs):
		Gtk.Window.__init__(self, *args, **kwargs)
		self.set_title("M-Tweak")
		self.set_size_request(400, 400)
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

		vbox = Gtk.VBox()
		self.add(vbox)
		vbox.pack_start(self.treeview, True, True, 0)

		btnApply = Gtk.Button("Apply Theme")
		btnApply.connect("clicked", self.retrieve_element)
		vbox.pack_start(btnApply, False, False, 5)

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

if __name__ == "__main__":
	GObject.type_register(Theme)
	MTweak()
	Gtk.main()
