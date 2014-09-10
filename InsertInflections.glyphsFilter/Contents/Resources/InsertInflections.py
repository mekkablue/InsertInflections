#!/usr/bin/env python
# encoding: utf-8

import objc
from Foundation import *
from AppKit import *
import sys, os, re

MainBundle = NSBundle.mainBundle()
path = MainBundle.bundlePath() + "/Contents/Scripts"
if not path in sys.path:
	sys.path.append( path )

import GlyphsApp

GlyphsFilterProtocol = objc.protocolNamed( "GlyphsFilter" )

class GlyphsFilterInsertInflections ( NSObject, GlyphsFilterProtocol ):
	
	def init( self ):
		"""
		Do all initializing here.
		"""
		return self
	
	def interfaceVersion( self ):
		"""
		Distinguishes the API version the plugin was built for. 
		Return 1.
		"""
		try:
			return 1
		except Exception as e:
			self.logToConsole( "interfaceVersion: %s" % str(e) )
	
	def setController_( self, Controller ):
		"""
		Do not touch this.
		"""
		try:
			self._controller = Controller
		except Exception as e:
			self.logToConsole( "setController_: %s" % str(e) )
	
	def controller( self ):
		"""
		Do not touch this.
		"""
		try:
			return self._controller
		except Exception as e:
			self.logToConsole( "controller: %s" % str(e) )
		
	def setup( self ):
		"""
		Do not touch this.
		"""
		try:
			return None
		except Exception as e:
			self.logToConsole( "setup: %s" % str(e) )
	
	def title( self ):
		"""
		This is the human-readable name as it appears in the menu.
		"""
		return "Insert Inflections"
	
	def keyEquivalent( self ):
		""" 
		The key together with Cmd+Shift will be the shortcut for the filter.
		Return None if you do not want to set a shortcut.
		Users can set their own shortcuts in System Prefs.
		"""
		try:
			return None
		except Exception as e:
			self.logToConsole( "keyEquivalent: %s" % str(e) )
	
	def processLayer( self, thisLayer ):
		"""
		Each selected layer is processed here.
		"""
		try:
			for ip in range( len( thisLayer.paths )):
				thisPath = thisLayer.paths[ip]
				numberOfNodes = len( thisPath.nodes )

				for i in range(numberOfNodes-1, -1, -1):
					node = thisPath.nodes[i]
					if node.type == 35: #CURVE
						nl = [ thisPath.nodes[ (x+numberOfNodes)%numberOfNodes ] for x in range( i-3, i+1 ) ]
						inflections = self.computeInflection( nl[0], nl[1], nl[2], nl[3] )
						if len(inflections) == 1:
							inflectionTime = inflections[0]
							thisPath.insertNodeWithPathTime_( i + inflectionTime )
							
			return True
		except Exception as e:
			self.logToConsole( "processLayer: %s" % str(e) )
			return False

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
			self.logToConsole( "computeInflection: %s" % str(e) )
	
	def runFilterWithLayers_error_(self, Layers, Error):
		"""
		Invoked when user triggers the filter through the Filter menu
		and more than one layer is selected.
		"""
		try:
			for k in range(len(Layers)):
				Layer = Layers[k]
				Layer.clearSelection()
				self.processLayer( Layer )
		except Exception as e:
			self.logToConsole( "runFilterWithLayers_error_: %s" % str(e) )
			
	def runFilterWithLayer_error_(self, Layer, Error):
		"""
		Invoked when user triggers the filter through the Filter menu
		and only one layer is selected.
		"""
		try:
			return self.processLayer( Layer )
		except Exception as e:
			self.logToConsole( "runFilterWithLayer_error_: %s" % str(e) )
	
	def processFont_withArguments_( self, Font, Arguments ):
		"""
		Invoked when called as Custom Parameter in an instance at export.
		The Arguments come from the custom parameter in the instance settings. 
		The first item in Arguments is the class-name. After that, it depends on the filter.
		"""
		try:
			# set glyphList to all glyphs
			glyphList = Font.glyphs
			
			# Override defaults with actual values from custom parameter:
			if len( Arguments ) > 1:
				
				# change glyphList to include or exclude glyphs
				if "exclude:" in Arguments[-1]:
					excludeList = [ n.strip() for n in Arguments.pop(-1).replace("exclude:","").strip().split(",") ]
					glyphList = [ g for g in glyphList if not g.name in excludeList ]
				elif "include:" in Arguments[-1]:
					includeList = [ n.strip() for n in Arguments.pop(-1).replace("include:","").strip().split(",") ]
					glyphList = [ Font.glyphs[n] for n in includeList ]
			
			FontMasterId = Font.fontMasterAtIndex_(0).id
			for thisGlyph in glyphList:
				Layer = thisGlyph.layerForKey_( FontMasterId )
				self.processLayer( Layer )
		except Exception as e:
			self.logToConsole( "processFont_withArguments_: %s" % str(e) )
	
	def logToConsole( self, message ):
		"""
		The variable 'message' will be passed to Console.app.
		Use self.logToConsole( "bla bla" ) for debugging.
		"""
		myLog = "Filter %s:\n%s" % ( self.title(), message )
		NSLog( myLog )
