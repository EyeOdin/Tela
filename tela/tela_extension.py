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


#region Imports ####################################################################

# Python Module
import zipfile
# Krita Module
from krita import *
# PyQt5 Modules
from PyQt5 import QtWidgets, QtCore, QtGui, uic
# Project Pages Modules
from .tela_modulo import (
    MirrorFix_Button,
    Color_Display,
    Color_Panel,
    )

#endregion
#region Global Variables ###########################################################

#region Plugin

tela_version = "2025_09_16"

#endregion


class Tela_Extension(Extension):
    """
    Tela ToolBox
    """

    #region Initialize #############################################################

    def __init__(self, parent):
        super().__init__(parent)
    def setup(self):
        self.User_Interface()
        self.Variables()
        self.Connections()
        self.Modules()
        # self.Timer()
        self.Style()

    def User_Interface( self ):
        # Operating System
        self.OS = str( QSysInfo.kernelType() ) # WINDOWS=winnt & LINUX=linux
        if self.OS == 'winnt': # Unlocks icons in Krita for Menu Mode
            QApplication.setAttribute( Qt.AA_DontShowIconsInMenus, False )

        # Path Name
        self.directory_plugin = str( os.path.dirname( os.path.realpath( __file__ ) ) )

        # Widget Docker
        tela_extension_ui = os.path.join( self.directory_plugin, "tela_extension.ui" )
        self.layout = uic.loadUi( tela_extension_ui, QWidget() )
        # Color Picker
        color_picker_ui = os.path.join( self.directory_plugin, "color_picker.ui" )
        self.color_picker = uic.loadUi( color_picker_ui, QWidget() )
    def Variables( self ):
        # System
        ki = Krita.instance()

        # None Variables
        self.qmenu = None
        self.stacked_widget = None
        self.qmdiarea = None
        self.window_list = []

        # Toolbox ( name, pykrita, qicon )
        self.tool = {
            "vector" : {
                "select_tool"        : [ "Select",        "InteractionTool",                   ki.icon( "select" ),                       0 ],
                "text_tool"          : [ "Text",          "SvgTextTool",                       ki.icon( "draw-text" ),                    1 ],
                "edit_tool"          : [ "Edit",          "PathTool",                          ki.icon( "shape_handling" ),               2 ],
                "calligraphy_tool"   : [ "Calligraphy",   "KarbonCalligraphyTool",             ki.icon( "calligraphy" ),                  3 ],
                },
            "brush" : {
                "freehand_brush"     : [ "Freehand",      "KritaShape/KisToolBrush",           ki.icon( "krita_tool_freehand" ),          0 ],
                "line_brush"         : [ "Line",          "KritaShape/KisToolLine",            ki.icon( "krita_tool_line" ),              1 ],
                "rectangle_brush"    : [ "Rectangle",     "KritaShape/KisToolRectangle",       ki.icon( "krita_tool_rectangle" ),         2 ],
                "ellipse_brush"      : [ "Ellipse",       "KritaShape/KisToolEllipse",         ki.icon( "krita_tool_ellipse" ),           3 ],
                "polygon_brush"      : [ "Polygon",       "KisToolPolygon",                    ki.icon( "krita_tool_polygon" ),           4 ],
                "polyline_brush"     : [ "Polyline",      "KisToolPolyline",                   ki.icon( "polyline" ),                     5 ],
                "bezier_brush"       : [ "Bezier",        "KisToolPath",                       ki.icon( "krita_draw_path" ),              6 ],
                "path_brush"         : [ "Path",          "KisToolPencil",                     ki.icon( "krita_tool_freehandvector" ),    7 ],
                "dynamic_brush"      : [ "Dynamic",       "KritaShape/KisToolDyna",            ki.icon( "krita_tool_dyna" ),              8 ],
                "multi_brush"        : [ "Multibrush",    "KritaShape/KisToolMultiBrush",      ki.icon( "krita_tool_multihand" ),         9 ],
                },
            "transform" : {
                "transform_tool"     : [ "Transform",     "KisToolTransform",                  ki.icon( "krita_tool_transform" ),         0 ],
                "move_tool"          : [ "Move",          "KritaTransform/KisToolMove",        ki.icon( "krita_tool_move" ),              1 ],
                "crop_tool"          : [ "Crop",          "KisToolCrop",                       ki.icon( "tool_crop" ),                    2 ],
                },
            "color" : {
                "gradient_tool"      : [ "Gradient",      "KritaFill/KisToolGradient",         ki.icon( "krita_tool_gradient" ),          0 ],
                "sampler_tool"       : [ "Sampler",       "KritaSelected/KisToolColorSampler", ki.icon( "krita_tool_color_sampler" ),     1 ],
                "colorize_tool"      : [ "Colorize",      "KritaShape/KisToolLazyBrush",       ki.icon( "krita_tool_lazybrush" ),         2 ],
                "patch_tool"         : [ "Patch",         "KritaShape/KisToolSmartPatch",      ki.icon( "krita_tool_smart_patch" ),       3 ],
                "fill_tool"          : [ "Fill",          "KritaFill/KisToolFill",             ki.icon( "krita_tool_color_fill" ),        4 ],
                "enclose_tool"       : [ "Enclose",       "KisToolEncloseAndFill",             ki.icon( "krita_tool_enclose_and_fill" ),  5 ],
                },
            "overlay" : {
                "assistant_tool"     : [ "Assistant",     "KisAssistantTool",                  ki.icon( "krita_tool_assistant" ),         0 ],
                "measure_tool"       : [ "Measure",       "KritaShape/KisToolMeasure",         ki.icon( "krita_tool_measure" ),           1 ],
                "reference_tool"     : [ "Reference",     "ToolReferenceImages",               ki.icon( "krita_tool_reference_images" ),  2 ],
                },
            "select" : {
                "rectangle_select"   : [ "Rectangle",     "KisToolSelectRectangular",          ki.icon( "tool_rect_selection" ),          0 ],
                "elliptical_select"  : [ "Elliptical",    "KisToolSelectElliptical",           ki.icon( "tool_elliptical_selection" ),    1 ],
                "polygon_select"     : [ "Polygon",       "KisToolSelectPolygonal",            ki.icon( "tool_polygonal_selection" ),     2 ],
                "freehand_select"    : [ "Freehand",      "KisToolSelectOutline",              ki.icon( "tool_outline_selection"),        3 ],
                "contiguous_select"  : [ "Contiguous",    "KisToolSelectContiguous",           ki.icon( "tool_contiguous_selection" ),    4 ],
                "color_select"       : [ "Color",         "KisToolSelectSimilar",              ki.icon( "tool_similar_selection"),        5 ],
                "bezier_select"      : [ "Bezier",        "KisToolSelectPath",                 ki.icon( "tool_path_selection"),           6 ],
                "magnetic_select"    : [ "Magnetic",      "KisToolSelectMagnetic",             ki.icon( "tool_magnetic_selection" ),      7 ],
                },
            "camera" : {
                "zoom_tool"          : [ "Zoom",          "ZoomTool",                          ki.icon( "tool_zoom" ),                    0 ],
                "pan_tool"           : [ "Pan",           "PanTool",                           ki.icon( "tool_pan" ),                     1 ],
                },
        }
        self.operation = {
            "vector"    : "InteractionTool",
            "brush"     : "KritaShape/KisToolBrush",
            "transform" : "KisToolTransform",
            "color"     : "KritaSelected/KisToolColorSampler",
            "overlay"   : "ToolReferenceImages",
            "select"    : "KisToolSelectOutline",
            "camera"    : "PanTool",
        }

        # Pushbutton Size
        self.bs = 35
        # Menu Margin
        self.mx = 10
        self.my = 10

        # QTimer
        self.press_time = 500 # 1000=1sec

        # Toolbox and Others
        self.Variables_Clean()

        # Color Picker Module
        self.pigment_o_check = False # state of the module
        self.pigment_o_pyid = "pykrita_pigment_o_picker_docker"
        self.pigment_o_module = None # pointer to the module

        # ProgressBar
        self.krita_progress_bar_id = "ProgressBar"
        self.krita_progress_bar_module = None

        # Color Picker
        self.qpixmap_list = []
        self.hue = self.color_picker.s1.maximum() # 360
        self.svl = self.color_picker.s2.maximum() # 255
        self.wheel_space = None # HSV HSL HCY ARD
        self.s1 = 0 # 0-360
        self.s2 = 0 # 0-255
        self.s3 = 0 # 0-255
        self.cor = None # Pigment.o color object
    def Connections( self ):
        # Vector
        self.layout.menu_vector.pressed.connect( self.Hold_Vector )
        self.layout.menu_vector.released.connect( self.Release_Vector )
        # Brush
        self.layout.menu_brush.pressed.connect( self.Hold_Brush )
        self.layout.menu_brush.released.connect( self.Release_Brush )
        # Transform
        self.layout.menu_transform.pressed.connect( self.Hold_Transform )
        self.layout.menu_transform.released.connect( self.Release_Transform )
        # Color
        self.layout.menu_color.pressed.connect( self.Hold_Color )
        self.layout.menu_color.released.connect( self.Release_Color )
        # Overlay
        self.layout.menu_overlay.pressed.connect( self.Hold_Overlay )
        self.layout.menu_overlay.released.connect( self.Release_Overlay )
        # Select
        self.layout.menu_select.pressed.connect( self.Hold_Select )
        self.layout.menu_select.released.connect( self.Release_Select )
        # Camera
        self.layout.menu_camera.pressed.connect( self.Hold_Camera )
        self.layout.menu_camera.released.connect( self.Release_Camera )
        # Actions
        self.layout.menu_action.pressed.connect( self.Hold_Action )
        self.layout.menu_action.released.connect( self.Release_Action )
        # View
        self.layout.menu_view.pressed.connect( self.Hold_View )
        self.layout.menu_view.released.connect( self.Release_View )
        # Color Picker
        self.layout.color_picker.clicked.connect( self.Show_Color_Picker )
        self.color_picker.s1.valueChanged.connect(   lambda: self.CS1_W( False ) )
        self.color_picker.s1.sliderReleased.connect( lambda: self.CS1_W( True ) )
        self.color_picker.s2.valueChanged.connect(   lambda: self.CS2_W( False ) )
        self.color_picker.s2.sliderReleased.connect( lambda: self.CS2_W( True ) )
        self.color_picker.s3.valueChanged.connect(   lambda: self.CS3_W( False ) )
        self.color_picker.s3.sliderReleased.connect( lambda: self.CS3_W( True ) )

        # User Interface Update
        self.layout.installEventFilter( self )
        self.color_picker.installEventFilter( self )
    def Modules( self ):
        #region Notifier
        self.notifier = Krita.instance().notifier()
        self.notifier.applicationClosing.connect( self.Application_Closing )
        self.notifier.configurationChanged.connect( self.Configuration_Changed )
        self.notifier.imageClosed.connect( self.Image_Closed )
        self.notifier.imageCreated.connect( self.Image_Created )
        self.notifier.imageSaved.connect( self.Image_Saved )
        self.notifier.viewClosed.connect( self.View_Closed )
        self.notifier.viewCreated.connect( self.View_Created )
        self.notifier.windowCreated.connect( self.Window_Created )
        self.notifier.windowIsBeingCreated.connect( self.Window_IsBeingCreated )

        #endregion
        #region Python

        self.mirror_fix = MirrorFix_Button( self.layout.mirror_fix )
        self.mirror_fix.SIGNAL_SIDE.connect( self.MirrorFix_Side )
        self.mirror_fix.SIGNAL_NEUTRAL.connect( self.MirrorFix_Explanation )

        #endregion
        #region Color Picker

        self.color_display = Color_Display( self.color_picker.color_display )

        self.color_panel = Color_Panel( self.color_picker.color_panel )
        self.color_panel.SIGNAL_PREVIEW.connect( self.Color_Panel_Preview )
        self.color_panel.SIGNAL_APPLY.connect( self.Color_Panel_Apply )

        #endregion
    def Timer( self ):
        self.qtimer = QtCore.QTimer( self )
        self.qtimer.timeout.connect( self.Update_Tool )
    def Style( self ):
        # Variables
        ki = Krita.instance()

        # Icon
        self.icon_mirrorfix = "wraparound"

        # Toolbox Icons
        self.layout.menu_vector.setIcon(    self.tool["vector"]["select_tool"][2]       )
        self.layout.menu_brush.setIcon(     self.tool["brush"]["freehand_brush"][2]     )
        self.layout.menu_transform.setIcon( self.tool["transform"]["transform_tool"][2] )
        self.layout.menu_color.setIcon(     self.tool["color"]["sampler_tool"][2]       )
        self.layout.menu_overlay.setIcon(   self.tool["overlay"]["reference_tool"][2]   )
        self.layout.menu_select.setIcon(    self.tool["select"]["freehand_select"][2]   )
        self.layout.menu_camera.setIcon(    self.tool["camera"]["pan_tool"][2]          )
        # Others Icons
        self.layout.menu_action.setIcon(    ki.icon( "updateColorize" ) )
        self.layout.menu_view.setIcon(      ki.icon( "view-filter" ) )
        self.layout.mirror_fix.setIcon(     ki.icon( self.icon_mirrorfix )   )
        self.layout.color_picker.setIcon(   ki.icon( "close-tab" ) )

        # Toolbox Label
        self.layout.menu_vector.setText( "" )
        self.layout.menu_brush.setText( "" )
        self.layout.menu_transform.setText( "" )
        self.layout.menu_color.setText( "" )
        self.layout.menu_overlay.setText( "" )
        self.layout.menu_select.setText( "" )
        self.layout.menu_camera.setText( "" )
        # Others Label
        self.layout.menu_action.setText( "" )
        self.layout.menu_view.setText( "" )
        self.layout.mirror_fix.setText( "" )
        self.layout.color_picker.setText( "" )

        # StyleSheet
        self.layout.progress_bar.setStyleSheet( "#progress_bar{ background-color: rgba( 0, 0, 0, 0 ); }" )

    #endregion
    #region Management #############################################################

    # Warnnings
    def Message_Float( self, operation, message, icon ):
        ki = Krita.instance()
        string = f"TELA | { operation } { message }"
        try:ki.activeWindow().activeView().showFloatingMessage( string, ki.icon( icon ), 5000, 0 )
        except:pass

    # Math
    def Limit_Range( self, value, mini, maxi, minifix, maxifix ):
        if value <= mini:
            value = mini + minifix
        if value >= maxi:
            value = maxi + maxifix
        return value

    # Geometry
    def Size_Update( self ):
        if self.qmdiarea != None:
            # Variables
            qmdw = self.qmdiarea.width()
            qmdh = self.qmdiarea.height()
            lw = self.layout.width()
            lh = self.layout.height()
            # Calculations
            px1 = qmdw * 0.5 - lw * 0.5
            px2 = qmdw * 0.5 + lw * 0.5
            py = qmdh - 70
            # Variables
            widget = self.color_picker
            ww = widget.width()
            wh = widget.height()
            # Geometry
            self.Tela_Geometry( px1, py, lw, lh )
            self.Picker_Geometry( px2 - self.bs, py - self.my - wh, ww, wh )
    def Tela_Geometry( self, px, py, ww, wh ):
        self.layout.setGeometry( int( px ), int( py ), int( ww ), int( wh ) )
    def Picker_Geometry( self, px, py, ww, wh ):
        self.color_picker.setGeometry( int( px ), int( py ), int( ww ), int( wh ) )

    # Timer Check
    def Toolbox_Button( self ):
        qwindow = Krita.instance().activeWindow().qwindow()
        # Vector Checks
        self.button_select_tool =       qwindow.findChild( QToolButton, self.tool["vector"]["select_tool"][1] )
        self.button_text_tool =         qwindow.findChild( QToolButton, self.tool["vector"]["text_tool"][1] )
        self.button_edit_tool =         qwindow.findChild( QToolButton, self.tool["vector"]["edit_tool"][1] )
        self.button_calligraphy_tool =  qwindow.findChild( QToolButton, self.tool["vector"]["calligraphy_tool"][1] )
        # Brush Checks
        self.button_freehand_brush =    qwindow.findChild( QToolButton, self.tool["brush"]["freehand_brush"][1] )
        self.button_line_brush =        qwindow.findChild( QToolButton, self.tool["brush"]["line_brush"][1] )
        self.button_rectangle_brush =   qwindow.findChild( QToolButton, self.tool["brush"]["rectangle_brush"][1] )
        self.button_ellipse_brush =     qwindow.findChild( QToolButton, self.tool["brush"]["ellipse_brush"][1] )
        self.button_polygon_brush =     qwindow.findChild( QToolButton, self.tool["brush"]["polygon_brush"][1] )
        self.button_polyline_brush =    qwindow.findChild( QToolButton, self.tool["brush"]["polyline_brush"][1] )
        self.button_bezier_brush =      qwindow.findChild( QToolButton, self.tool["brush"]["bezier_brush"][1] )
        self.button_path_brush =        qwindow.findChild( QToolButton, self.tool["brush"]["path_brush"][1] )
        self.button_dynamic_brush =     qwindow.findChild( QToolButton, self.tool["brush"]["dynamic_brush"][1] )
        self.button_multi_brush =       qwindow.findChild( QToolButton, self.tool["brush"]["multi_brush"][1] )
        # Transform Checks
        self.button_transform_tool =    qwindow.findChild( QToolButton, self.tool["transform"]["transform_tool"][1] )
        self.button_move_tool =         qwindow.findChild( QToolButton, self.tool["transform"]["move_tool"][1] )
        self.button_crop_tool =         qwindow.findChild( QToolButton, self.tool["transform"]["crop_tool"][1] )
        # Color Checks
        self.button_gradient_tool =     qwindow.findChild( QToolButton, self.tool["color"]["gradient_tool"][1] )
        self.button_sampler_tool =      qwindow.findChild( QToolButton, self.tool["color"]["sampler_tool"][1] )
        self.button_colorize_tool =     qwindow.findChild( QToolButton, self.tool["color"]["colorize_tool"][1] )
        self.button_patch_tool =        qwindow.findChild( QToolButton, self.tool["color"]["patch_tool"][1] )
        self.button_fill_tool =         qwindow.findChild( QToolButton, self.tool["color"]["fill_tool"][1] )
        self.button_enclose_tool =      qwindow.findChild( QToolButton, self.tool["color"]["enclose_tool"][1] )
        # Overlay Checks
        self.button_assistant_tool =    qwindow.findChild( QToolButton, self.tool["overlay"]["assistant_tool"][1] )
        self.button_measure_tool =      qwindow.findChild( QToolButton, self.tool["overlay"]["measure_tool"][1] )
        self.button_reference_tool =    qwindow.findChild( QToolButton, self.tool["overlay"]["reference_tool"][1] )
        # Selection Checks
        self.button_rectangle_select =  qwindow.findChild( QToolButton, self.tool["select"]["rectangle_select"][1] )
        self.button_elliptical_select = qwindow.findChild( QToolButton, self.tool["select"]["elliptical_select"][1] )
        self.button_polygon_select =    qwindow.findChild( QToolButton, self.tool["select"]["polygon_select"][1] )
        self.button_freehand_select =   qwindow.findChild( QToolButton, self.tool["select"]["freehand_select"][1] )
        self.button_contiguous_select = qwindow.findChild( QToolButton, self.tool["select"]["contiguous_select"][1] )
        self.button_color_select =      qwindow.findChild( QToolButton, self.tool["select"]["color_select"][1] )
        self.button_bezier_select =     qwindow.findChild( QToolButton, self.tool["select"]["bezier_select"][1] )
        self.button_magnetic_select =   qwindow.findChild( QToolButton, self.tool["select"]["magnetic_select"][1] )
        # Camera Checks
        self.button_zoom_tool =         qwindow.findChild( QToolButton, self.tool["camera"]["zoom_tool"][1] )
        self.button_pan_tool =          qwindow.findChild( QToolButton, self.tool["camera"]["pan_tool"][1] )
    def Update_Tool( self ):
        check_canvas = self.Check_Canvas()
        if check_canvas == True:

            # Vector Checks
            try:select_tool =       self.button_select_tool.isChecked()
            except:pass
            try:text_tool =         self.button_text_tool.isChecked()
            except:pass
            try:edit_tool =         self.button_edit_tool.isChecked()
            except:pass
            try:calligraphy_tool =  self.button_calligraphy_tool.isChecked()
            except:pass
            # Brush Checks
            try:freehand_brush =    self.button_freehand_brush.isChecked()
            except:pass
            try:line_brush =        self.button_line_brush.isChecked()
            except:pass
            try:rectangle_brush =   self.button_rectangle_brush.isChecked()
            except:pass
            try:ellipse_brush =     self.button_ellipse_brush.isChecked()
            except:pass
            try:polygon_brush =     self.button_polygon_brush.isChecked()
            except:pass
            try:polyline_brush =    self.button_polyline_brush.isChecked()
            except:pass
            try:bezier_brush =      self.button_bezier_brush.isChecked()
            except:pass
            try:path_brush =        self.button_path_brush.isChecked()
            except:pass
            try:dynamic_brush =     self.button_dynamic_brush.isChecked()
            except:pass
            try:multi_brush =       self.button_multi_brush.isChecked()
            except:pass
            # Transform Checks
            try:transform_tool =    self.button_transform_tool.isChecked()
            except:pass
            try:move_tool =         self.button_move_tool.isChecked()
            except:pass
            try:crop_tool =         self.button_crop_tool.isChecked()
            except:pass
            # Color Checks
            try:gradient_tool =     self.button_gradient_tool.isChecked()
            except:pass
            try:sampler_tool =      self.button_sampler_tool.isChecked()
            except:pass
            try:colorize_tool =     self.button_colorize_tool.isChecked()
            except:pass
            try:patch_tool =        self.button_patch_tool.isChecked()
            except:pass
            try:fill_tool =         self.button_fill_tool.isChecked()
            except:pass
            try:enclose_tool =      self.button_enclose_tool.isChecked()
            except:pass
            # Overlay Checks
            try:assistant_tool =    self.button_assistant_tool.isChecked()
            except:pass
            try:measure_tool =      self.button_measure_tool.isChecked()
            except:pass
            try:reference_tool =    self.button_reference_tool.isChecked()
            except:pass
            # Selection Checks
            try:rectangle_select =  self.button_rectangle_select.isChecked()
            except:pass
            try:elliptical_select = self.button_elliptical_select.isChecked()
            except:pass
            try:polygon_select =    self.button_polygon_select.isChecked()
            except:pass
            try:freehand_select =   self.button_freehand_select.isChecked()
            except:pass
            try:contiguous_select = self.button_contiguous_select.isChecked()
            except:pass
            try:color_select =      self.button_color_select.isChecked()
            except:pass
            try:bezier_select =     self.button_bezier_select.isChecked()
            except:pass
            try:magnetic_select =   self.button_magnetic_select.isChecked()
            except:pass
            # Camera Checks
            try:zoom_tool =         self.button_zoom_tool.isChecked()
            except:pass
            try:pan_tool =          self.button_pan_tool.isChecked()
            except:pass

            # Group
            if   select_tool          == True : self.Apply_Tool( "vector", "select_tool", self.layout.menu_vector )
            elif text_tool            == True : self.Apply_Tool( "vector", "text_tool", self.layout.menu_vector )
            elif edit_tool            == True : self.Apply_Tool( "vector", "edit_tool", self.layout.menu_vector )
            elif calligraphy_tool     == True : self.Apply_Tool( "vector", "calligraphy_tool", self.layout.menu_vector )
            # Brush Checks
            elif freehand_brush       == True : self.Apply_Tool( "brush", "freehand_brush", self.layout.menu_brush )
            elif line_brush           == True : self.Apply_Tool( "brush", "line_brush", self.layout.menu_brush )
            elif rectangle_brush      == True : self.Apply_Tool( "brush", "rectangle_brush", self.layout.menu_brush )
            elif ellipse_brush        == True : self.Apply_Tool( "brush", "ellipse_brush", self.layout.menu_brush )
            elif polygon_brush        == True : self.Apply_Tool( "brush", "polygon_brush", self.layout.menu_brush )
            elif polyline_brush       == True : self.Apply_Tool( "brush", "polyline_brush", self.layout.menu_brush )
            elif bezier_brush         == True : self.Apply_Tool( "brush", "bezier_brush", self.layout.menu_brush )
            elif path_brush           == True : self.Apply_Tool( "brush", "path_brush", self.layout.menu_brush )
            elif dynamic_brush        == True : self.Apply_Tool( "brush", "dynamic_brush", self.layout.menu_brush )
            elif multi_brush          == True : self.Apply_Tool( "brush", "multi_brush", self.layout.menu_brush )
            # Transform Checks
            elif transform_tool       == True : self.Apply_Tool( "transform", "transform_tool", self.layout.menu_transform )
            elif move_tool            == True : self.Apply_Tool( "transform", "move_tool", self.layout.menu_transform )
            elif crop_tool            == True : self.Apply_Tool( "transform", "crop_tool", self.layout.menu_transform )
            # Color Checks
            elif gradient_tool        == True : self.Apply_Tool( "color", "gradient_tool", self.layout.menu_color )
            elif sampler_tool         == True : self.Apply_Tool( "color", "sampler_tool", self.layout.menu_color )
            elif colorize_tool        == True : self.Apply_Tool( "color", "colorize_tool", self.layout.menu_color )
            elif patch_tool           == True : self.Apply_Tool( "color", "patch_tool", self.layout.menu_color )
            elif fill_tool            == True : self.Apply_Tool( "color", "fill_tool", self.layout.menu_color )
            elif enclose_tool         == True : self.Apply_Tool( "color", "enclose_tool", self.layout.menu_color )
            # Overlay Checks
            elif assistant_tool       == True : self.Apply_Tool( "overlay", "assistant_tool", self.layout.menu_overlay )
            elif measure_tool         == True : self.Apply_Tool( "overlay", "measure_tool", self.layout.menu_overlay )
            elif reference_tool       == True : self.Apply_Tool( "overlay", "reference_tool", self.layout.menu_overlay )
            # Selection Checks
            elif rectangle_select     == True : self.Apply_Tool( "select", "rectangle_select", self.layout.menu_select )
            elif elliptical_select    == True : self.Apply_Tool( "select", "elliptical_select", self.layout.menu_select )
            elif polygon_select       == True : self.Apply_Tool( "select", "polygon_select", self.layout.menu_select )
            elif freehand_select      == True : self.Apply_Tool( "select", "freehand_select", self.layout.menu_select )
            elif contiguous_select    == True : self.Apply_Tool( "select", "contiguous_select", self.layout.menu_select )
            elif color_select         == True : self.Apply_Tool( "select", "color_select", self.layout.menu_select )
            elif bezier_select        == True : self.Apply_Tool( "select", "bezier_select", self.layout.menu_select )
            elif magnetic_select      == True : self.Apply_Tool( "select", "magnetic_select", self.layout.menu_select )
            # Camera Checks
            elif zoom_tool            == True : self.Apply_Tool( "camera", "zoom_tool", self.layout.menu_camera )
            elif pan_tool             == True : self.Apply_Tool( "camera", "pan_tool", self.layout.menu_camera )
    def Apply_Tool( self, mode, tool, widget ):
        # Variables
        operation = self.tool[mode][tool][1]
        qicon = self.tool[mode][tool][2]
        # Tool
        self.operation[mode] = operation
        # UI
        widget.setIcon( qicon )
        widget.setChecked( True )

    # Widgets
    def Toolbox_Display( self ):
        # Import Pigment.o module
        if self.pigment_o_check == False:
            self.Import_Pigment_O()

        # Window
        ki = Krita.instance()
        self.window = Krita.instance().activeWindow()

        # Main Window
        self.stacked_widget = self.window.qwindow().centralWidget()
        self.qmdiarea = self.stacked_widget.findChild( QMdiArea )
        self.qmdiarea.installEventFilter( self )
        # Display
        self.layout.setParent( self.qmdiarea )
        self.layout.show()
        # Color Picker
        self.color_picker.setParent( self.qmdiarea )
        self.color_picker.hide()
        # Progress Bar
        self.krita_progress_bar = self.window.qwindow().statusBar().findChild( QProgressBar )
        self.krita_progress_bar.valueChanged.connect( self.Progress_Bar )

    def Check_Canvas( self ):
        # Replaces
        # if ( ( self.canvas() is not None ) and ( self.canvas().view() is not None ) ):

        # Variables
        ki = Krita.instance()
        view = ki.activeWindow().activeView()
        canvas = view.canvas()

        # Return
        if ( canvas is not None ) and ( view is not None ): return True
        else:                                               return False
    def Button_Highlight( self, button, name, qcolor ):
        try:
            rgb = f"{ qcolor.red() },{ qcolor.green() },{ qcolor.blue() }"
            button.setStyleSheet("#" + name + "::checked{ background-color : rgb( " + rgb + " );}" )
        except:
            pass

    #endregion
    #region ToolBox ################################################################

    # Variables
    def Variables_Clean( self ):
        # Toolbox
        self.menu_vector = False
        self.menu_brush = False
        self.menu_transform = False
        self.menu_color = False
        self.menu_overlay = False
        self.menu_select = False
        self.menu_camera = False
        # Others
        self.menu_action = False
        self.menu_view = False
        # Color Picker
        self.color_picker.hide()

    # Hold
    def Hold_Vector( self ):
        self.Menu_Clear()
        self.Variables_Clean()
        self.menu_vector = True
        QtCore.QTimer.singleShot( self.press_time, lambda: self.Menu_Vector( False ) )
    def Hold_Brush( self ):
        self.Menu_Clear()
        self.Variables_Clean()
        self.menu_brush = True
        QtCore.QTimer.singleShot( self.press_time, lambda: self.Menu_Brush( False ) )
    def Hold_Transform( self ):
        self.Menu_Clear()
        self.Variables_Clean()
        self.menu_transform = True
        QtCore.QTimer.singleShot( self.press_time, lambda: self.Menu_Transform( False ) )
    def Hold_Color( self ):
        self.Menu_Clear()
        self.Variables_Clean()
        self.menu_color = True
        QtCore.QTimer.singleShot( self.press_time, lambda: self.Menu_Color( False ) )
    def Hold_Overlay( self ):
        self.Menu_Clear()
        self.Variables_Clean()
        self.menu_overlay = True
        QtCore.QTimer.singleShot( self.press_time, lambda: self.Menu_Overlay( False ) )
    def Hold_Select( self ):
        self.Menu_Clear()
        self.Variables_Clean()
        self.menu_select = True
        QtCore.QTimer.singleShot( self.press_time, lambda: self.Menu_Select( False ) )
    def Hold_Camera( self ):
        self.Menu_Clear()
        self.Variables_Clean()
        self.menu_camera = True
        QtCore.QTimer.singleShot( self.press_time, lambda: self.Menu_Camera( False ) )
    def Hold_Action( self ):
        self.Menu_Clear()
        self.Variables_Clean()
        self.menu_action = True
        QtCore.QTimer.singleShot( self.press_time, self.Menu_Action )
    def Hold_View( self ):
        self.Menu_Clear()
        self.Variables_Clean()
        self.menu_view = True
        QtCore.QTimer.singleShot( self.press_time, self.Menu_View )
        
    # Release
    def Release_Vector( self ):
        self.menu_vector = False
        Krita.instance().action( self.operation["vector"] ).trigger()
        self.Menu_Clear()
    def Release_Brush( self ):
        self.menu_brush = False
        Krita.instance().action( self.operation["brush"] ).trigger()
        self.Menu_Clear()
    def Release_Transform( self ):
        self.menu_transform = False
        Krita.instance().action( self.operation["transform"] ).trigger()
        self.Menu_Clear()
    def Release_Color( self ):
        self.menu_color = False
        Krita.instance().action( self.operation["color"] ).trigger()
        self.Menu_Clear()
    def Release_Overlay( self ):
        self.menu_overlay = False
        Krita.instance().action( self.operation["overlay"] ).trigger()
        self.Menu_Clear()
    def Release_Select( self ):
        self.menu_select = False
        Krita.instance().action( self.operation["select"] ).trigger()
        self.Menu_Clear()
    def Release_Camera( self ):
        self.menu_camera = False
        Krita.instance().action( self.operation["camera"] ).trigger()
        self.Menu_Clear()
    def Release_Action( self ):
        self.menu_action = False
        self.Menu_Clear()
    def Release_View( self ):
        self.menu_view = False
        self.Menu_Clear()

    # Menu
    def Menu_Clear( self ):
        try:
            self.qmenu.clear()
        except:
            pass
    def Menu_Down( self ):
        # Toolbox
        self.layout.menu_vector.setDown( False )
        self.layout.menu_brush.setDown( False )
        self.layout.menu_transform.setDown( False )
        self.layout.menu_color.setDown( False )
        self.layout.menu_overlay.setDown( False )
        self.layout.menu_select.setDown( False )
        self.layout.menu_camera.setDown( False )
        # Other
        self.layout.menu_action.setDown( False )
        self.layout.menu_view.setDown( False )

    # Menu
    def Menu_Vector( self, menu ):
        if ( self.menu_vector == True or menu == True ):
            self.Menu_Toolbox( "vector", self.layout.menu_vector )
    def Menu_Brush( self, menu ):
        if ( self.menu_brush == True or menu == True ):
            self.Menu_Toolbox( "brush", self.layout.menu_brush )
    def Menu_Transform( self, menu ):
        if ( self.menu_transform == True or menu == True ):
            self.Menu_Toolbox( "transform", self.layout.menu_transform )
    def Menu_Color( self, menu ):
        if ( self.menu_color == True or menu == True ):
            self.Menu_Toolbox( "color", self.layout.menu_color )
    def Menu_Overlay( self, menu ):
        if ( self.menu_overlay == True or menu == True ):
            self.Menu_Toolbox( "overlay", self.layout.menu_overlay )
    def Menu_Select( self, menu ):
        if ( self.menu_select == True or menu == True ):
            self.Menu_Toolbox( "select", self.layout.menu_select )
    def Menu_Camera( self, menu ):
        if ( self.menu_camera == True or menu == True ):
            self.Menu_Toolbox( "camera", self.layout.menu_camera )

    # Menu
    def Menu_Toolbox( self, mode, widget ):
        check = (
            self.menu_vector == True,
            self.menu_brush == True,
            self.menu_transform == True,
            self.menu_color == True,
            self.menu_overlay == True,
            self.menu_select == True,
            self.menu_camera == True,
            )
        if True in check:
            # Variables
            ki = Krita.instance()
            key = list( self.tool[mode].keys() )
            len_key = len( key )

            # Menu
            self.qmenu = QMenu()

            # Actions
            action_menu = []
            for k in key:
                string = self.tool[mode][k][0]
                qicon = self.tool[mode][k][2]
                action_menu.append( QAction( qicon, string ) )
            self.qmenu.addActions( action_menu )

            # Mapping
            size = 23  # 23 is the expected height of a self.qmenu item on windows at least
            height = size * len_key
            qpoint = widget.geometry().topLeft()
            pos = self.layout.tool_box.mapToGlobal( qpoint )
            point = QPoint( pos.x(), pos.y() - self.my - height )
            action = self.qmenu.exec_( point )

            # Pin
            if action in action_menu:
                # Variables
                index = action_menu.index( action )
                k = key[index]
                operation = self.tool[mode][k][1]
                qicon = self.tool[mode][k][2]
                # Tool
                ki.action( operation ).trigger()
                self.operation[mode] = operation
                # UI
                widget.setIcon( qicon )
                widget.setChecked( True )
        self.Menu_Down()
    def Menu_Action( self ):
        if self.menu_action == True:
            # Variables
            widget = self.layout.menu_action
            ki = Krita.instance()

            # Menu
            self.qmenu = QMenu()

            # Edit Actions
            action_edit_cut_sharp = self.qmenu.addAction( "Cut Sharp" )
            action_edit_copy_sharp = self.qmenu.addAction( "Copy Sharp" )
            self.qmenu.addSeparator()
            # Selection Actions
            action_select_all = self.qmenu.addAction( "Select All" )
            action_select_none = self.qmenu.addAction( "Select None" )
            action_select_invert = self.qmenu.addAction( "Select Invert" )

            # Icons
            action_edit_cut_sharp.setIcon( ki.icon( "edit-cut" ) )
            action_edit_copy_sharp.setIcon( ki.icon( "edit-copy" ) )
            action_select_all.setIcon( ki.icon( "select-all" ) )
            action_select_none.setIcon( ki.icon( "select-clear" ) )
            action_select_invert.setIcon( ki.icon( "selection-mode_ants" ) )

            # Mapping
            item = 5
            size = 23  # 23 is the expected height of a self.qmenu item on windows at least
            height = size * item
            qpoint = widget.geometry().topLeft()
            pos = self.layout.mapToGlobal( qpoint )
            point = QPoint( pos.x(), pos.y() - self.my - height )
            action = self.qmenu.exec_( point )

            # Edit
            if action == action_edit_cut_sharp:     self.Edit_Cut_Sharp()
            if action == action_edit_copy_sharp:    self.Edit_Copy_Sharp()
            # Select
            if action == action_select_all:         self.Select_All()
            if action == action_select_none:        self.Select_None()
            if action == action_select_invert:      self.Select_Invert()
        self.Menu_Down()
    def Menu_View( self ):
        if self.menu_view == True:
            # Variables
            widget = self.layout.menu_view
            ki = Krita.instance()
            ad = ki.activeDocument()

            # Read State
            view_docker_ui = ki.action( "view_toggledockers" ).isChecked()
            # Read Layer
            layer_isolate = ki.action( "isolate_active_layer" ).isChecked()
            # Read Canvas
            canvas_mirror = ki.action( "mirror_canvas" ).isChecked()
            canvas_wrap = ki.action( "wrap_around_mode" ).isChecked()
            canvas_grid = ki.action( "view_pixel_grid" ).isChecked()
            # Read Guides
            guides_ruler = ki.action( "view_ruler" ).isChecked()
            guides_snap = ki.action( "view_snap_to_guides" ).isChecked()
            guides_show = ad.guidesVisible()
            guides_lock = ad.guidesLocked()
            # Read View
            view_painting_assistant = ki.action( "view_toggle_painting_assistants" ).isChecked()
            view_assitant_preview = ki.action( "view_toggle_assistant_previews" ).isChecked()
            view_reference_image = ki.action( "view_toggle_reference_images" ).isChecked()

            # Menu
            self.qmenu = QMenu()

            # State
            action_view_docker_ui = self.qmenu.addAction( "View Docker UI" )
            action_view_docker_ui.setCheckable( True )
            action_view_docker_ui.setChecked( view_docker_ui )
            self.qmenu.addSeparator()
            # Layers
            action_layer_isolate = self.qmenu.addAction( "Layer Isolate" )
            action_layer_isolate.setCheckable( True )
            action_layer_isolate.setChecked( layer_isolate )
            self.qmenu.addSeparator()
            # Canvas
            action_canvas_mirror = self.qmenu.addAction( "Canvas Mirror" )
            action_canvas_wrap = self.qmenu.addAction( "Canvas Wrap" )
            action_canvas_mirror.setCheckable( True )
            action_canvas_wrap.setCheckable( True )
            action_canvas_mirror.setChecked( canvas_mirror )
            action_canvas_wrap.setChecked( canvas_wrap )
            self.qmenu.addSeparator()
            # Guides
            action_guides_ruler = self.qmenu.addAction( "Guides Ruler" )
            action_guides_snap = self.qmenu.addAction( "Guides Snap" )
            action_guides_show = self.qmenu.addAction( "Guides Show" )
            action_guides_lock = self.qmenu.addAction( "Guides Lock" )
            action_guides_ruler.setCheckable( True )
            action_guides_snap.setCheckable( True )
            action_guides_show.setCheckable( True )
            action_guides_lock.setCheckable( True )
            action_guides_ruler.setChecked( guides_ruler )
            action_guides_snap.setChecked( guides_snap )
            action_guides_show.setChecked( guides_show )
            action_guides_lock.setChecked( guides_lock )
            self.qmenu.addSeparator()
            # View
            action_view_painting_assistant = self.qmenu.addAction( "View Painting Assistant" )
            action_view_assitant_preview = self.qmenu.addAction( "View Assistant Preview" )
            action_view_reference_image = self.qmenu.addAction( "View Reference Image" )
            action_view_painting_assistant.setCheckable( True )
            action_view_assitant_preview.setCheckable( True )
            action_view_reference_image.setCheckable( True )
            action_view_painting_assistant.setChecked( view_painting_assistant )
            action_view_assitant_preview.setChecked( view_assitant_preview )
            action_view_reference_image.setChecked( view_reference_image )
            self.qmenu.addSeparator()
            # Selection
            action_selection_overlay_mode = self.qmenu.addAction( "Selection Overlay Mode" )

            # Mapping
            item_num = 12
            item_size = 23  # 23 is the expected height of a self.qmenu item on windows at least
            sep_num = 6
            height = item_size * item_num + sep_num
            qpoint = widget.geometry().topLeft()
            pos = self.layout.mapToGlobal( qpoint )
            point = QPoint( pos.x(), pos.y() - self.my - height )
            action = self.qmenu.exec_( point )

            # State
            if action == action_view_docker_ui:             self.View_Docker_UI()
            # Layers
            if action == action_layer_isolate:              self.Layer_Isolate()
            # Canvas
            if action == action_canvas_mirror:              self.Canvas_Mirror()
            if action == action_canvas_wrap:                self.Canvas_Wrap()
            # Guides
            if action == action_guides_ruler:               self.Guides_Ruler()
            if action == action_guides_snap:                self.Guides_Snap()
            if action == action_guides_show:                self.Guides_Show()
            if action == action_guides_lock:                self.Guides_Lock()
            # View
            if action == action_view_painting_assistant:    self.View_Painting_Assistant()
            if action == action_view_assitant_preview:      self.View_Assistant_Preview()
            if action == action_view_reference_image:       self.View_Reference_Image()
            # Selection
            if action == action_selection_overlay_mode:     self.Selection_Overlay_Mode()
        self.Menu_Down()

    # Progress Bar
    def Progress_Bar( self, value ):
        if value >= 99:
            value = 0
        self.layout.progress_bar.setValue( int( value ) )

    #endregion
    #region Actions ################################################################

    # Select
    def Select_All( self ):
        Krita.instance().action( "select_all" ).trigger()
    def Select_None( self ):
        Krita.instance().action( "deselect" ).trigger()
    def Select_Invert( self ):
        Krita.instance().action( "invert_selection" ).trigger()
    def Select_Display( self ):
        Krita.instance().action( "toggle-selection-overlay-mode" ).trigger()
    # Edit
    def Edit_Cut_Sharp( self ):
        Krita.instance().action( "cut_sharp" ).trigger()
    def Edit_Copy_Sharp( self ):
        Krita.instance().action( "copy_sharp" ).trigger()

    # Dockers
    def View_Docker_UI( self ):
        Krita.instance().action( "view_toggledockers" ).trigger()
    def View_Docker_Title( self ):
        Krita.instance().action( "view_toggledockertitlebars" ).trigger()
    # Layer
    def Layer_Isolate( self ):
        Krita.instance().action( "isolate_active_layer" ).trigger()
    # Canvas
    def Canvas_Mirror( self ):
        Krita.instance().action( "mirror_canvas" ).trigger()
    def Canvas_Wrap( self ):
        Krita.instance().action( "wrap_around_mode" ).trigger()
    # Guides
    def Guides_Ruler( self ):
        Krita.instance().action( "view_ruler" ).trigger()
    def Guides_Snap( self ):
        Krita.instance().action( "view_snap_to_guides" ).trigger()
    def Guides_Show( self ):
        Krita.instance().action( "view_show_guides" ).trigger()
    def Guides_Lock( self ):
        Krita.instance().action( "view_lock_guides" ).trigger()
    # View
    def View_Painting_Assistant( self ):
        Krita.instance().action( "view_toggle_painting_assistants" ).trigger()
    def View_Assistant_Preview( self ):
        Krita.instance().action( "view_toggle_assistant_previews" ).trigger()
    def View_Reference_Image( self ):
        Krita.instance().action( "view_toggle_reference_images" ).trigger()
    # Selection
    def Selection_Overlay_Mode( self ):
        Krita.instance().action( "toggle-selection-overlay-mode" ).trigger()

    #endregion
    #region Mirror Fix #############################################################

    def MirrorFix_Explanation( self ):
        self.Variables_Clean()
        self.Message_Float( "MIRROR FIX", f"Press and hold LMB then do a vertical or horizontal drag and release", self.icon_mirrorfix )
        self.Menu_Clear()

    def MirrorFix_Side( self, SIGNAL_SIDE ):
        self.Variables_Clean()
        check_canvas = self.Check_Canvas()
        if check_canvas == True:
            boolean = QMessageBox.question( None, "TELA", f"Mirror Fix Selected Layer(s) ?\nSource = { SIGNAL_SIDE }", QMessageBox.Yes, QMessageBox.No )
            if ( boolean == QMessageBox.Yes and SIGNAL_SIDE != None ):
                self.MirrorFix_Run( SIGNAL_SIDE )
    def MirrorFix_Run( self, side ):
        check_canvas = self.Check_Canvas()
        if check_canvas == True:
            # Warnning
            self.Message_Float( "MIRROR FIX", f"START", self.icon_mirrorfix )

            # State
            ki = Krita.instance()
            ad = ki.activeDocument()
            av = ki.activeWindow().activeView()
            # Variables
            width = int( ad.width() )
            height = int( ad.height() )
            w2 = int( width * 0.5 )
            h2 = int( height * 0.5 )

            # Selection
            ss = ad.selection()
            if ss == None: # Square
                state = True
                # Correction
                if side in ( "LEFT", "RIGHT" ):
                    r = width % 2
                    if r == 0:m = 0
                    else:m = 1
                if side in ( "TOP", "DOWN" ):
                    r = height % 2
                    if r == 0:m = 0
                    else:m = 1
                # Variables
                if side == "LEFT":
                    px = 0
                    py = 0
                    pw = w2 + m
                    ph = height
                if side == "RIGHT":
                    px = w2
                    py = 0
                    pw = w2 + m
                    ph = height
                if side == "TOP":
                    px = 0
                    py = 0
                    pw = width
                    ph = h2 + m
                if side == "DOWN":
                    px = 0
                    py = h2
                    pw = width
                    ph = h2 + m
                # Selection
                sel = Selection()
                sel.select( int( px ), int( py ), int( pw ), int( ph ), 255 )
                ad.setSelection( sel )
            else: # Custom
                state = False
                sel = ss
                px = sel.x()
                py = sel.y()
                pw = sel.width()
                ph = sel.height()
            sel.invert()
            selection_data = sel.pixelData( 0, 0, width, height )
            ki.action( 'deselect' ).trigger()

            # Cycle
            old_node_list = av.selectedNodes()
            for old_node in old_node_list:
                node_type = old_node.type()
                if str( node_type ) == "paintlayer":
                    # Variables
                    old_name = old_node.name()
                    new_name = f"Mirror Fix : { old_name }"
                    parent = old_node.parentNode()
                    # Old Node
                    ad.setActiveNode( old_node )
                    self.Wait( ad )
                    # New Node
                    new_node = ad.createNode( new_name, "paintLayer" )
                    parent.addChildNode( new_node, old_node )
                    # Copy Paste
                    if state == True:
                        pixel_array = old_node.pixelData( int( px ), int( py ), int( pw ), int( ph ) )
                        new_node.setPixelData( pixel_array, int( px ), int( py ), int( pw ), int( ph ) )
                    if state == False:
                        pixel_array = old_node.pixelData( int( 0 ), int( 0 ), int( width ), int( height ) )
                        new_node.setPixelData( pixel_array, int( 0 ), int( 0 ), int( width ), int( height ) )

            # Re-Select
            sel = Selection()
            sel.setPixelData( selection_data, 0, 0, width, height )
            ad.setSelection( sel )
            # Cycle
            for old_node in old_node_list:
                node_type = old_node.type()
                if str( node_type ) == "paintlayer":
                    # Old Node
                    ad.setActiveNode( old_node )
                    self.Wait( ad )
                    # Clear
                    ki.action( 'clear' ).trigger()
            # De-Select
            ki.action( 'deselect' ).trigger()

            # Cycle
            for old_node in old_node_list:
                node_type = old_node.type()
                if str( node_type ) == "paintlayer":
                    # Variables
                    old_name = old_node.name()
                    new_name = f"Mirror Fix : { old_name }"
                    # Old Node
                    ad.setActiveNode( old_node )
                    self.Wait( ad )
                    # Mirror
                    if ( side == "LEFT" or side == "RIGHT" ):
                        ki.action( 'mirrorNodeX' ).trigger()
                    if ( side == "TOP" or side == "DOWN" ):
                        ki.action( 'mirrorNodeY' ).trigger()
                    self.Wait( ad )
                    # Re-Order
                    ki.action( 'move_layer_up' ).trigger()
                    self.Wait( ad )
                    # Merge ( this solves a alpha compositing issue )
                    ki.action( 'merge_layer' ).trigger()
                    self.Wait( ad )
                    # Merge
                    merge_node = ad.nodeByName( new_name )
                    self.Wait( ad )
                    ad.setActiveNode( merge_node )
                    self.Wait( ad )
                    merge_node.setName( old_name )
                    self.Wait( ad )

            # Warnning
            self.Message_Float( "MIRROR FIX", "END", self.icon_mirrorfix )
    def Wait( self, active_document ):
        active_document.waitForDone()
        active_document.refreshProjection()

    #endregion
    #region Color Picker ###########################################################

    # Module
    def Import_Pigment_O( self ):
        self.pigment_o_check = True
        widget = self.layout.color_picker
        widget.setEnabled( False )
        try:
            ki = Krita.instance()
            dockers = ki.dockers()
            for d in dockers:
                if d.objectName() == self.pigment_o_pyid:
                    # Variables
                    self.pigment_o_module = d
                    # Styling
                    widget.setEnabled( True )
                    self.layout.color_picker.setIcon( ki.icon( "krita_tool_ellipse" ) )
                    break
        except:
            pass
    # Ui
    def Show_Color_Picker( self ):
        if self.color_picker.isVisible() == False:
            self.Variables_Clean()
            self.Size_Update()
            self.Color_READ()
            self.color_picker.show()
        else:
            self.color_picker.hide()

    # Color Panel
    def Color_Panel_Preview( self, lista ):
        self.Color_Sliders_READ( lista[0], lista[1], lista[2] )
        self.Color_WRITE( self.wheel_space, self.s1, self.s2, self.s3, False )
    def Color_Panel_Apply( self, lista ):
        self.Color_Sliders_READ( lista[0], lista[1], lista[2] )
        self.Color_WRITE( self.wheel_space, self.s1, self.s2, self.s3, True )

    # Sliders Read
    def CS1_R( self, value ):
        self.s1 = value
        self.color_picker.s1.blockSignals( True )
        self.color_picker.s1.setValue( int( self.s1 * self.hue ) )
        self.color_picker.s1.blockSignals( False )
    def CS2_R( self, value ):
        self.s2 = value
        self.color_picker.s2.blockSignals( True )
        self.color_picker.s2.setValue( int( self.s2 * self.svl ) )
        self.color_picker.s2.blockSignals( False )
    def CS3_R( self, value ):
        self.s3 = value
        self.color_picker.s3.blockSignals( True )
        self.color_picker.s3.setValue( int( self.s3 * self.svl ) )
        self.color_picker.s3.blockSignals( False )
    def Color_Sliders_READ( self, s1, s2, s3 ):
        self.s1 = s1
        self.s2 = s2
        self.s3 = s3
        self.color_picker.s1.blockSignals( True )
        self.color_picker.s2.blockSignals( True )
        self.color_picker.s3.blockSignals( True )
        self.color_picker.s1.setValue( int( self.s1 * self.hue ) )
        self.color_picker.s2.setValue( int( self.s2 * self.svl ) )
        self.color_picker.s3.setValue( int( self.s3 * self.svl ) )
        self.color_picker.s1.blockSignals( False )
        self.color_picker.s2.blockSignals( False )
        self.color_picker.s3.blockSignals( False )
    # Sliders Write
    def CS1_W( self, action ):
        self.s1 = self.color_picker.s1.value() / self.hue
        self.Color_WRITE( self.wheel_space, self.s1, self.s2, self.s3, action )
    def CS2_W( self, action ):
        self.s2 = self.color_picker.s2.value() / self.svl
        self.Color_WRITE( self.wheel_space, self.s1, self.s2, self.s3, action )
    def CS3_W( self, action ):
        self.s3 = self.color_picker.s3.value() / self.svl
        self.Color_WRITE( self.wheel_space, self.s1, self.s2, self.s3, action )
    def Color_Sliders_WRITE( self, s1, s2, s3 ):
        self.s1 = s1 / self.hue
        self.s2 = s2 / self.svl
        self.s3 = s3 / self.svl
        self.Color_WRITE( self.wheel_space, self.s1, self.s2, self.s3 )

    # Read and Write
    def Color_READ( self ):
        if self.pigment_o_module != None:
            # Read
            self.cor = self.pigment_o_module.API_Request_FG()
            wheel_space = self.pigment_o_module.API_Request_Wheel_Space()

            # Wheel Space
            if wheel_space != self.wheel_space:
                # Variables
                self.wheel_space = wheel_space
                if self.pigment_o_module != None:
                    panel_path = self.directory_plugin.replace( "tela", "pigment_o\\PANEL")
                    zip_path = os.path.join( panel_path, f"RGB_{ self.wheel_space }_4.zip" )

                    # QPixmap List
                    self.qpixmap_list = self.Read_Zip( zip_path, self.wheel_space )
                    self.color_panel.Set_Background( self.qpixmap_list )

            # Variables
            hex6 = self.cor["hex6_d"]
            if self.wheel_space == "HSV":
                s1 = self.cor["hsv_1"]
                s2 = self.cor["hsv_2"]
                s3 = self.cor["hsv_3"]
            elif self.wheel_space == "HSL":
                s1 = self.cor["hsl_1"]
                s2 = self.cor["hsl_2"]
                s3 = self.cor["hsl_3"]
            elif self.wheel_space == "HCY":
                s1 = self.cor["hcy_1"]
                s2 = self.cor["hcy_2"]
                s3 = self.cor["hcy_3"]
            elif self.wheel_space == "ARD":
                s1 = self.cor["ard_1"]
                s2 = self.cor["ard_2"]
                s3 = self.cor["ard_3"]

            # Preview
            self.color_display.Set_Color( hex6 )
            # Panel
            self.color_panel.Set_Color( s1, s2, s3 )
            # Sliders
            self.Color_Sliders_READ( s1, s2, s3 )
    def Color_WRITE( self, wheel_space, s1, s2, s3, action=True ):
        if self.pigment_o_module != None:
            # Pigment.O
            self.pigment_o_module.API_Input_Kelvin( 6500 )
            if action == False:
                self.cor = self.pigment_o_module.API_Input_Preview( str( wheel_space ), float( s1 ), float( s2 ), float( s3 ), 0.0 )
            if action == True:
                self.cor = self.pigment_o_module.API_Input_Apply( str( wheel_space ), float( s1 ), float( s2 ), float( s3 ), 0.0 )
            # Update
            self.color_display.Set_Color( self.cor["hex6_d"] )
            self.color_panel.Set_Color( s1, s2, s3 )

    # Extras
    def Color_BlockSignals( self, boolean ):
        self.color_picker.color_display.blockSignals( boolean )
        self.color_picker.color_panel.blockSignals( boolean )
        self.color_picker.s1.blockSignals( boolean )
        self.color_picker.s2.blockSignals( boolean )
        self.color_picker.s3.blockSignals( boolean )
    def Read_Zip( self, location, space ):
        qpixmap_list = []
        try:
            if zipfile.is_zipfile( location ):
                archive = zipfile.ZipFile( location, "r" )
                for i in range( 0, self.hue+1 ):
                    # Mode Sensitive
                    name = f"{ space }_4_{ str( i ).zfill( 3 ) }.png"
                    # Read File
                    archive_open = archive.open( name )
                    archive_read = archive_open.read()
                    # Image
                    image = QImage()
                    image.loadFromData( archive_read )
                    qpixmap = QPixmap().fromImage( image )
                    qpixmap_list.append( qpixmap )
        except:
            try:QtCore.qDebug( f"Tela to Pigment.O | ERROR Zip failed" )
            except:pass
        return qpixmap_list

    #endregion
    #region Notifier ###############################################################

    def Application_Closing( self ):
        pass
    def Configuration_Changed( self ):
        pass
    def Image_Closed( self ):
        pass
    def Image_Created( self ):
        pass
    def Image_Saved( self ):
        pass
    def View_Closed( self ):
        self.Theme_Changed()
        self.Size_Update()
    def View_Created( self ):
        self.Theme_Changed()
        self.Size_Update()
    def Window_Created( self ):
        # Toolbox
        self.Toolbox_Display()

        # Signals
        self.window.activeViewChanged.connect( self.View_Changed )
        self.window.themeChanged.connect( self.Theme_Changed )
        self.window.windowClosed.connect( self.Window_Closed )

        # Buttons
        self.Toolbox_Button()
    def Window_IsBeingCreated( self ):
        pass

    # Window
    def View_Changed( self ):
        self.Variables_Clean()
        self.Theme_Changed()
    def Theme_Changed( self ):
        # Theme Highlight
        qcolor = QApplication.palette().highlight().color()

        # QPushbuttons
        self.Button_Highlight( self.layout.menu_vector,     "menu_vector",     qcolor )
        self.Button_Highlight( self.layout.menu_brush,      "menu_brush",      qcolor )
        self.Button_Highlight( self.layout.menu_transform,  "menu_transform",  qcolor )
        self.Button_Highlight( self.layout.menu_color,      "menu_color",      qcolor )
        self.Button_Highlight( self.layout.menu_overlay,    "menu_overlay",    qcolor )
        self.Button_Highlight( self.layout.menu_select,     "menu_select",     qcolor )
        self.Button_Highlight( self.layout.menu_camera,     "menu_camera",     qcolor )
        # non pressable buttons
        self.Button_Highlight( self.layout.menu_action,     "menu_action",     qcolor )
        self.Button_Highlight( self.layout.menu_view,       "menu_view",       qcolor )
        self.Button_Highlight( self.layout.mirror_fix,      "mirror_fix",      qcolor )
        self.Button_Highlight( self.layout.color_picker,    "color_picker",    qcolor )
    def Window_Closed( self ):
        try:self.Toolbox_Display()
        except:pass

    #endregion
    #region Widget Events ##########################################################

    def eventFilter( self, source, event ):
        # Enter
        if ( event.type() == 10 and source is self.layout ):
            self.Color_READ()
            self.Update_Tool()
            return True
        if ( event.type() == 10 and source is self.color_picker ):
            self.Color_READ()
            return True

        # Geometry
        if self.qmdiarea != None:
            if ( event.type() == 14 and source is self.qmdiarea):
                self.Size_Update()

        return super().eventFilter( source, event )

    #endregion
    #region Actions ################################################################

    def createActions(self, window):
        # Main Menu
        menu_tela = QtWidgets.QMenu( "tela_menu", window.qwindow() )
        action_tela = window.createAction( "tela_menu", "Tela", "tools/scripts" )
        action_tela.setMenu( menu_tela )
        # Sub Menus
        menu_mirror_fix = QtWidgets.QMenu( "mirror_fix_menu", window.qwindow() )
        action_mirror_fix = window.createAction( "mirror_fix_menu", "Mirror Fix", "tools/scripts/tela_menu" )
        action_mirror_fix.setMenu( menu_mirror_fix )

        # Actions Mirror Fix
        action_mirror_fix_left  = window.createAction( "tela_extension_mirror_fix_left",  "Mirror Fix - LEFT",  "tools/scripts/tela_menu/mirror_fix_menu" )
        action_mirror_fix_right = window.createAction( "tela_extension_mirror_fix_right", "Mirror Fix - RIGHT", "tools/scripts/tela_menu/mirror_fix_menu" )
        action_mirror_fix_top   = window.createAction( "tela_extension_mirror_fix_top",   "Mirror Fix - TOP",   "tools/scripts/tela_menu/mirror_fix_menu" )
        action_mirror_fix_down  = window.createAction( "tela_extension_mirror_fix_down",  "Mirror Fix - DOWN",  "tools/scripts/tela_menu/mirror_fix_menu" )
        action_mirror_fix_left.triggered.connect(  lambda: self.MirrorFix_Side( "LEFT" ) )
        action_mirror_fix_right.triggered.connect( lambda: self.MirrorFix_Side( "RIGHT" ) )
        action_mirror_fix_top.triggered.connect(   lambda: self.MirrorFix_Side( "TOP" ) )
        action_mirror_fix_down.triggered.connect(  lambda: self.MirrorFix_Side( "DOWN" ) )
        # Actions Picker
        action_picker_to_cursor = window.createAction( "tela_extension_picker_to_cursor", "Picker to Cursor", "tools/scripts/tela_menu" )
        action_picker_to_cursor.triggered.connect( self.Picker_to_Cursor )

    def Picker_to_Cursor( self ):
        check_canvas = self.Check_Canvas()
        if check_canvas == True:
            # Cursor
            position = QCursor().pos()
            cx = position.x()
            cy = position.y()
            # Canvas
            delta = self.qmdiarea.mapFromGlobal( QPoint( 0, 0 ) )
            dx = delta.x()
            dy = delta.y()
            # Widget
            widget = self.color_picker
            ww = widget.width()
            wh = widget.height()
            # Color Panel
            colorpanel = self.color_picker.color_panel
            cpx = colorpanel.x()
            cpy = colorpanel.y()
            cpw = colorpanel.width()
            cph = colorpanel.height()
            cp_cx = cpw * self.s2
            cp_cy = cph - cph * self.s3
            cp_cx = self.Limit_Range( int( cp_cx ), 0, cpw, 0, -1 )
            cp_cy = self.Limit_Range( int( cp_cy ), 0, cph, 0, -1 )

            # Relocate Color Picker
            self.Picker_Geometry( cx+dx-cpx-cp_cx, cy+dy-cpy-cp_cy, ww, wh )
            # Toggle Visibility
            check_visible = self.color_picker.isVisible()
            if check_visible == False:
                self.color_picker.setVisible( True )
            else:
                self.color_picker.setVisible( False )

    #endregion
    #region Notes ##################################################################

    """
    # Label Message
    self.layout.label.setText( "message" )

    # Pop Up Message
    QMessageBox.information( QWidget(), i18n( "Warnning" ), i18n( "message" ) )

    # Log Viewer Message
    QtCore.qDebug( f"value = { value }" )
    QtCore.qDebug( "message" )
    QtCore.qWarning( "message" )
    QtCore.qCritical( "message" )

    """

    """
    # self.setWindowFlags( QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint )
    """

    """
    QTimer.singleShot( 0, lambda: self.MirrorFix_Invert( ki, ad, side, new_node ) )
    """
    #endregion


