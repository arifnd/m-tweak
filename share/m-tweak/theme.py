#!/usr/bin/python
#
#	M Tweak Theme Class
#	Las Update	: 2013/10/06
#
#	Powered by BlankOn Linux Developer 2013
#
#	Developed by:
#	* Ari Effendi <zerosix06@gmail.com>
#	*
#	Some code based on:
#	* http://w.blankon.in/v_
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

import ConfigParser
import os

from gi.repository import GObject

class Theme(GObject.GObject):
	name = GObject.property(type=str)
	creator = GObject.property(type=str)
	version = GObject.property(type=str)
	folder = GObject.property(type=str)
	active = GObject.property(type=str)

	def __init__(self):
		GObject.GObject.__init__(self)
		self.config = ConfigParser.ConfigParser()

	def theme_list(self):
		theme = []

		for info in os.listdir('/usr/share/m-tweak/info/'):
			#if info.endswith('.cfg'):
			self.config.read(os.path.join('/usr/share/m-tweak/info/',info))
			name = self.config.get('theme', 'name')
			creator = self.config.get('theme', 'creator')
			version = self.config.get('theme', 'version')
			active = self.config.get('manokwari', 'active')
			theme.append(tuple((name, creator, version, info, active)))

		return theme

	def theme_change(self, theme):
		try:
			
			return True
		except:
			return False

	def __repr__(self):
		return "%s" % (self.get_property("folder"))
