# encoding: utf-8
from __future__ import division, print_function, unicode_literals

###########################################################################################################
#
#
#	Reporter Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Reporter
#
#
###########################################################################################################

import objc
from GlyphsApp import *
from GlyphsApp.plugins import *
from math import hypot

class ShowDistanceBetweenTwoPoints(ReporterPlugin):

	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({
			'en': 'Distance between Two Points',
			'es': 'distancia entre dos puntos',
			'de': 'Abstand zwischen zwei Punkten', 
			'fr': 'distance entre deux points',
			'pt': 'distância entre dois pontos',
		})
	
	@objc.python_method
	def roundDotForPoint( self, thisPoint, markerWidth ):
		"""
		Returns a circle with thisRadius around thisPoint.
		"""
		myRect = NSRect( ( thisPoint.x - markerWidth * 0.5, thisPoint.y - markerWidth * 0.5 ), ( markerWidth, markerWidth ) )
		return NSBezierPath.bezierPathWithOvalInRect_(myRect)

	@objc.python_method
	def drawRoundedRectangleForStringAtPosition(self, thisString, center, fontsize):
		scaledSize = fontsize / self.getScale()
		width = len(thisString) * scaledSize * 0.7
		rim = scaledSize * 0.3

		panel = NSRect()
		panel.origin = NSPoint( center.x-width/2, center.y-scaledSize/2-rim )
		panel.size = NSSize( width, scaledSize + rim*2 )
		
		NSBezierPath.bezierPathWithRoundedRect_xRadius_yRadius_( panel, scaledSize*0.5, scaledSize*0.5 ).fill()
		
	@objc.python_method
	def foreground(self, layer):
		currentSelection = layer.selection
		if currentSelection and len(currentSelection) == 2:
			node1 = currentSelection[0]
			node2 = currentSelection[1]
			if type(node1)==GSNode and type(node2)==GSNode:
				# set drawing color:
				fontColor = NSColor.whiteColor()
				drawingColor = NSColor.grayColor()
				drawingColor.set()
				scale = self.getScale()
				
				# draw line:
				NSBezierPath.setDefaultLineWidth_( 1.0 / scale )
				NSBezierPath.strokeLineFromPoint_toPoint_( node1.position, node2.position )
				
				# draw handles:
				# handlesize = self.getHandleSize() / scale
				# dots = NSBezierPath.bezierPath()
				# for thisNode in (node1,node2):
				# 	newDot = self.roundDotForPoint( thisNode.position, handlesize )
				# 	dots.appendBezierPath_( newDot )
				# dots.stroke()
				
				# write measurement:
				distance = hypot( node1.x - node2.x, node1.y - node2.y )
				distanceString = "%.1f" % distance
				middle = NSPoint( (node1.x+node2.x)*0.5, (node1.y+node2.y)*0.5 )
				typeSize = 12.0
				scaledSize = typeSize / scale
				
				if Glyphs.buildNumber == 965:
					distanceNSString = NSString.alloc().initWithString_(distanceString) #
					distanceNSString.drawBadgeAtPoint_size_color_backgroundColor_alignment_visibleInRect_( middle, scaledSize, fontColor, drawingColor, 3, NSMakeRect(NSNotFound, 0, 0, 0) )
				else:
					self.drawRoundedRectangleForStringAtPosition( distanceString, middle, typeSize )
					self.drawTextAtPoint( distanceString, middle, fontColor=fontColor, align='center', fontSize=typeSize )

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
