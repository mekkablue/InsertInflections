# encoding: utf-8
from __future__ import division, print_function, unicode_literals

###########################################################################################################
#
#
#	Filter without dialog Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Filter%20without%20Dialog
#
#
###########################################################################################################

import objc
from GlyphsApp import Glyphs
from GlyphsApp.plugins import FilterWithoutDialog

class InsertInflections(FilterWithoutDialog):
	
	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({
			'en': u'Insert Inflections',
			'de': u'Inflektionspunkte einfügen',
			'fr': u'Ajouter les points d’inflexion',
			'es': u'Agregar puntos de inflexión',
			'zh': u'🎢曲线拐点',
		})
		self.keyboardShortcut = None # With Cmd+Shift

	@objc.python_method
	def filter(self, thisLayer, inEditView, customParameters):
		thisLayer.addInflectionPoints()
		
	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
