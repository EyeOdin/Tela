# Tela is a Krita plugin for a Canvas Tool Box
# Copyright (C) 2021  Ricardo Jeremias.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


# Krita
from krita import *
# PyQt5
from PyQt5 import QtWidgets, QtCore, QtGui, uic


class MirrorFix_Button( QWidget ):
    SIGNAL_SIDE = QtCore.pyqtSignal( str )
    SIGNAL_NEUTRAL = QtCore.pyqtSignal( str )

    # Initilization
    def __init__( self, parent ):
        super( MirrorFix_Button, self ).__init__( parent )
        # Variables
        self.origin_x = 0
        self.origin_y = 0
        self.side = None

    # Mouse Events
    def mousePressEvent( self, event ):
        # Read
        self.origin_x = event.x()
        self.origin_y = event.y()

        # Neutral
        if ( event.modifiers() == QtCore.Qt.NoModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.Cursor_Side( event )
    def mouseMoveEvent( self, event ):
        if ( event.modifiers() == QtCore.Qt.NoModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.Cursor_Side( event )
    def mouseDoubleClickEvent( self, event ):
        if ( event.modifiers() == QtCore.Qt.NoModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.Cursor_Side( event )
    def mouseReleaseEvent( self, event ):
        # Emite
        if self.side != None:
            self.Cursor_Signal( self.side )
        else:
            self.Cursor_Neutral()
        # Variables
        self.origin_x = 0
        self.origin_y = 0
        self.side = None

    # Mouse Operation
    def Cursor_Side( self, event ):
        # Read
        ex = event.x()
        ey = event.y()

        # Calculations
        delta_x = ex - self.origin_x
        delta_y = ey - self.origin_y
        dist = abs( delta_x ) + abs( delta_y )

        limit = 30
        if dist >= limit:
            if abs( delta_x ) > abs( delta_y ): # Horizontal
                if ex < self.origin_x:
                    self.side = "RIGHT"
                else:
                    self.side = "LEFT"
            else: # Vertical
                if ey < self.origin_y:
                    self.side = "DOWN"
                else:
                    self.side = "TOP"
        else:
            self.side = None
    def Cursor_Signal( self, side ):
        self.SIGNAL_SIDE.emit( side )
    def Cursor_Neutral( self ):
        self.SIGNAL_NEUTRAL.emit( "" )