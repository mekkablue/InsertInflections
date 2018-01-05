# encoding: utf-8

import objc
from GlyphsApp import *
from GlyphsApp.plugins import *

class InsertInflections(FilterWithoutDialog):
	
	def settings(self):
		self.menuName = Glyphs.localize({
			'en': u'Insert Inflections',
			'de': u'Inflektionspunkte einfügen'
		})
		self.keyboardShortcut = None # With Cmd+Shift

	def filter(self, thisLayer, inEditView, customParameters):
		for ip in range( len( thisLayer.paths )):
			thisPath = thisLayer.paths[ip]
			numberOfNodes = len( thisPath.nodes )

			for i in range(numberOfNodes-1, -1, -1):
				node = thisPath.nodes[i]
				if node.type == CURVE:
					nl = [ thisPath.nodes[ (x+numberOfNodes) % numberOfNodes ] for x in range( i-3, i+1 ) ]
					inflections = self.computeInflection( nl[0], nl[1], nl[2], nl[3] )
					if len(inflections) == 1:
						inflectionTime = inflections[0]
						thisPath.insertNodeWithPathTime_( i + inflectionTime )
	
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
		
	def computeInflection( self, p1, p2, p3, p4 ):
		"""
		For a given curve p1, p2, p3, p4,
		t for the first inflection point is calculated and returned.
		"""
		try:
			Result = []
			ax = p2.x - p1.x
			ay = p2.y - p1.y
			bx = p3.x - p2.x - ax
			by = p3.y - p2.y - ay
			cx = p4.x - p3.x - ax - bx - bx
			cy = p4.y - p3.y - ay - by - by
			c0 = ( ax * by ) - ( ay * bx )
			c1 = ( ax * cy ) - ( ay * cx )
			c2 = ( bx * cy ) - ( by * cx )
	
			if abs(c2) > 0.00001:
				discr = ( c1 ** 2 ) - ( 4 * c0 * c2)
				c2 *= 2
				if abs(discr) < 0.000001:
					root = -c1 / c2
					if (root > 0.001) and (root < 0.99):
						Result.append(root)
				elif discr > 0:
					discr = discr ** 0.5
					root = ( -c1 - discr ) / c2
					if (root > 0.001) and (root < 0.99):
						Result.append(root)
			
					root = ( -c1 + discr ) / c2
					if (root > 0.001) and (root < 0.99):
						Result.append(root)
			elif c1 != 0.0:
				root = - c0 / c1
				if (root > 0.001) and (root < 0.99):
					Result.append(root)

			return Result
		except Exception as e:
			print "computeInflection: %s" % str(e)
			import traceback
			print traceback.format_exc()
	
	