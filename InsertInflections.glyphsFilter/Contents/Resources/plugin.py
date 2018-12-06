# encoding: utf-8

import objc
from GlyphsApp import *
from GlyphsApp.plugins import *

class InsertInflections(FilterWithoutDialog):
	
	def settings(self):
		self.menuName = Glyphs.localize({
			'en': u'Insert Inflections',
			'de': u'Inflektionspunkte einfügen',
			'fr': u'Ajouter les points d’inflexion',
			'es': u'Agregar puntos de inflexión',
			'zh': u'🎢曲线拐点',
		})
		self.keyboardShortcut = None # With Cmd+Shift

	def filter(self, thisLayer, inEditView, customParameters):
		thisLayer.addInflectionPoints()
		
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
