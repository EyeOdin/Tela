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

# Krita Module
from krita import *
# PyQt5 Modules
from PyQt5 import QtWidgets, QtCore, QtGui, uic

#endregion
#region Global Variables ###########################################################

# Plugin
DOCKER_NAME = "Tela"
tela_version = "2024_01_23"

#endregion


class Tela_Docker( DockWidget ):
    """
    Tela ToolBox
    """

    #region Initialize #############################################################

    def __init__( self ):
        super( Tela_Docker, self ).__init__()
        self.User_Interface()
        self.Variables()
        self.Connections()
        self.Modules()
        self.Style()

    def User_Interface( self ):
        # Window
        self.setWindowTitle( DOCKER_NAME )

        # Operating System
        self.OS = str( QSysInfo.kernelType() ) # WINDOWS=winnt & LINUX=linux
        if self.OS == 'winnt': # Unlocks icons in Krita for Menu Mode
            QApplication.setAttribute( Qt.AA_DontShowIconsInMenus, False )

        # Path Name
        self.directory_plugin = str( os.path.dirname( os.path.realpath( __file__ ) ) )

        # Widget Docker
        self.layout = uic.loadUi( os.path.join( self.directory_plugin, "tela_docker.ui" ), QDialog( self ) )
    def Variables( self ):
        # System
        ki = Krita.instance()
        self.stacked_widget = None
        self.qmdiarea = None

        # Toolbox ( name, pykrita, qicon )
        self.tool = {
            "vector" : {
                "select_tool"        : [ "Select",        "InteractionTool",                   ki.icon( "select" )                      ],
                "text_tool"          : [ "Text",          "SvgTextTool",                       ki.icon( "draw-text" )                   ],
                "edit_tool"          : [ "Edit",          "PathTool",                          ki.icon( "shape_handling" )              ],
                "calligraphy_tool"   : [ "Calligraphy",   "KarbonCalligraphyTool",             ki.icon( "calligraphy" )                 ],
                },
            "brush" : {
                "freehand_brush"     : [ "Freehand",      "KritaShape/KisToolBrush",           ki.icon( "krita_tool_freehand" )         ],
                "line_brush"         : [ "Line",          "KritaShape/KisToolLine",            ki.icon( "krita_tool_line" )             ],
                "rectangle_brush"    : [ "Rectangle",     "KritaShape/KisToolRectangle",       ki.icon( "krita_tool_rectangle" )        ],
                "ellipse_brush"      : [ "Ellipse",       "KritaShape/KisToolEllipse",         ki.icon( "krita_tool_ellipse" )          ],
                "polygon_brush"      : [ "Polygon",       "KisToolPolygon",                    ki.icon( "krita_tool_polygon" )          ],
                "polyline_brush"     : [ "Polyline",      "KisToolPolyline",                   ki.icon( "polyline" )                    ],
                "bezier_brush"       : [ "Bezier",        "KisToolPath",                       ki.icon( "krita_draw_path" )             ],
                "path_brush"         : [ "Path",          "KisToolPencil",                     ki.icon( "krita_tool_freehandvector" )   ],
                "dynamic_brush"      : [ "Dynamic",       "KritaShape/KisToolDyna",            ki.icon( "krita_tool_dyna" )             ],
                "multi_brush"        : [ "Multibrush",    "KritaShape/KisToolMultiBrush",      ki.icon( "krita_tool_multihand" )        ],
                },
            "transform" : {
                "transform_tool"     : [ "Transform",     "KisToolTransform",                  ki.icon( "krita_tool_transform" )        ],
                "move_tool"          : [ "Move",          "KritaTransform/KisToolMove",        ki.icon( "krita_tool_move" )             ],
                "crop_tool"          : [ "Crop",          "KisToolCrop",                       ki.icon( "tool_crop" )                   ],
                },
            "color" : {
                "gradient_tool"      : [ "Gradient",      "KritaFill/KisToolGradient",         ki.icon( "krita_tool_gradient" )         ],
                "sampler_tool"       : [ "Sampler",       "KritaSelected/KisToolColorSampler", ki.icon( "krita_tool_color_sampler" )    ],
                "colorize_tool"      : [ "Colorize",      "KritaShape/KisToolLazyBrush",       ki.icon( "krita_tool_lazybrush" )        ],
                "patch_tool"         : [ "Patch",         "KritaShape/KisToolSmartPatch",      ki.icon( "krita_tool_smart_patch" )      ],
                "fill_tool"          : [ "Fill",          "KritaFill/KisToolFill",             ki.icon( "krita_tool_color_fill" )       ],
                "enclose_tool"       : [ "Enclose",       "KisToolEncloseAndFill",             ki.icon( "krita_tool_enclose_and_fill" ) ],
                },
            "overlay" : {
                "assistant_tool"     : [ "Assistant",     "KisAssistantTool",                  ki.icon( "krita_tool_assistant" )        ],
                "measure_tool"       : [ "Measure",       "KritaShape/KisToolMeasure",         ki.icon( "krita_tool_measure" )          ],
                "reference_tool"     : [ "Reference",     "ToolReferenceImages",               ki.icon( "krita_tool_reference_images" ) ],
                },
            "select" : {
                "rectangle_select"   : [ "Rectangle",     "KisToolSelectRectangular",          ki.icon( "tool_rect_selection" )         ],
                "elliptical_select"  : [ "Elliptical",    "KisToolSelectElliptical",           ki.icon( "tool_elliptical_selection" )   ],
                "polygon_select"     : [ "Polygon",       "KisToolSelectPolygonal",            ki.icon( "tool_polygonal_selection" )    ],
                "freehand_select"    : [ "Freehand",      "KisToolSelectOutline",              ki.icon( "tool_outline_selection")       ],
                "contiguous_select"  : [ "Contiguous",    "KisToolSelectContiguous",           ki.icon( "tool_contiguous_selection" )   ],
                "color_select"       : [ "Color",         "KisToolSelectSimilar",              ki.icon( "tool_similar_selection")       ],
                "bezier_select"      : [ "Bezier",        "KisToolSelectPath",                 ki.icon( "tool_path_selection")          ],
                "magnetic_select"    : [ "Magnetic",      "KisToolSelectMagnetic",             ki.icon( "tool_magnetic_selection" )     ],
                },
            "camera" : {
                "zoom_tool"          : [ "Zoom",          "ZoomTool",                          ki.icon( "tool_zoom" )                   ],
                "pan_tool"           : [ "Pan",           "PanTool",                           ki.icon( "tool_pan" )                    ],
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

        # Menu Margin
        self.mx = 10
        self.my = 10
    def Connections( self ):
        #region Toolbox

        self.layout.menu_vector.clicked.connect( self.Tool_Vector )
        self.layout.menu_brush.clicked.connect( self.Tool_Brush )
        self.layout.menu_transform.clicked.connect( self.Tool_Transform )
        self.layout.menu_color.clicked.connect( self.Tool_Color )
        self.layout.menu_overlay.clicked.connect( self.Tool_Overlay )
        self.layout.menu_select.clicked.connect( self.Tool_Select )
        self.layout.menu_camera.clicked.connect( self.Tool_Camera )

        #endregion
        #region Event Filters

        # Menu
        self.layout.menu_vector.installEventFilter( self )
        self.layout.menu_brush.installEventFilter( self )
        self.layout.menu_transform.installEventFilter( self )
        self.layout.menu_color.installEventFilter( self )
        self.layout.menu_overlay.installEventFilter( self )
        self.layout.menu_select.installEventFilter( self )
        self.layout.menu_camera.installEventFilter( self )

        #endregion
    def Modules( self ):
        # Notifier
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
    def Style( self ):
        # Icon Initialize
        self.layout.menu_vector.setIcon(    self.tool["vector"]["select_tool"][2]       )
        self.layout.menu_brush.setIcon(     self.tool["brush"]["freehand_brush"][2]     )
        self.layout.menu_transform.setIcon( self.tool["transform"]["transform_tool"][2] )
        self.layout.menu_color.setIcon(     self.tool["color"]["sampler_tool"][2]       )
        self.layout.menu_overlay.setIcon(   self.tool["overlay"]["reference_tool"][2]   )
        self.layout.menu_select.setIcon(    self.tool["select"]["freehand_select"][2]   )
        self.layout.menu_camera.setIcon(    self.tool["camera"]["pan_tool"][2]          )

    #endregion
    #region Management #############################################################

    def Size_Update( self ):
        if self.qmdiarea != None:
            w = self.qmdiarea.width()
            h = self.qmdiarea.height()
            pw = self.layout.width()
            ph = self.layout.height()
            px = w * 0.5 - pw * 0.5
            py = h - 70
            self.layout.setGeometry( int( px ), int( py ), int( pw ), int( ph ) )

    #endregion
    #region ToolBox ################################################################

    def Tool_Vector( self ):
        Krita.instance().action( self.operation["vector"] ).trigger()
    def Tool_Brush( self ):
        Krita.instance().action( self.operation["brush"] ).trigger()
    def Tool_Transform( self ):
        Krita.instance().action( self.operation["transform"] ).trigger()
    def Tool_Color( self ):
        Krita.instance().action( self.operation["color"] ).trigger()
    def Tool_Overlay( self ):
        Krita.instance().action( self.operation["overlay"] ).trigger()
    def Tool_Select( self ):
        Krita.instance().action( self.operation["select"] ).trigger()
    def Tool_Camera( self ):
        Krita.instance().action( self.operation["camera"] ).trigger()

    #endregion
    #region Menu Signals ###########################################################

    def Menu_Vector( self, event ):
        self.Tool_Menu( "vector", self.layout.menu_vector )
    def Menu_Brush( self, event ):
        self.Tool_Menu( "brush", self.layout.menu_brush )
    def Menu_Transform( self, event ):
        self.Tool_Menu( "transform", self.layout.menu_transform )
    def Menu_Color( self, event ):
        self.Tool_Menu( "color", self.layout.menu_color )
    def Menu_Overlay( self, event ):
        self.Tool_Menu( "overlay", self.layout.menu_overlay )
    def Menu_Select( self, event ):
        self.Tool_Menu( "select", self.layout.menu_select )
    def Menu_Camera( self, event ):
        self.Tool_Menu( "camera", self.layout.menu_camera )

    def Tool_Menu( self, mode, widget ):
        # Variables
        ki = Krita.instance()
        key = list( self.tool[mode].keys() )
        len_key = len( key )

        # Menu
        qmenu = QMenu( self )

        # Tool
        action_menu = []
        for k in key:
            string = self.tool[mode][k][0]
            qicon = self.tool[mode][k][2]
            action_menu.append( QAction( qicon, string ) )
        qmenu.addActions( action_menu )

        # Mapping
        height = 23 * len_key  # 23 is the expected height of a qmenu item on windows at least
        qpoint = widget.geometry().topLeft()
        pos = self.layout.tool_box.mapToGlobal( qpoint )
        point = QPoint( pos.x(), pos.y() - self.my - height )
        action = qmenu.exec_( point )

        # Pin
        if action in action_menu:
            # Variables
            index = action_menu.index( action )
            k = key[index]
            operation = self.tool[mode][k][1]
            qicon = self.tool[mode][k][2]
            # Tool
            Krita.instance().action( operation ).trigger()
            self.operation[mode] = operation
            # UI
            widget.setIcon( qicon )

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
        self.Size_Update()
    def View_Created( self ):
        self.Size_Update()
    def Window_Created( self ):
        # Window
        self.window = Krita.instance().activeWindow()
        # Main Window
        self.stacked_widget = self.window.qwindow().centralWidget()
        self.qmdiarea = self.stacked_widget.findChild( QMdiArea )
        self.qmdiarea.installEventFilter( self )
        # Display
        self.layout.setParent( self.qmdiarea )
        self.layout.show()
        self.hide()
    def Window_IsBeingCreated( self ):
        pass

    #endregion
    #region Widget Events ##########################################################

    def eventFilter( self, source, event ):
        # ToolBox
        if ( event.type() == 82 and source is self.layout.menu_vector ):
            self.Menu_Vector( event )
            return True
        if ( event.type() == 82 and source is self.layout.menu_brush ):
            self.Menu_Brush( event )
            return True
        if ( event.type() == 82 and source is self.layout.menu_transform ):
            self.Menu_Transform( event )
            return True
        if ( event.type() == 82 and source is self.layout.menu_color ):
            self.Menu_Color( event )
            return True
        if ( event.type() == 82 and source is self.layout.menu_overlay ):
            self.Menu_Overlay( event )
            return True
        if ( event.type() == 82 and source is self.layout.menu_select ):
            self.Menu_Select( event )
            return True
        if ( event.type() == 82 and source is self.layout.menu_camera ):
            self.Menu_Camera( event )
            return True

        # Geometry
        if self.qmdiarea != None:
            if ( event.type() == 14 and source is self.qmdiarea ):
                self.Size_Update()

        return super().eventFilter( source, event )

    #endregion
    #region Change Canvas ##########################################################

    def canvasChanged( self, canvas ):
        self.Size_Update()

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

    #endregion
