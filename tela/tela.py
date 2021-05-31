#\\ Import Modules #############################################################
# Python Modules
import os
import math
# Krita Modules
from krita import *
# PyQt5 Modules
from PyQt5 import Qt, QtWidgets, QtCore, QtGui, QtSvg, uic
from PyQt5.Qt import Qt
# Pigment.O Modules
from .tela_modulo import (
    Channel_Slider,
    Clicks,
    Panel_Canvas,
    Panel_View,
    )

#//
#\\ Global Variables ###########################################################
# Set Window Title Name
DOCKER_NAME = "Tela"
# Timer
check_timer = 60  # 1000 = 1 SECOND (Zero will Disable checks)
# Pigment.O Version Date
tela_version = "2021_05_16"
# Numbers
zero = 0.0
half = 0.5
unit = 1.0
two = 2.0
max_val = 16777215
# UI variables
ui_5 = 5
ui_10 = 10
ui_15 = 15
ui_17 = 17
ui_20 = 20
ui_25 = 25
ui_30 = 30
ui_35 = 35
ui_40 = 40
ui_45 = 45
ui_47 = 47
ui_50 = 50
ui_55 = 55
ui_60 = 60
ui_65 = 65
ui_70 = 70
# View Constants
k_rotation = 360
k_zoom = 10
k_size = 1000
k_opacity = 100
k_flow = 100
k_exposure = 10
k_gamma = 5
# Units
u_zoom = 0.2
u_exposure = 0.1
u_gamma = 0.1
# SOF Initial Values
i_size = 40
i_opacity = 1
i_flow = 1
# Color Reference
bg_unseen = str("background-color: rgba(0,0,0,0);")
bg_alpha = str("background-color: rgba(0, 0, 0, 50); ")

#//


class TelaDocker(DockWidget):
    """
    Quick settings
    """

    #\\ Initialize The Docker Window ###########################################
    def __init__(self):
        super(TelaDocker, self).__init__()

        # Construct
        self.Variables()
        self.User_Interface()

        # Modules and Connections
        self.Connects()
        self.Style_Widget()
        self.Clock()

        # Settings
        self.Version_Settings()

    def Variables(self):
        self.sync = False # Ensures no overlapping sync cycles
        self.mode = "Canvas"
        self.eraser = False
        # Canvas
        self.can_rotation = 0.000
        self.can_zoom = 1.000
        self.dpi = 1
        self.can_mirror = False
        self.can_wrap = False
        # Document
        self.doc_width = 0
        self.doc_height = 0
        self.doc_resolution = 0
        self.doc_ref = [None, None]
        self.delta_old = [0,0,0,0]
        self.delta_new = [0,0,0,0]
        self.gui_hor_norm = []
        self.gui_hor_dif = None
        self.gui_hor_index = [None, None]
        self.gui_hor_previous = []
        self.gui_ver_norm = []
        self.gui_ver_dif = None
        self.gui_ver_index = [None, None]
        self.gui_ver_previous = []
        # View
        self.sof_1_lock = i_size
        self.sof_2_lock = i_opacity
        self.sof_3_lock = i_flow
        self.sof_1 = i_size
        self.sof_2 = i_opacity
        self.sof_3 = i_flow
        self.hdr_e = 0
        self.hdr_g = 1
        self.vie_blend = "..."
        # UI checks
        self.ui_d_ref = False
        self.ui_g_mirror = False # Original does not need to Check
        self.ui_g_sort = False # Original does not need to Check
        self.ui_g_visible = False
        self.ui_g_lock = False
    def User_Interface(self):
        # Path Name
        self.dir_name = str(os.path.dirname(os.path.realpath(__file__)))
        # Window Title
        self.setWindowTitle(DOCKER_NAME)
        # Tela Widget
        self.window = QWidget()
        self.layout = uic.loadUi(self.dir_name + '/tela.ui', self.window)
        self.setWidget(self.window)
        # Theme Variables
        self.krita_value = 59
        self.krita_contrast = 196
        self.gray_natural = self.HEX_6string(self.krita_value/255,self.krita_value/255,self.krita_value/255)
        self.gray_contrast = self.HEX_6string(self.krita_contrast/255,self.krita_contrast/255,self.krita_contrast/255)
    def Connects(self):
        #\\ MENU ###############################################################
        self.layout.menu.currentTextChanged.connect(self.Menu_Display)
        self.layout.check.stateChanged.connect(self.Krita_TIMER)

        #//
        #\\ CANVAS #############################################################
        # Panel Canvas
        self.panel_canvas = Panel_Canvas(self.layout.panel_canvas)
        self.panel_canvas.SIGNAL_CANVAS.connect(self.CANVAS_Signal)
        # Range
        self.layout.can_rotation_value.setMinimum(zero)
        self.layout.can_zoom_value.setMinimum(zero)
        self.layout.can_rotation_value.setMaximum(k_rotation)
        self.layout.can_zoom_value.setMaximum(k_zoom)
        # Module
        self.can_rotation_slider = Channel_Slider(self.layout.can_rotation_slider)
        self.can_zoom_slider = Channel_Slider(self.layout.can_zoom_slider)
        self.can_rotation_slider.Channel("ROTATION")
        self.can_zoom_slider.Channel("ZOOM")
        # ROTATION
        self.can_rotation_slider.SIGNAL_HALF.connect(self.CANVAS_Rotation_RESET)
        self.can_rotation_slider.SIGNAL_MINUS.connect(self.CANVAS_Rotation_Minus)
        self.can_rotation_slider.SIGNAL_PLUS.connect(self.CANVAS_Rotation_Plus)
        self.can_rotation_slider.SIGNAL_VALUE.connect(self.CANVAS_Rotation_Slider_Modify)
        self.layout.can_rotation_value.valueChanged.connect(self.CANVAS_Rotation_Value_Modify)
        # ZOOM
        self.can_zoom_slider.SIGNAL_HALF.connect(self.CANVAS_Zoom_RESET)
        self.can_zoom_slider.SIGNAL_MINUS.connect(self.CANVAS_Zoom_Minus)
        self.can_zoom_slider.SIGNAL_PLUS.connect(self.CANVAS_Zoom_Plus)
        self.can_zoom_slider.SIGNAL_VALUE.connect(self.CANVAS_Zoom_Slider_Modify)
        self.layout.can_zoom_value.valueChanged.connect(self.CANVAS_Zoom_Value_Modify)
        # Check Boxes
        self.layout.can_mirror.toggled.connect(self.CANVAS_Mirror_TOGGLE)
        self.layout.can_wrap.toggled.connect(self.CANVAS_Wrap_TOGGLE)

        #//
        #\\ DOCUMENT ###########################################################
        # Document
        self.layout.doc_width.editingFinished.connect(self.DOC_Width_WRITE)
        self.layout.doc_height.editingFinished.connect(self.DOC_Height_WRITE)
        self.layout.doc_resolution.editingFinished.connect(self.DOC_Resolution_WRITE)
        # Delta Document
        self.layout.doc_delta_reference.toggled.connect(self.GUIDES_Delta_Reference)
        self.layout.doc_delta_up.valueChanged.connect(self.GUIDES_Delta)
        self.layout.doc_delta_left.valueChanged.connect(self.GUIDES_Delta)
        self.layout.doc_delta_right.valueChanged.connect(self.GUIDES_Delta)
        self.layout.doc_delta_down.valueChanged.connect(self.GUIDES_Delta)
        # Guides
        self.layout.gui_horizontal_group.itemDoubleClicked.connect(self.GUIDES_Horizontal_EDIT)
        self.layout.gui_vertical_group.itemDoubleClicked.connect(self.GUIDES_Vertical_EDIT)
        # Guides Status
        self.layout.gui_mirror.toggled.connect(self.GUIDES_Mirror)
        self.layout.gui_sort.toggled.connect(self.GUIDES_Sort)
        self.layout.gui_visible.toggled.connect(self.GUIDES_Visible_WRITE)
        self.layout.gui_lock.toggled.connect(self.GUIDES_Lock_WRITE)

        #//
        #\\ VIEW ###############################################################
        # Panel
        self.panel_view = Panel_View(self.layout.panel_view)
        self.panel_view.SIGNAL_VIEW.connect(self.VIEW_Signal)

        # Blend
        self.layout.brush_blend.returnPressed.connect(self.BLEND_WRITE)

        # Range
        self.layout.sof_1_value.setMinimum(zero)
        self.layout.sof_2_value.setMinimum(zero)
        self.layout.sof_3_value.setMinimum(zero)
        self.layout.sof_1_value.setMaximum(k_size)
        self.layout.sof_2_value.setMaximum(k_opacity)
        self.layout.sof_3_value.setMaximum(k_flow)
        # Module
        self.sof_1_slider = Channel_Slider(self.layout.sof_1_slider)
        self.sof_2_slider = Channel_Slider(self.layout.sof_2_slider)
        self.sof_3_slider = Channel_Slider(self.layout.sof_3_slider)
        self.sof_1_slider.Channel("SIZE")
        self.sof_2_slider.Channel("OPACITY")
        self.sof_3_slider.Channel("FLOW")
        # SIZE
        self.sof_1_slider.SIGNAL_HALF.connect(lambda: self.SOF_1_READ(self.sof_1_lock))
        self.sof_1_slider.SIGNAL_MINUS.connect(self.SOF_1_Minus)
        self.sof_1_slider.SIGNAL_PLUS.connect(self.SOF_1_Plus)
        self.sof_1_slider.SIGNAL_VALUE.connect(self.SOF_1_Slider_Modify)
        self.layout.sof_1_value.valueChanged.connect(self.SOF_1_Value_Modify)
        # OPACITY
        self.sof_2_slider.SIGNAL_HALF.connect(lambda: self.SOF_2_READ(self.sof_2_lock))
        self.sof_2_slider.SIGNAL_MINUS.connect(self.SOF_2_Minus)
        self.sof_2_slider.SIGNAL_PLUS.connect(self.SOF_2_Plus)
        self.sof_2_slider.SIGNAL_VALUE.connect(self.SOF_2_Slider_Modify)
        self.layout.sof_2_value.valueChanged.connect(self.SOF_2_Value_Modify)
        # FLOW
        self.sof_3_slider.SIGNAL_HALF.connect(lambda: self.SOF_3_READ(self.sof_3_lock))
        self.sof_3_slider.SIGNAL_MINUS.connect(self.SOF_3_Minus)
        self.sof_3_slider.SIGNAL_PLUS.connect(self.SOF_3_Plus)
        self.sof_3_slider.SIGNAL_VALUE.connect(self.SOF_3_Slider_Modify)
        self.layout.sof_3_value.valueChanged.connect(self.SOF_3_Value_Modify)
        # Tip
        self.sof_n = Clicks(self.layout.sof_n)
        self.sof_n.SIGNAL_APPLY.connect(self.SOF_Lock_APPLY)
        self.sof_n.SIGNAL_SAVE.connect(self.SOF_Lock_SAVE)
        self.sof_n.SIGNAL_CLEAN.connect(self.SOF_Lock_CLEAN)

        # Range
        self.layout.hdr_e_value.setMinimum(-k_exposure)
        self.layout.hdr_g_value.setMinimum(0)
        self.layout.hdr_e_value.setMaximum(k_exposure)
        self.layout.hdr_g_value.setMaximum(k_gamma)
        # Module
        self.hdr_e_slider = Channel_Slider(self.layout.hdr_e_slider)
        self.hdr_g_slider = Channel_Slider(self.layout.hdr_g_slider)
        self.hdr_e_slider.Channel("EXPOSURE")
        self.hdr_g_slider.Channel("GAMMA")
        # EXPOSURE
        self.hdr_e_slider.SIGNAL_HALF.connect(self.HDR_E_RESET)
        self.hdr_e_slider.SIGNAL_MINUS.connect(self.HDR_E_Minus)
        self.hdr_e_slider.SIGNAL_PLUS.connect(self.HDR_E_Plus)
        self.hdr_e_slider.SIGNAL_VALUE.connect(self.HDR_E_Slider_Modify)
        self.layout.hdr_e_value.valueChanged.connect(self.HDR_E_Value_Modify)
        # GAMMA
        self.hdr_g_slider.SIGNAL_HALF.connect(self.HDR_G_RESET)
        self.hdr_g_slider.SIGNAL_MINUS.connect(self.HDR_G_Minus)
        self.hdr_g_slider.SIGNAL_PLUS.connect(self.HDR_G_Plus)
        self.hdr_g_slider.SIGNAL_VALUE.connect(self.HDR_G_Slider_Modify)
        self.layout.hdr_g_value.valueChanged.connect(self.HDR_G_Value_Modify)

        #//
    def Style_Widget(self):
        # CANVAS
        self.layout.panel_canvas.setStyleSheet(bg_alpha)
        self.layout.can_rotation_slider.setStyleSheet(bg_alpha)
        self.layout.can_zoom_slider.setStyleSheet(bg_alpha)
        # DOCUMENT
        # VIEW
        self.layout.panel_view.setStyleSheet(bg_alpha)
        self.layout.sof_n.setStyleSheet(bg_alpha)
        self.layout.sof_1_slider.setStyleSheet(bg_alpha)
        self.layout.sof_2_slider.setStyleSheet(bg_alpha)
        self.layout.sof_3_slider.setStyleSheet(bg_alpha)
        self.layout.hdr_e_slider.setStyleSheet(bg_alpha)
        self.layout.hdr_g_slider.setStyleSheet(bg_alpha)
    def Clock(self):
        # Start Timer and Connect Switch
        if check_timer >= 1:
            self.timer = QtCore.QTimer(self)
            self.timer.timeout.connect(self.Krita_2_Tela)
            self.timer.start(check_timer)
            # Method ON/OFF switch boot
            self.layout.check.setCheckState(1)
            self.Krita_TIMER()
            # Stop Timer so it does work without the Docker Present
            self.timer.stop()

    #//
    #\\ Krita & Tela ###########################################################
    def Krita_TIMER(self):
        font = self.layout.check.font()
        self.timer_state = self.layout.check.checkState()
        if check_timer >= 1:
            if self.timer_state == 0:
                font.setBold(False)
                self.layout.check.setText("OFF")
                self.timer.stop()
            elif self.timer_state == 1:
                font.setBold(True)
                self.layout.check.setText("ON")
                self.Krita_2_Tela()
                self.timer.start()
            elif self.timer_state == 2:
                self.layout.check.setCheckState(0)
        else:
            font.setBold(False)
            self.layout.check.setText("C<1")
            self.layout.check.setEnabled(False)
        self.layout.check.setFont(font)
    def Krita_2_Tela(self):
        if self.sync == False:
            # Sync Control Variable
            self.sync = True
            # Check current Theme color Value (0-255)
            krita_value = QApplication.palette().color(QPalette.Window).value()
            if self.krita_value != krita_value:
                # Update System Variable
                self.krita_value = krita_value
                # Contrast Gray Calculation
                self.krita_contrast = self.gc(krita_value/255, krita_value/255, krita_value/255) * 255
                # RGB Code of contrast Gray
                self.gray_natural = self.HEX_6string(self.krita_value,self.krita_value,self.krita_value)
                self.gray_contrast = self.HEX_6string(self.krita_contrast,self.krita_contrast,self.krita_contrast)
                # Update Docker
                self.update()

            # Read Values
            if ((self.canvas() is not None) and (self.canvas().view() is not None)):
                # Eraser
                self.eraser = Application.action("erase_action").isChecked()

                # Krita instance Classes
                c = Krita.instance().activeWindow().activeView().canvas()
                ad = Krita.instance().activeDocument()
                av = Krita.instance().activeWindow().activeView()

                # Check and Update Classes
                if (self.mode == "Canvas" or self.mode == "Document"):
                    # Read Document
                    doc_width = ad.width()
                    doc_height = ad.height()
                    doc_resolution = ad.resolution()
                    gui_hor = ad.horizontalGuides()
                    gui_ver = ad.verticalGuides()
                    ui_g_visible = ad.guidesVisible()
                    ui_g_lock = ad.guidesLocked()
                    # Read Canvas
                    can_rotation = round(self.Rotation_Recieve(c.rotation()), 3)
                    can_zoom = round(self.Zoom_Recieve(c.zoomLevel(), doc_resolution), 3)
                    can_mirror = c.mirror()
                    can_wrap = c.wrapAroundMode()
                    # Update Canvas
                    if self.can_rotation != can_rotation:
                        self.CANVAS_Rotation_READ(can_rotation)
                    if self.can_zoom != can_zoom:
                        self.CANVAS_Zoom_READ(can_zoom)
                    if self.can_mirror != can_mirror:
                        self.CANVAS_Mirror_READ(can_mirror)
                    if self.can_wrap != can_wrap:
                        self.CANVAS_Wrap_READ(can_wrap)
                    # Guides Float percision error correction
                    for i in range(0, len(gui_hor)):
                        gui_hor[i] = round(gui_hor[i], 5)
                    for i in range(0, len(gui_ver)):
                        gui_ver[i] = round(gui_ver[i], 5)
                    # Update Document
                    if self.doc_width != doc_width:
                        self.DOC_Width_READ(doc_width)
                    if self.doc_height != doc_height:
                        self.DOC_Height_READ(doc_height)
                    if self.doc_resolution != doc_resolution:
                        self.DOC_Resolution_READ(doc_resolution)
                    if self.gui_hor_previous != gui_hor:
                        self.gui_hor_norm = gui_hor
                        if self.ui_d_ref == True:
                            self.GUIDES_Horizontal_LIST_REF()
                            pass
                        else:
                            self.GUIDES_Horizontal_LIST_NOR()
                        self.gui_hor_previous = self.gui_hor_norm
                    if self.gui_ver_previous != gui_ver:
                        self.gui_ver_norm = gui_ver
                        if self.ui_d_ref == True:
                            self.GUIDES_Vertical_LIST_REF()
                            pass
                        else:
                            self.GUIDES_Vertical_LIST_NOR()
                        self.gui_ver_previous = self.gui_ver_norm
                    if self.ui_g_visible != ui_g_visible:
                        self.GUIDES_Visible_READ(ui_g_visible)
                    if self.ui_g_lock != ui_g_lock:
                        self.GUIDES_Lock_READ(ui_g_lock)
                if self.mode == "View":
                    # Read
                    vie_size = av.brushSize()
                    vie_opacity = av.paintingOpacity()
                    vie_flow = av.paintingFlow()
                    vie_exposure = av.HDRExposure()
                    vie_gamma = av.HDRGamma()
                    vie_blend = av.currentBlendingMode()
                    # Update
                    if self.sof_1 != vie_size:
                        self.SOF_1_READ(vie_size)
                    if self.sof_2 != vie_opacity:
                        self.SOF_2_READ(vie_opacity)
                    if self.sof_3 != vie_flow:
                        self.SOF_3_READ(vie_flow)
                    if self.hdr_e != vie_exposure:
                        self.HDR_E_READ(vie_exposure)
                    if self.hdr_g != vie_gamma:
                        self.HDR_G_READ(vie_gamma)
                    if self.vie_blend != vie_blend:
                        self.BLEND_READ(vie_blend)
            else:
                self.eraser = False
                if self.mode == "Canvas":
                    if self.can_rotation != 0:
                        self.CANVAS_Rotation_READ(0)
                    if self.can_zoom != 1:
                        self.CANVAS_Zoom_READ(1)
                    if self.can_mirror != 0:
                        self.CANVAS_Mirror_READ(0)
                    if self.can_wrap != 0:
                        self.CANVAS_Wrap_READ(0)
                if self.mode == "Document":
                    if self.doc_width != 0:
                        self.DOC_Width_READ(0)
                    if self.doc_height != 0:
                        self.DOC_Height_READ(0)
                    if self.doc_resolution != 0:
                        self.DOC_Resolution_READ(0)
                    if self.ui_d_ref == True:
                        self.GUIDES_Delta_Reference()
                    if self.gui_hor_previous != None:
                        self.gui_hor_previous = [None]
                        self.gui_hor_index = [None, None]
                        self.layout.gui_horizontal_group.clear()
                    if self.gui_ver_previous != None:
                        self.gui_ver_previous = [None]
                        self.gui_ver_index = [None, None]
                        self.layout.gui_vertical_group.clear()
                    if self.ui_g_sort == True:
                        self.layout.gui_sort.setChecked(False)
                    if self.ui_g_mirror == True:
                        self.layout.gui_mirror.setChecked(False)
                    if self.ui_g_visible != 0:
                        self.GUIDES_Visible_READ(0)
                    if self.ui_g_lock != 0:
                        self.GUIDES_Lock_READ(0)
                if self.mode == "View":
                    if self.sof_1 != 40:
                        self.SOF_1_READ(40)
                    if self.sof_2 != 100:
                        self.SOF_2_READ(100)
                    if self.sof_3 != 100:
                        self.SOF_3_READ(100)
                    if self.hdr_e != 0:
                        self.HDR_E_RESET()
                    if self.hdr_g != 1:
                        self.HDR_G_RESET()
                    if self.vie_blend != "...":
                        self.BLEND_READ("...")

            # Panel Update
            self.Panel_Update()
            # Sync Control Variable
            self.sync = False
    def Panel_Update(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            if self.mode == "Canvas":
                self.panel_canvas.Update_Panel(
                    self.eraser,
                    self.can_rotation, self.can_zoom,
                    self.doc_width, self.doc_height,
                    self.ui_d_ref, self.delta_new,
                    self.gui_hor_norm, self.gui_ver_norm,
                    self.layout.panel_canvas.width(), self.layout.panel_canvas.height(), # reduntdant
                    self.gray_natural, self.gray_contrast,
                    )
                self.layout.panel_canvas.update()
            if self.mode == "View":
                self.panel_view.Update_Panel(
                    self.eraser,
                    self.sof_1, self.sof_2, self.sof_3,
                    self.hdr_e, self.hdr_g,
                    self.layout.panel_view.width(), self.layout.panel_view.height(),
                    self.gray_natural, self.gray_contrast
                    )
                self.layout.panel_view.update()
        else:
            if self.mode == "Canvas":
                self.panel_canvas.Update_Panel(
                    False,
                    0, 1,
                    1, 1,
                    [], [],
                    [], [],
                    self.layout.panel_canvas.width(), self.layout.panel_canvas.height(), # reduntdant
                    self.gray_natural, self.gray_contrast,
                    )
                self.layout.panel_canvas.update()
            if self.mode == "View":
                self.panel_view.Update_Panel(
                    False,
                    self.sof_1_lock, self.sof_2_lock, self.sof_3_lock,
                    self.hdr_e, self.hdr_g,
                    self.layout.panel_view.width(), self.layout.panel_view.height(),
                    self.gray_natural, self.gray_contrast
                    )
                self.layout.panel_view.update()

    # Rotation Conversion from (-180,180) to (0,360)
    def Rotation_Recieve(self, value):
        if value < 0:
            value = value + 360
        return value
    def Rotation_Send(self, value):
        if value > 180:
            value = value - 360
        return value
    # Zoom Conversion from Zoom+DPI to Zoom (Bug reported : https://bugs.kde.org/show_bug.cgi?id=437068)
    def Zoom_Recieve(self, zoom, resolution):
        dpi = resolution / 72 # Neutral Zooom + DPI Factor
        value = zoom / dpi  # Adjust Zooom Level to DPI amount
        return value
    # Range
    def range_formating(self, i_value, i_min, i_max, o_min, o_max):
        """
        formats a value inside a given range into the same value on another given range
        i_value - input value
        i_min - input minimum
        i_max - input maximum
        o_min - output minimum
        o_max - output maximum
        """
        i_space = i_max - i_min
        o_space = o_max - o_min
        i_delta = i_value - i_min
        o_delta = (o_space * i_delta) / i_space
        o_value = o_min + o_delta
        return o_value
    def lin_to_cir(self, l):
        c = l**(0.5)
        return c
    def cir_to_lin(self, c):
        l = c**2
        return l
    # Conversions
    def gc(self, r, g, b):
        value = (0.2126*r) + (0.7152*g) + (0.0722*b) # BT.709
        if value <= 0.3:
            gc = ( 1 - value )
        else:
            gc = ( value - 0.4 )
        return gc
    def HEX_6string(self, red, green, blue):
        # Transform into HEX
        hex1 = str(hex(int(red * 255)))[2:4].zfill(2)
        hex2 = str(hex(int(green * 255)))[2:4].zfill(2)
        hex3 = str(hex(int(blue * 255)))[2:4].zfill(2)
        pigment_hex = str("#"+hex1+hex2+hex3)
        return pigment_hex

    #//
    #\\ Display ################################################################
    def Menu_Display(self):
        self.mode = self.layout.menu.currentText()
        self.Menu_Shrink()
        if self.mode == "Canvas":
            self.layout.panel_canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            self.layout.can_rotation_slider.setMinimumHeight(ui_10)
            self.layout.can_rotation_slider.setMaximumHeight(ui_20)
            self.layout.can_rotation_value.setMinimumHeight(ui_10)
            self.layout.can_rotation_value.setMaximumHeight(ui_20)

            self.layout.can_zoom_slider.setMinimumHeight(ui_10)
            self.layout.can_zoom_slider.setMaximumHeight(ui_20)
            self.layout.can_zoom_value.setMinimumHeight(ui_10)
            self.layout.can_zoom_value.setMaximumHeight(ui_20)

            self.layout.can_mirror.setMinimumHeight(ui_10)
            self.layout.can_mirror.setMaximumHeight(ui_20)
            self.layout.can_wrap.setMinimumHeight(ui_10)
            self.layout.can_wrap.setMaximumHeight(ui_20)

            self.layout.canvas_layout.setContentsMargins(zero,zero,zero,zero)
            self.layout.canvas_layout.setSpacing(unit)
        if self.mode == "Document":
            self.layout.doc_width.setMinimumHeight(ui_10)
            self.layout.doc_width.setMaximumHeight(ui_20)
            self.layout.doc_height.setMinimumHeight(ui_10)
            self.layout.doc_height.setMaximumHeight(ui_20)
            self.layout.doc_resolution.setMinimumHeight(ui_10)
            self.layout.doc_resolution.setMaximumHeight(ui_20)

            self.layout.doc_delta_reference.setMinimumHeight(ui_10)
            self.layout.doc_delta_reference.setMaximumHeight(ui_20)

            self.layout.doc_delta_up.setMinimumHeight(ui_10)
            self.layout.doc_delta_up.setMaximumHeight(ui_20)
            self.layout.doc_delta_left.setMinimumHeight(ui_10)
            self.layout.doc_delta_left.setMaximumHeight(ui_20)
            self.layout.doc_delta_right.setMinimumHeight(ui_10)
            self.layout.doc_delta_right.setMaximumHeight(ui_20)
            self.layout.doc_delta_down.setMinimumHeight(ui_10)
            self.layout.doc_delta_down.setMaximumHeight(ui_20)

            self.layout.gui_horizontal_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)
            self.layout.gui_vertical_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)
            self.layout.gui_horizontal_group.setMinimumHeight(zero)
            self.layout.gui_horizontal_group.setMaximumHeight(max_val)
            self.layout.gui_vertical_group.setMinimumHeight(zero)
            self.layout.gui_vertical_group.setMaximumHeight(max_val)

            self.layout.gui_sort.setMinimumHeight(ui_10)
            self.layout.gui_sort.setMaximumHeight(ui_20)
            self.layout.gui_mirror.setMinimumHeight(ui_10)
            self.layout.gui_mirror.setMaximumHeight(ui_20)
            self.layout.gui_visible.setMinimumHeight(ui_10)
            self.layout.gui_visible.setMaximumHeight(ui_20)
            self.layout.gui_lock.setMinimumHeight(ui_10)
            self.layout.gui_lock.setMaximumHeight(ui_20)

            self.layout.document_layout.setContentsMargins(zero,zero,zero,zero)
            self.layout.document_layout.setSpacing(unit)
        if self.mode == "View":
            self.layout.panel_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            self.layout.brush_blend.setMinimumHeight(ui_10)
            self.layout.brush_blend.setMaximumHeight(ui_20)

            self.layout.sof_n.setMinimumHeight(ui_10)
            self.layout.sof_n.setMaximumHeight(max_val)

            self.layout.sof_1_slider.setMinimumHeight(ui_10)
            self.layout.sof_1_slider.setMaximumHeight(ui_20)
            self.layout.sof_1_value.setMinimumHeight(ui_10)
            self.layout.sof_1_value.setMaximumHeight(ui_20)

            self.layout.sof_2_slider.setMinimumHeight(ui_10)
            self.layout.sof_2_slider.setMaximumHeight(ui_20)
            self.layout.sof_2_value.setMinimumHeight(ui_10)
            self.layout.sof_2_value.setMaximumHeight(ui_20)

            self.layout.sof_3_slider.setMinimumHeight(ui_10)
            self.layout.sof_3_slider.setMaximumHeight(ui_20)
            self.layout.sof_3_value.setMinimumHeight(ui_10)
            self.layout.sof_3_value.setMaximumHeight(ui_20)

            self.layout.hdr_e_slider.setMinimumHeight(ui_10)
            self.layout.hdr_e_slider.setMaximumHeight(ui_20)
            self.layout.hdr_e_value.setMinimumHeight(ui_10)
            self.layout.hdr_e_value.setMaximumHeight(ui_20)

            self.layout.hdr_g_slider.setMinimumHeight(ui_10)
            self.layout.hdr_g_slider.setMaximumHeight(ui_20)
            self.layout.hdr_g_value.setMinimumHeight(ui_10)
            self.layout.hdr_g_value.setMaximumHeight(ui_20)

            self.layout.view_layout.setContentsMargins(zero,zero,zero,zero)
            self.layout.view_layout.setSpacing(unit)
            self.layout.channels_sof.setSpacing(unit)
            self.layout.channels_hdr.setSpacing(unit)
    def Menu_Shrink(self):
        #\\ Canvas #############################################################
        self.layout.panel_canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.layout.can_rotation_slider.setMinimumHeight(zero)
        self.layout.can_rotation_slider.setMaximumHeight(zero)
        self.layout.can_rotation_value.setMinimumHeight(zero)
        self.layout.can_rotation_value.setMaximumHeight(zero)

        self.layout.can_zoom_slider.setMinimumHeight(zero)
        self.layout.can_zoom_slider.setMaximumHeight(zero)
        self.layout.can_zoom_value.setMinimumHeight(zero)
        self.layout.can_zoom_value.setMaximumHeight(zero)

        self.layout.can_mirror.setMinimumHeight(zero)
        self.layout.can_mirror.setMaximumHeight(zero)
        self.layout.can_wrap.setMinimumHeight(zero)
        self.layout.can_wrap.setMaximumHeight(zero)

        self.layout.canvas_layout.setContentsMargins(zero,zero,zero,zero)
        self.layout.canvas_layout.setSpacing(zero)

        #//
        #\\ Document ###########################################################
        self.layout.doc_width.setMinimumHeight(zero)
        self.layout.doc_width.setMaximumHeight(zero)
        self.layout.doc_height.setMinimumHeight(zero)
        self.layout.doc_height.setMaximumHeight(zero)
        self.layout.doc_resolution.setMinimumHeight(zero)
        self.layout.doc_resolution.setMaximumHeight(zero)

        self.layout.doc_delta_reference.setMinimumHeight(zero)
        self.layout.doc_delta_reference.setMaximumHeight(zero)

        self.layout.doc_delta_up.setMinimumHeight(zero)
        self.layout.doc_delta_up.setMaximumHeight(zero)
        self.layout.doc_delta_left.setMinimumHeight(zero)
        self.layout.doc_delta_left.setMaximumHeight(zero)
        self.layout.doc_delta_right.setMinimumHeight(zero)
        self.layout.doc_delta_right.setMaximumHeight(zero)
        self.layout.doc_delta_down.setMinimumHeight(zero)
        self.layout.doc_delta_down.setMaximumHeight(zero)

        self.layout.gui_horizontal_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.layout.gui_vertical_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.layout.gui_horizontal_group.setMinimumHeight(zero)
        self.layout.gui_horizontal_group.setMaximumHeight(zero)
        self.layout.gui_vertical_group.setMinimumHeight(zero)
        self.layout.gui_vertical_group.setMaximumHeight(zero)

        self.layout.gui_sort.setMinimumHeight(zero)
        self.layout.gui_sort.setMaximumHeight(zero)
        self.layout.gui_mirror.setMinimumHeight(zero)
        self.layout.gui_mirror.setMaximumHeight(zero)
        self.layout.gui_visible.setMinimumHeight(zero)
        self.layout.gui_visible.setMaximumHeight(zero)
        self.layout.gui_lock.setMinimumHeight(zero)
        self.layout.gui_lock.setMaximumHeight(zero)

        self.layout.document_layout.setContentsMargins(zero,zero,zero,zero)
        self.layout.document_layout.setSpacing(zero)

        #//
        #\\ Brush ##############################################################
        self.layout.panel_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.layout.brush_blend.setMinimumHeight(zero)
        self.layout.brush_blend.setMaximumHeight(zero)

        self.layout.sof_n.setMinimumHeight(zero)
        self.layout.sof_n.setMaximumHeight(zero)

        self.layout.sof_1_slider.setMinimumHeight(zero)
        self.layout.sof_1_slider.setMaximumHeight(zero)
        self.layout.sof_1_value.setMinimumHeight(zero)
        self.layout.sof_1_value.setMaximumHeight(zero)

        self.layout.sof_2_slider.setMinimumHeight(zero)
        self.layout.sof_2_slider.setMaximumHeight(zero)
        self.layout.sof_2_value.setMinimumHeight(zero)
        self.layout.sof_2_value.setMaximumHeight(zero)

        self.layout.sof_3_slider.setMinimumHeight(zero)
        self.layout.sof_3_slider.setMaximumHeight(zero)
        self.layout.sof_3_value.setMinimumHeight(zero)
        self.layout.sof_3_value.setMaximumHeight(zero)

        self.layout.hdr_e_slider.setMinimumHeight(zero)
        self.layout.hdr_e_slider.setMaximumHeight(zero)
        self.layout.hdr_e_value.setMinimumHeight(zero)
        self.layout.hdr_e_value.setMaximumHeight(zero)

        self.layout.hdr_g_slider.setMinimumHeight(zero)
        self.layout.hdr_g_slider.setMaximumHeight(zero)
        self.layout.hdr_g_value.setMinimumHeight(zero)
        self.layout.hdr_g_value.setMaximumHeight(zero)

        self.layout.view_layout.setContentsMargins(zero,zero,zero,zero)
        self.layout.view_layout.setSpacing(zero)
        self.layout.channels_sof.setSpacing(zero)
        self.layout.channels_hdr.setSpacing(zero)

        #//

    def Ratio(self):
        # Relocate Handle due to Size Variation
        try:
            # Panel
            self.Panel_Update()
            # CANVAS
            self.can_rotation_slider.Update(self.can_rotation / k_rotation, self.layout.can_rotation_slider.width(), self.gray_natural, self.gray_contrast, 0)
            self.can_zoom_slider.Update(self.can_zoom / k_zoom, self.layout.can_zoom_slider.width(), self.gray_natural, self.gray_contrast, 1)
            # VIEW
            self.sof_1_slider.Update(self.lin_to_cir(self.sof_1 / k_size), self.layout.sof_1_slider.width(), self.gray_natural, self.gray_contrast, self.sof_1_lock)
            self.sof_2_slider.Update(self.sof_2, self.layout.sof_2_slider.width(), self.gray_natural, self.gray_contrast, self.sof_2_lock)
            self.sof_3_slider.Update(self.sof_3, self.layout.sof_3_slider.width(), self.gray_natural, self.gray_contrast, self.sof_3_lock)
            self.hdr_e_slider.Update(self.range_formating(self.hdr_e, -10, 10, 0, 1), self.layout.hdr_e_slider.width(), self.gray_natural, self.gray_contrast, 0)
            self.hdr_g_slider.Update(self.hdr_g / k_gamma, self.layout.hdr_g_slider.width(), self.gray_natural, self.gray_contrast, 1)
        except:
            pass

    #//
    #\\ CANVAS #################################################################
    # Panel
    def CANVAS_Signal(self, SIGNAL_VIEW):
        pass

    def CANVAS_Rotation_READ(self, value):
        # Variable
        self.can_rotation = round(value, 3)
        # Block Signals
        self.can_rotation_slider.blockSignals(True)
        self.layout.can_rotation_value.blockSignals(True)
        # Widgets
        self.can_rotation_slider.Update(value / k_rotation, self.layout.can_rotation_slider.width(), self.gray_natural, self.gray_contrast, 0)
        self.layout.can_rotation_value.setValue(value)
        # Block Signals
        self.can_rotation_slider.blockSignals(False)
        self.layout.can_rotation_value.blockSignals(False)
        # Updates
        self.layout.can_rotation_slider.update()
        self.layout.can_rotation_value.update()
    def CANVAS_Rotation_Minus(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.can_rotation = self.can_rotation - unit
            if self.can_rotation <= 0:
                self.can_rotation = self.can_rotation + k_rotation
            self.CANVAS_Rotation_READ(self.can_rotation)
            Krita.instance().activeWindow().activeView().canvas().setRotation(self.Rotation_Send(self.can_rotation))
    def CANVAS_Rotation_Plus(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.can_rotation = self.can_rotation + unit
            if self.can_rotation >= k_rotation:
                self.can_rotation = self.can_rotation - k_rotation
            self.CANVAS_Rotation_READ(self.can_rotation)
            Krita.instance().activeWindow().activeView().canvas().setRotation(self.Rotation_Send(self.can_rotation))
    def CANVAS_Rotation_Slider_Modify(self, SIGNAL_VALUE):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.can_rotation = SIGNAL_VALUE * k_rotation
            self.CANVAS_Rotation_READ(self.can_rotation)
            Krita.instance().activeWindow().activeView().canvas().setRotation(self.Rotation_Send(self.can_rotation))
        else:
            self.can_rotation = zero
            self.CANVAS_Rotation_READ(self.can_rotation)
    def CANVAS_Rotation_Value_Modify(self, SIGNAL_VALUE):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.can_rotation = self.layout.can_rotation_value.value()
            self.CANVAS_Rotation_READ(self.can_rotation)
            Krita.instance().activeWindow().activeView().canvas().setRotation(self.Rotation_Send(self.can_rotation))
        else:
            self.can_rotation = zero
            self.CANVAS_Rotation_READ(self.can_rotation)
    def CANVAS_Rotation_RESET(self):
        self.CANVAS_Rotation_READ(zero)
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            # Krita.instance().activeWindow().activeView().canvas().resetRotation()
            Krita.instance().activeWindow().activeView().canvas().setRotation(zero)

    def CANVAS_Zoom_READ(self, value):
        # Variable
        self.can_zoom = round(value, 3)
        # Block Signals
        self.can_zoom_slider.blockSignals(True)
        self.layout.can_zoom_value.blockSignals(True)
        # Widgets
        self.can_zoom_slider.Update(value / k_zoom, self.layout.can_zoom_slider.width(), self.gray_natural, self.gray_contrast, 1)
        self.layout.can_zoom_value.setValue(value)
        # Block Signals
        self.can_zoom_slider.blockSignals(False)
        self.layout.can_zoom_value.blockSignals(False)
        # Updates
        self.layout.can_zoom_slider.update()
        self.layout.can_zoom_value.update()
    def CANVAS_Zoom_Minus(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.can_zoom = self.can_zoom - u_zoom
            if self.can_zoom <= zero:
                self.can_zoom = zero
            self.CANVAS_Zoom_READ(self.can_zoom)
            Krita.instance().activeWindow().activeView().canvas().setZoomLevel(self.can_zoom)
    def CANVAS_Zoom_Plus(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.can_zoom = self.can_zoom + u_zoom
            if self.can_zoom >= k_zoom:
                self.can_zoom = k_zoom
            self.CANVAS_Zoom_READ(self.can_zoom)
            Krita.instance().activeWindow().activeView().canvas().setZoomLevel(self.can_zoom)
    def CANVAS_Zoom_Slider_Modify(self, SIGNAL_VALUE):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.can_zoom = SIGNAL_VALUE * k_zoom
            self.CANVAS_Zoom_READ(self.can_zoom)
            Krita.instance().activeWindow().activeView().canvas().setZoomLevel(self.can_zoom)
        else:
            self.can_zoom = unit
            self.CANVAS_Zoom_READ(self.can_zoom)
    def CANVAS_Zoom_Value_Modify(self, SIGNAL_VALUE):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.can_zoom = self.layout.can_zoom_value.value()
            self.CANVAS_Zoom_READ(self.can_zoom)
            Krita.instance().activeWindow().activeView().canvas().setZoomLevel(self.can_zoom)
        else:
            self.can_zoom = unit
            self.CANVAS_Zoom_READ(self.can_zoom)
    def CANVAS_Zoom_RESET(self):
        self.CANVAS_Zoom_READ(unit)
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            # Krita.instance().activeWindow().activeView().canvas().resetZoom()
            Krita.instance().activeWindow().activeView().canvas().setZoomLevel(unit)

    def CANVAS_Mirror_READ(self, value):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.can_mirror = value
            self.layout.can_mirror.setChecked(value)
        else:
            self.can_mirror = False
            self.layout.can_mirror.setChecked(False)
    def CANVAS_Mirror_TOGGLE(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            value = self.layout.can_mirror.isChecked()
            Krita.instance().activeWindow().activeView().canvas().setMirror(value)
        else:
            value = self.layout.can_mirror.setChecked(False)

    def CANVAS_Wrap_READ(self, value):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.can_wrap = value
            self.layout.can_wrap.setChecked(value)
        else:
            self.can_wrap = False
            self.layout.can_wrap.setChecked(False)
    def CANVAS_Wrap_TOGGLE(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            value = self.layout.can_wrap.isChecked()
            Krita.instance().activeWindow().activeView().canvas().setWrapAroundMode(value)
        else:
            value = self.layout.can_wrap.setChecked(False)

    #//
    #\\ DOCUMENT ###############################################################
    def DOC_Width_READ(self, value):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.doc_width = value
            self.layout.doc_width.setValue(value)
        else:
            self.doc_width = zero
            self.layout.doc_width.setValue(zero)
    def DOC_Width_WRITE(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            width = self.layout.doc_width.value()
            Krita.instance().activeDocument().setWidth(width)

    def DOC_Height_READ(self, value):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.doc_height = value
            self.layout.doc_height.setValue(value)
        else:
            self.doc_height = zero
            self.layout.doc_height.setValue(zero)
    def DOC_Height_WRITE(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            height = self.layout.doc_height.value()
            Krita.instance().activeDocument().setHeight(height)

    def DOC_Resolution_READ(self, value):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.doc_resolution = value
            self.layout.doc_resolution.setValue(value)
        else:
            self.doc_resolution = zero
            self.layout.doc_resolution.setValue(zero)
    def DOC_Resolution_WRITE(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            height = self.layout.doc_resolution.value()
            Krita.instance().activeDocument().setResolution(height)

    def GUIDES_Delta_Reference(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.ui_d_ref = self.layout.doc_delta_reference.isChecked()
            if self.ui_d_ref == True:
                # Guides
                self.GUIDES_Reference_Horizontal()
                self.GUIDES_Reference_Vertical()
                # Reset Deltas before doing changes
                self.delta_new = [0,0,0,0]
                self.layout.doc_delta_up.setValue(0)
                self.layout.doc_delta_left.setValue(0)
                self.layout.doc_delta_right.setValue(0)
                self.layout.doc_delta_down.setValue(0)
                # Allow Delta Editing
                self.layout.doc_delta_up.setEnabled(True)
                self.layout.doc_delta_left.setEnabled(True)
                self.layout.doc_delta_right.setEnabled(True)
                self.layout.doc_delta_down.setEnabled(True)
                # Save Reference List
                self.doc_ref = [round(self.layout.doc_width.value()), round(self.layout.doc_height.value())]
                self.layout.doc_width.setPrefix("["+str(self.doc_ref[0])+"]-")
                self.layout.doc_height.setPrefix("["+str(self.doc_ref[1])+"]-")
            else:
                # Guides
                self.GUIDES_Reference_Horizontal()
                self.GUIDES_Reference_Vertical()
                # Reset Values
                self.delta_new = [0,0,0,0]
                self.layout.doc_delta_up.setValue(0)
                self.layout.doc_delta_left.setValue(0)
                self.layout.doc_delta_right.setValue(0)
                self.layout.doc_delta_down.setValue(0)
                # No Edit Allowed
                self.layout.doc_delta_up.setEnabled(False)
                self.layout.doc_delta_left.setEnabled(False)
                self.layout.doc_delta_right.setEnabled(False)
                self.layout.doc_delta_down.setEnabled(False)
                # Prefix
                self.doc_ref = [None, None]
                self.layout.doc_width.setPrefix("W-")
                self.layout.doc_height.setPrefix("H-")
        else:
            # Reset Values
            self.delta_new = [0,0,0,0]
            self.layout.doc_delta_up.setValue(0)
            self.layout.doc_delta_left.setValue(0)
            self.layout.doc_delta_right.setValue(0)
            self.layout.doc_delta_down.setValue(0)
            # No Edit Allowed
            self.layout.doc_delta_up.setEnabled(False)
            self.layout.doc_delta_left.setEnabled(False)
            self.layout.doc_delta_right.setEnabled(False)
            self.layout.doc_delta_down.setEnabled(False)
            # Prefix
            self.doc_ref = [None, None]
            self.layout.doc_delta_reference.setChecked(False)
            self.layout.doc_width.setPrefix("W-")
            self.layout.doc_height.setPrefix("H-")
    def GUIDES_Reference_Horizontal(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            # Add Edge Guides
            if self.ui_d_ref == True:
                self.gui_hor_norm.insert(0, 0)
                self.gui_hor_norm.insert(1, self.doc_height)
            # Minus Edge Guides
            if self.ui_d_ref == False:
                # Count Edges and Anomalies
                count = 0
                for i in range(0, len(self.gui_hor_norm)):
                    if (self.gui_hor_norm[i] <= self.delta_new[0] or self.gui_hor_norm[i] >= self.delta_new[0] + self.doc_ref[1]):
                        count += 1
                # Delete Edges and Anomalies
                for c in range(0, count):
                    for i in range(0, len(self.gui_hor_norm)):
                        if (self.gui_hor_norm[i] <= self.delta_new[0] or self.gui_hor_norm[i] >= self.delta_new[0] + self.doc_ref[1]):
                            del self.gui_hor_norm[i]
                            break
            # Populate List
            self.layout.gui_horizontal_group.clear()
            for i in range(0, len(self.gui_hor_norm)):
                self.layout.gui_horizontal_group.insertItem(i, str(int(self.gui_hor_norm[i])))
            # Apply Guides to Krita
            Krita.instance().activeDocument().setHorizontalGuides(self.gui_hor_norm)
    def GUIDES_Reference_Vertical(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            # Add Edge Guides
            if self.ui_d_ref == True:
                self.gui_ver_norm.insert(0, 0)
                self.gui_ver_norm.insert(1, self.doc_width)
            # Minus Edge Guides
            if self.ui_d_ref == False:
                # Count Edges and Anomalies
                count = 0
                for i in range(0, len(self.gui_ver_norm)):
                    if (self.gui_ver_norm[i] <= self.delta_new[1] or self.gui_ver_norm[i] >= self.delta_new[1] + self.doc_ref[0]):
                        count += 1
                # Delete Edges and Anomalies
                for c in range(0, count):
                    for i in range(0, len(self.gui_ver_norm)):
                        if (self.gui_ver_norm[i] <= self.delta_new[1] or self.gui_ver_norm[i] >= self.delta_new[1] + self.doc_ref[0]):
                            del self.gui_ver_norm[i]
                            break
            # Populate List
            self.layout.gui_vertical_group.clear()
            for i in range(0, len(self.gui_ver_norm)):
                self.layout.gui_vertical_group.insertItem(i, str(int(self.gui_ver_norm[i])))
            # Apply Guides to Krita
            Krita.instance().activeDocument().setVerticalGuides(self.gui_ver_norm)
    def GUIDES_Delta(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            try:
                # New Values
                self.delta_new = [
                    self.layout.doc_delta_up.value(), # up 0
                    self.layout.doc_delta_left.value(), # left 1
                    self.layout.doc_delta_right.value(), # right 2
                    self.layout.doc_delta_down.value(), # down 32
                    ]
                # Operations
                du = self.delta_old[0] - self.delta_new[0]
                dl = self.delta_old[1] - self.delta_new[1]
                dw = self.delta_new[1] + self.doc_ref[0] + self.delta_new[2]
                dh = self.delta_new[0] + self.doc_ref[1] + self.delta_new[3]
                # Resize Image
                Krita.instance().activeDocument().resizeImage(dl,du,dw,dh)
                # Future Proof Nest Delta
                self.delta_old = [
                    self.delta_new[0], # up
                    self.delta_new[1], # left
                    self.delta_new[2], # right┬
                    self.delta_new[3], # down
                    ]
            except:
                self.layout.label.setText("Reference not Found")
        else:
            self.layout.label.setText("Document not Found")

    def GUIDES_Horizontal_LIST_NOR(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            #\\ List ###########################################################
            # Delete Previous List
            self.layout.gui_horizontal_group.clear()
            # Sort Items
            if self.ui_g_sort == True:
                self.gui_hor_norm.sort()
                Krita.instance().activeDocument().setHorizontalGuides(self.gui_hor_norm)
            # Populate with the updated List
            for i in range(0, len(self.gui_hor_norm)):
                self.layout.gui_horizontal_group.insertItem(i, str(int(self.gui_hor_norm[i])))
            # Case now considering Previous case
            self.gui_hor_dif = len(self.gui_hor_norm) - len(self.gui_hor_previous)
            #//
            #\\ Index ##########################################################
            index = 0
            a = set(self.gui_hor_norm)
            b = set(self.gui_hor_previous)
            c = a.difference(b)
            if len(c) == 1:
                for i in range(0, len(self.gui_hor_norm)):
                    if self.gui_hor_norm[i] in c:
                        index = i # because of "a" index is independant of sort or not
            # Symmetrical Index
            sym_index = 0
            # Case =0
            if self.gui_hor_dif == 0:
                max = len(self.gui_hor_norm) # Scale does not count zero
                if max % 2 == 0: # Paridade and alter Scale to count zero
                    max = max - 1 # Even
                else:
                    max = max # Odd
                sym_index = max - index
                self.gui_hor_index = [index, sym_index]
            else:
                self.gui_hor_index = [None, None]
            # Select Item
            if self.gui_hor_index[0] != None:
                self.layout.gui_horizontal_group.setCurrentRow(self.gui_hor_index[0])
            #//
            #\\ Mirror #########################################################
            if (self.ui_g_sort == True and self.ui_g_mirror == True and self.gui_hor_index[0] != None):
                value = eval(self.layout.gui_horizontal_group.item(self.gui_hor_index[0]).text())
                sym_value = self.doc_height - value # Because self.doc_ref == False
                if (value != (self.doc_height/2) and value > 0 and value < self.doc_height):
                    if (len(self.gui_hor_norm) % 2 != 0 and self.gui_hor_index[0] == 0):
                        self.gui_hor_norm.append(sym_value) # add value at the end of the list if index is empty
                    else:
                        self.gui_hor_norm[self.gui_hor_index[1]] = sym_value
                        self.layout.gui_horizontal_group.item(self.gui_hor_index[1]).setText(str(sym_value))
            #//
            #\\ Apply ##########################################################
            if (self.gui_hor_dif == 0 and (self.ui_g_sort == True or self.ui_g_mirror == True)):
                Krita.instance().activeDocument().setHorizontalGuides(self.gui_hor_norm)
            #//
    def GUIDES_Horizontal_LIST_REF(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            #\\ List ###########################################################
            # Delete Previous List
            self.layout.gui_horizontal_group.clear()
            # Variables
            dh1 = self.delta_new[0]
            dh2 = self.delta_new[0] + self.doc_ref[1]
            dh3 = self.delta_new[0] + self.doc_ref[1] + self.delta_new[3]
            # Sort Items
            if self.ui_g_sort == True:
                # Sort
                self.gui_hor_norm.sort()
                # Delete doc ref numbers from list
                for i in range(0, len(self.gui_hor_norm)):
                    if self.gui_hor_norm[i] == dh1:
                        del self.gui_hor_norm[i]
                        break
                for i in range(0, len(self.gui_hor_norm)):
                    if self.gui_hor_norm[i] == dh2:
                        del self.gui_hor_norm[i]
                        break
                # Add ref numbers back correctly
                self.gui_hor_norm.insert(0, dh1)
                self.gui_hor_norm.insert(1, dh2)
                # Apply new list to Guides
                Krita.instance().activeDocument().setHorizontalGuides(self.gui_hor_norm)
            # Populate with the updated List
            for i in range(0, len(self.gui_hor_norm)):
                self.layout.gui_horizontal_group.insertItem(i, str(int(self.gui_hor_norm[i])))
            # Case now considering Previous case
            self.gui_hor_dif = len(self.gui_hor_norm) - len(self.gui_hor_previous)
            #//
            #\\ Index ##########################################################
            index = 0
            a = set(self.gui_hor_norm[2:])
            b = set(self.gui_hor_previous[2:])
            c = a.difference(b)
            if len(c) == 1:
                for i in range(0, len(self.gui_hor_norm)):
                    if self.gui_hor_norm[i] in c:
                        index = i
            # Symmetrical Index
            sym_index = 0
            # Case =0
            if self.gui_hor_dif == 0:
                max = len(self.gui_hor_norm) # Scale does not count zero
                if max % 2 == 0: # Paridade and alter Scale to count zero
                    max = max - 1 # Even
                else:
                    max = max # Odd
                sym_index = max - (index-2)
                self.gui_hor_index = [index, sym_index]
            else:
                self.gui_hor_index = [None, None]
            # Select Item
            if self.gui_hor_index[0] != None:
                self.layout.gui_horizontal_group.setCurrentRow(self.gui_hor_index[0])
            #//
            #\\ Mirror #########################################################
            if (self.ui_g_sort == True and self.ui_g_mirror == True and self.gui_hor_index[0] != None):
                value = eval(self.layout.gui_horizontal_group.item(self.gui_hor_index[0]).text()) - dh1
                sym_value = dh2 - value # Because self.doc_ref == True
                if (value != (self.doc_height/2) and value > 0 and value < dh3):
                    if (len(self.gui_hor_norm) % 2 != 0 and self.gui_hor_index[0] == 2):
                        self.gui_hor_norm.append(sym_value) # add value at the end of the list if index is empty
                    else:
                        self.gui_hor_norm[self.gui_hor_index[1]] = sym_value
                        self.layout.gui_horizontal_group.item(self.gui_hor_index[1]).setText(str(sym_value))
            #//
            #\\ Apply ##########################################################
            if (self.gui_hor_dif == 0 and (self.ui_g_sort == True or self.ui_g_mirror == True)):
                Krita.instance().activeDocument().setHorizontalGuides(self.gui_hor_norm)
            #//
    def GUIDES_Horizontal_EDIT(self):
        # Edit Selected Row
        row = self.layout.gui_horizontal_group.currentRow()
        item = self.layout.gui_horizontal_group.item(row)
        if item is not None:
            title = "Guide = {0}".format(str(row))
            string, ok = QInputDialog.getText(self, "Edit Guide", title,
                    QLineEdit.Normal, item.text())
            if ok and string is not None:
                item.setText(str(eval(string)))
            # Apply changed Guide to Krita
            list = []
            if self.ui_d_ref == True:
                list.append(self.delta_new[0])
                list.append(self.delta_new[0]+self.doc_ref[1])
                for i in range(2, self.layout.gui_horizontal_group.count()):
                    list.append(eval(self.layout.gui_horizontal_group.item(i).text()))
            else:
                for i in range(0, self.layout.gui_horizontal_group.count()):
                    list.append(eval(self.layout.gui_horizontal_group.item(i).text()))
            Krita.instance().activeDocument().setHorizontalGuides(list)

    def GUIDES_Vertical_LIST_NOR(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            #\\ List ###########################################################
            # Delete Previous List
            self.layout.gui_vertical_group.clear()
            # Sort Items
            if self.ui_g_sort == True:
                self.gui_ver_norm.sort()
                Krita.instance().activeDocument().setVerticalGuides(self.gui_ver_norm)
            # Populate with the updated List
            for i in range(0, len(self.gui_ver_norm)):
                self.layout.gui_vertical_group.insertItem(i, str(int(self.gui_ver_norm[i])))
            # Case now considering Previous case
            self.gui_ver_dif = len(self.gui_ver_norm) - len(self.gui_ver_previous)
            #//
            #\\ Index ##########################################################
            index = 0
            a = set(self.gui_ver_norm)
            b = set(self.gui_ver_previous)
            c = a.difference(b)
            if len(c) == 1:
                for i in range(0, len(self.gui_ver_norm)):
                    if self.gui_ver_norm[i] in c:
                        index = i # because of "a" index is independant of sort or not
            # Symmetrical Index
            sym_index = 0
            # Case =0
            if self.gui_ver_dif == 0:
                max = len(self.gui_ver_norm) # Scale does not count zero
                if max % 2 == 0: # Paridade and alter Scale to count zero
                    max = max - 1 # Even
                else:
                    max = max # Odd
                sym_index = max - index
                self.gui_ver_index = [index, sym_index]
            else:
                self.gui_ver_index = [None, None]
            # Select Item
            if self.gui_ver_index[0] != None:
                self.layout.gui_vertical_group.setCurrentRow(self.gui_ver_index[0])
            #//
            #\\ Mirror #########################################################
            if (self.ui_g_sort == True and self.ui_g_mirror == True and self.gui_ver_index[0] != None):
                value = eval(self.layout.gui_vertical_group.item(self.gui_ver_index[0]).text())
                sym_value = self.doc_width - value # Because self.doc_ref == False
                if (value != (self.doc_width/2) and value > 0 and value < self.doc_width):
                    if (len(self.gui_ver_norm) % 2 != 0 and self.gui_ver_index[0] == 0):
                        self.gui_ver_norm.append(sym_value) # add value at the end of the list if index is empty
                    else:
                        self.gui_ver_norm[self.gui_ver_index[1]] = sym_value
                        self.layout.gui_vertical_group.item(self.gui_ver_index[1]).setText(str(sym_value))
            #//
            #\\ Apply ##########################################################
            if (self.gui_ver_dif == 0 and (self.ui_g_sort == True or self.ui_g_mirror == True)):
                Krita.instance().activeDocument().setVerticalGuides(self.gui_ver_norm)
            #//
    def GUIDES_Vertical_LIST_REF(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            #\\ List ###########################################################
            # Delete Previous List
            self.layout.gui_vertical_group.clear()
            # Variables
            dh1 = self.delta_new[1]
            dh2 = self.delta_new[1] + self.doc_ref[0]
            dh3 = self.delta_new[1] + self.doc_ref[0] + self.delta_new[2]
            # Sort Items
            if self.ui_g_sort == True:
                # Sort
                self.gui_ver_norm.sort()
                # Delete doc ref numbers from list
                for i in range(0, len(self.gui_ver_norm)):
                    if self.gui_ver_norm[i] == dh1:
                        del self.gui_ver_norm[i]
                        break
                for i in range(0, len(self.gui_ver_norm)):
                    if self.gui_ver_norm[i] == dh2:
                        del self.gui_ver_norm[i]
                        break
                # Add ref numbers back correctly
                self.gui_ver_norm.insert(0, dh1)
                self.gui_ver_norm.insert(1, dh2)
                # Apply new list to Guides
                Krita.instance().activeDocument().setVerticalGuides(self.gui_ver_norm)
            # Populate with the updated List
            for i in range(0, len(self.gui_ver_norm)):
                self.layout.gui_vertical_group.insertItem(i, str(int(self.gui_ver_norm[i])))
            # Case now considering Previous case
            self.gui_ver_dif = len(self.gui_ver_norm) - len(self.gui_ver_previous)
            #//
            #\\ Index ##########################################################
            index = 0
            a = set(self.gui_ver_norm[2:])
            b = set(self.gui_ver_previous[2:])
            c = a.difference(b)
            if len(c) == 1:
                for i in range(0, len(self.gui_ver_norm)):
                    if self.gui_ver_norm[i] in c:
                        index = i
            # Symmetrical Index
            sym_index = 0
            # Case =0
            if self.gui_ver_dif == 0:
                max = len(self.gui_ver_norm) # Scale does not count zero
                if max % 2 == 0: # Paridade and alter Scale to count zero
                    max = max - 1 # Even
                else:
                    max = max # Odd
                sym_index = max - (index-2)
                self.gui_ver_index = [index, sym_index]
            else:
                self.gui_ver_index = [None, None]
            # Select Item
            if self.gui_ver_index[0] != None:
                self.layout.gui_vertical_group.setCurrentRow(self.gui_ver_index[0])
            #//
            #\\ Mirror #########################################################
            if (self.ui_g_sort == True and self.ui_g_mirror == True and self.gui_ver_index[0] != None):
                value = eval(self.layout.gui_vertical_group.item(self.gui_ver_index[0]).text()) - dh1
                sym_value = dh2 - value # Because self.doc_ref == True
                if (value != (self.doc_width/2) and value > 0 and value < dh3):
                    if (len(self.gui_ver_norm) % 2 != 0 and self.gui_ver_index[0] == 2):
                        self.gui_ver_norm.append(sym_value) # add value at the end of the list if index is empty
                    else:
                        self.gui_ver_norm[self.gui_ver_index[1]] = sym_value
                        self.layout.gui_vertical_group.item(self.gui_ver_index[1]).setText(str(sym_value))
            #//
            #\\ Apply ##########################################################
            if (self.gui_ver_dif == 0 and (self.ui_g_sort == True or self.ui_g_mirror == True)):
                Krita.instance().activeDocument().setVerticalGuides(self.gui_ver_norm)
            #//
    def GUIDES_Vertical_EDIT(self):
        # Edit Selected Row
        row = self.layout.gui_vertical_group.currentRow()
        item = self.layout.gui_vertical_group.item(row)
        if item is not None:
            title = "Guide = {0}".format(str(row))
            string, ok = QInputDialog.getText(self, "Edit Guide", title,
                    QLineEdit.Normal, item.text())
            if ok and string is not None:
                item.setText(str(eval(string)))
            # Apply changed Guide to Krita
            list = []
            if self.ui_d_ref == True:
                list.append(self.delta_new[1])
                list.append(self.delta_new[1]+self.doc_ref[0])
                for i in range(2, self.layout.gui_vertical_group.count()):
                    list.append(eval(self.layout.gui_vertical_group.item(i).text()))
            else:
                for i in range(0, self.layout.gui_vertical_group.count()):
                    list.append(eval(self.layout.gui_vertical_group.item(i).text()))
            Krita.instance().activeDocument().setVerticalGuides(list)

    def GUIDES_Sort(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.ui_g_sort = self.layout.gui_sort.isChecked()
            if self.ui_g_sort == True:
                self.layout.gui_mirror.setEnabled(True)
            if self.ui_g_sort == False:
                self.layout.gui_mirror.setChecked(False)
                self.layout.gui_mirror.setEnabled(False)
        else:
            self.ui_g_sort = False
            self.layout.gui_sort.setChecked(False)
            self.layout.gui_mirror.setChecked(False)
            self.layout.gui_mirror.setEnabled(False)

    def GUIDES_Mirror(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.ui_g_mirror = self.layout.gui_mirror.isChecked()
            if self.ui_g_mirror == True:
                self.layout.gui_horizontal_group.setSelectionMode(3)
            else:
                self.layout.gui_horizontal_group.setSelectionMode(1)
        else:
            self.ui_g_mirror = False
            self.layout.gui_mirror.setChecked(False)

    def GUIDES_Visible_READ(self, value):
        self.ui_g_visible = value
        self.layout.gui_visible.setChecked(value)
    def GUIDES_Visible_WRITE(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.ui_g_visible = self.layout.gui_visible.isChecked()
            Krita.instance().activeDocument().setGuidesVisible(self.ui_g_visible)
        else:
            self.ui_g_visible = False
            self.layout.gui_visible.setChecked(False)

    def GUIDES_Lock_READ(self, value):
        self.ui_g_lock = value
        self.layout.gui_lock.setChecked(value)
    def GUIDES_Lock_WRITE(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.ui_g_lock = self.layout.gui_lock.isChecked()
            Krita.instance().activeDocument().setGuidesLocked(self.ui_g_lock)
        else:
            self.ui_g_lock = False
            self.layout.gui_lock.setChecked(False)

    #//
    #\\ VIEW ###################################################################
    # PANEL VIEW
    def VIEW_Signal(self, SIGNAL_VIEW):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            """
            # Size
            self.sof_1 = SIGNAL_VIEW[0] * k_size
            self.sof_1_slider.Update(self.lin_to_cir(self.sof_1 / k_size), self.layout.sof_1_slider.width(), self.gray_natural, self.gray_contrast, self.sof_1_lock)
            self.layout.sof_1_value.setValue(self.sof_1)
            Krita.instance().activeWindow().activeView().setBrushSize(self.sof_1)
            """
            # Opacity
            self.sof_2 = SIGNAL_VIEW[1]
            self.sof_2_slider.Update(self.sof_2, self.layout.sof_2_slider.width(), self.gray_natural, self.gray_contrast, self.sof_2_lock)
            self.layout.sof_2_value.setValue(self.sof_2 * k_opacity)
            Krita.instance().activeWindow().activeView().setPaintingOpacity(self.sof_2)
            # Flow
            self.sof_3 = SIGNAL_VIEW[2]
            self.sof_3_slider.Update(self.sof_3, self.layout.sof_3_slider.width(), self.gray_natural, self.gray_contrast, self.sof_3_lock)
            self.layout.sof_3_value.setValue(self.sof_3 * k_flow)
            Krita.instance().activeWindow().activeView().setPaintingFlow(self.sof_3)

    # SOF
    def SOF_Lock_APPLY(self, SIGNAL_CLICKS):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            av = Krita.instance().activeWindow().activeView()
            av.setBrushSize(self.sof_1_lock)
            av.setPaintingOpacity(self.sof_2_lock)
            av.setPaintingFlow(self.sof_3_lock)
            self.sof_n.Setup_SOF(self.gray_contrast)
            self.SOF_1_READ(self.sof_1_lock)
            self.SOF_2_READ(self.sof_2_lock)
            self.SOF_3_READ(self.sof_3_lock)
    def SOF_Lock_SAVE(self, SIGNAL_CLICKS):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            av = Krita.instance().activeWindow().activeView()
            self.sof_1_lock = av.brushSize()
            self.sof_2_lock = av.paintingOpacity()
            self.sof_3_lock = av.paintingFlow()
            self.sof_n.Setup_SOF(self.gray_contrast)
            self.layout.sof_n.update()
            self.sof_1_slider.Update(self.lin_to_cir(self.sof_1 / k_size), self.layout.sof_1_slider.width(), self.gray_natural, self.gray_contrast, self.sof_1_lock)
            self.sof_2_slider.Update(self.sof_2, self.layout.sof_2_slider.width(), self.gray_natural, self.gray_contrast, self.sof_2_lock)
            self.sof_3_slider.Update(self.sof_3, self.layout.sof_3_slider.width(), self.gray_natural, self.gray_contrast, self.sof_3_lock)
            self.update()
    def SOF_Lock_CLEAN(self, SIGNAL_CLICKS):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            av = Krita.instance().activeWindow().activeView()
            self.sof_1_lock = i_size
            self.sof_2_lock = i_opacity
            self.sof_3_lock = i_flow
            av.setBrushSize(self.sof_1_lock)
            av.setPaintingOpacity(self.sof_2_lock)
            av.setPaintingFlow(self.sof_3_lock)
            self.sof_n.Setup_SOF(self.gray_contrast)
            self.SOF_1_READ(self.sof_1_lock)
            self.SOF_2_READ(self.sof_2_lock)
            self.SOF_3_READ(self.sof_3_lock)

    def SOF_1_READ(self, value):
        self.sof_1 = value
        self.sof_1_slider.Update(self.lin_to_cir(value / k_size), self.layout.sof_1_slider.width(), self.gray_natural, self.gray_contrast, self.sof_1_lock)
        self.layout.sof_1_value.setValue(value)
        self.layout.sof_1_slider.update()
        self.layout.sof_1_value.update()
        self.Panel_Update()
    def SOF_1_Minus(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.sof_1 = self.sof_1 - 1
            if self.sof_1 <= zero:
                self.sof_1 = zero
            self.sof_1_slider.Update(self.lin_to_cir(self.sof_1 / k_size), self.layout.sof_1_slider.width(), self.gray_natural, self.gray_contrast, self.sof_1_lock)
            self.layout.sof_1_value.setValue(self.sof_1)
            self.sof_1_slider.update()
            self.Panel_Update()
    def SOF_1_Plus(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.sof_1 = self.sof_1 + 1
            if self.sof_1 >= k_size:
                self.sof_1 = k_size
            self.sof_1_slider.Update(self.lin_to_cir(self.sof_1 / k_size), self.layout.sof_1_slider.width(), self.gray_natural, self.gray_contrast, self.sof_1_lock)
            self.layout.sof_1_value.setValue(self.sof_1)
            self.sof_1_slider.update()
            self.Panel_Update()
    def SOF_1_Slider_Modify(self, SIGNAL_VALUE):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.sof_1 = self.cir_to_lin(SIGNAL_VALUE) * k_size
            self.layout.sof_1_value.setValue(self.sof_1)
            Krita.instance().activeWindow().activeView().setBrushSize(self.sof_1)
        else:
            self.sof_1 = self.sof_1_lock
            self.sof_1_slider.Update(self.lin_to_cir(self.sof_1 / k_size), self.layout.sof_1_slider.width(), self.gray_natural, self.gray_contrast, self.sof_1_lock)
            self.layout.sof_1_value.setValue(self.sof_1)
        self.layout.sof_1_slider.update()
        self.layout.sof_1_value.update()
        self.Panel_Update()
    def SOF_1_Value_Modify(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.sof_1 = self.layout.sof_1_value.value()
            self.sof_1_slider.Update(self.lin_to_cir(self.sof_1 / k_size), self.layout.sof_1_slider.width(), self.gray_natural, self.gray_contrast, self.sof_1_lock)
            Krita.instance().activeWindow().activeView().setBrushSize(self.sof_1)
        else:
            self.sof_1 = self.sof_1_lock
            self.sof_1_slider.Update(self.lin_to_cir(self.sof_1 / k_size), self.layout.sof_1_slider.width(), self.gray_natural, self.gray_contrast, self.sof_1_lock)
            self.layout.sof_1_value.setValue(self.sof_1)
        self.layout.sof_1_slider.update()
        self.layout.sof_1_value.update()
        self.Panel_Update()

    def SOF_2_READ(self, value):
        self.sof_2 = value
        self.sof_2_slider.Update(value, self.layout.sof_2_slider.width(), self.gray_natural, self.gray_contrast, self.sof_2_lock)
        self.layout.sof_2_value.setValue(value * k_opacity)
        self.layout.sof_2_slider.update()
        self.layout.sof_2_value.update()
        self.Panel_Update()
    def SOF_2_Minus(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.sof_2 = self.sof_2 - (unit/k_opacity)
            if self.sof_2 <= zero:
                self.sof_2 = zero
            self.sof_2_slider.Update(self.sof_2, self.layout.sof_2_slider.width(), self.gray_natural, self.gray_contrast, self.sof_2_lock)
            self.layout.sof_2_value.setValue(self.sof_2 * k_opacity)
            self.sof_2_slider.update()
            self.Panel_Update()
    def SOF_2_Plus(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.sof_2 = self.sof_2 + (unit/k_opacity)
            if self.sof_2 >= unit:
                self.sof_2 = unit
            self.sof_2_slider.Update(self.sof_2, self.layout.sof_2_slider.width(), self.gray_natural, self.gray_contrast, self.sof_2_lock)
            self.layout.sof_2_value.setValue(self.sof_2 * k_opacity)
            self.sof_2_slider.update()
            self.Panel_Update()
    def SOF_2_Slider_Modify(self, SIGNAL_VALUE):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.sof_2 = SIGNAL_VALUE
            self.layout.sof_2_value.setValue(self.sof_2 * k_opacity)
            Krita.instance().activeWindow().activeView().setPaintingOpacity(self.sof_2)
        else:
            self.sof_2 = self.sof_2_lock
            self.sof_2_slider.Update(self.sof_2, self.layout.sof_2_slider.width(), self.gray_natural, self.gray_contrast, self.sof_2_lock)
            self.layout.sof_2_value.setValue(self.sof_2 * k_opacity)
        self.layout.sof_2_slider.update()
        self.layout.sof_2_value.update()
        self.Panel_Update()
    def SOF_2_Value_Modify(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.sof_2 = self.layout.sof_2_value.value() / k_opacity
            self.sof_2_slider.Update(self.sof_2, self.layout.sof_2_slider.width(), self.gray_natural, self.gray_contrast, self.sof_2_lock)
            Krita.instance().activeWindow().activeView().setPaintingOpacity(self.sof_2)
        else:
            self.sof_2 = self.sof_2_lock
            self.sof_2_slider.Update(self.sof_2, self.layout.sof_2_slider.width(), self.gray_natural, self.gray_contrast, self.sof_2_lock)
            self.layout.sof_2_value.setValue(self.sof_2 * k_opacity)
        self.layout.sof_2_slider.update()
        self.layout.sof_2_value.update()
        self.Panel_Update()

    def SOF_3_READ(self, value):
        self.sof_3 = value
        self.sof_3_slider.Update(value, self.layout.sof_3_slider.width(), self.gray_natural, self.gray_contrast, self.sof_3_lock)
        self.layout.sof_3_value.setValue(value * k_flow)
        self.layout.sof_3_slider.update()
        self.layout.sof_3_value.update()
    def SOF_3_Minus(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.sof_3 = self.sof_3 - (unit/k_flow)
            if self.sof_3 <= zero:
                self.sof_3 = zero
            self.sof_3_slider.Update(self.sof_3, self.layout.sof_3_slider.width(), self.gray_natural, self.gray_contrast, self.sof_3_lock)
            self.layout.sof_3_value.setValue(self.sof_3 * k_flow)
            self.sof_3_slider.update()
    def SOF_3_Plus(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.sof_3 = self.sof_3 + (unit/k_flow)
            if self.sof_3 >= unit:
                self.sof_3 = unit
            self.sof_3_slider.Update(self.sof_3, self.layout.sof_3_slider.width(), self.gray_natural, self.gray_contrast, self.sof_3_lock)
            self.layout.sof_3_value.setValue(self.sof_3 * k_flow)
            self.sof_3_slider.update()
    def SOF_3_Slider_Modify(self, SIGNAL_VALUE):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.sof_3 = SIGNAL_VALUE
            self.layout.sof_3_value.setValue(self.sof_3 * k_flow)
            Krita.instance().activeWindow().activeView().setPaintingFlow(self.sof_3)
        else:
            self.sof_3 = self.sof_3_lock
            self.sof_3_slider.Update(self.sof_3, self.layout.sof_3_slider.width(), self.gray_natural, self.gray_contrast, self.sof_3_lock)
            self.layout.sof_3_value.setValue(self.sof_3 * k_flow)
        self.layout.sof_3_slider.update()
        self.layout.sof_3_value.update()
    def SOF_3_Value_Modify(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.sof_3 = self.layout.sof_3_value.value() / k_flow
            self.sof_3_slider.Update(self.sof_3, self.layout.sof_3_slider.width(), self.gray_natural, self.gray_contrast, self.sof_3_lock)
            Krita.instance().activeWindow().activeView().setPaintingFlow(self.sof_3)
        else:
            self.sof_3 = self.sof_3_lock
            self.sof_3_slider.Update(self.sof_3, self.layout.sof_3_slider.width(), self.gray_natural, self.gray_contrast, self.sof_3_lock)
            self.layout.sof_3_value.setValue(self.sof_3 * k_flow)
        self.layout.sof_3_slider.update()
        self.layout.sof_3_value.update()

    # HDR
    def HDR_E_READ(self, value):
        # Variable
        self.hdr_e = round(value, 3)
        # Block Signals
        self.hdr_e_slider.blockSignals(True)
        self.layout.hdr_e_value.blockSignals(True)
        # Widgets
        self.hdr_e_slider.Update(self.range_formating(self.hdr_e, -10, 10, 0, 1), self.layout.hdr_e_slider.width(), self.gray_natural, self.gray_contrast, 0)
        self.layout.hdr_e_value.setValue(value)
        # Block Signals
        self.hdr_e_slider.blockSignals(False)
        self.layout.hdr_e_value.blockSignals(False)
        # Updates
        self.layout.hdr_e_slider.update()
        self.layout.hdr_e_value.update()
    def HDR_E_Minus(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.hdr_e = self.hdr_e - u_exposure
            if self.hdr_e <= -k_exposure:
                self.hdr_e = k_exposure
            self.HDR_E_READ(self.hdr_e)
            Krita.instance().activeWindow().activeView().setHDRExposure(self.hdr_e)
    def HDR_E_Plus(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.hdr_e = self.hdr_e + u_exposure
            if self.hdr_e >= k_exposure:
                self.hdr_e = k_exposure
            self.HDR_E_READ(self.hdr_e)
            Krita.instance().activeWindow().activeView().setHDRExposure(self.hdr_e)
    def HDR_E_Slider_Modify(self, SIGNAL_VALUE):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.hdr_e = self.range_formating(SIGNAL_VALUE, 0, 1, -10, 10)
            self.HDR_E_READ(self.hdr_e)
            Krita.instance().activeWindow().activeView().setHDRExposure(self.hdr_e)
        else:
            self.hdr_e = zero
            self.HDR_E_READ(self.hdr_e)
    def HDR_E_Value_Modify(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.hdr_e = self.layout.hdr_e_value.value()
            self.HDR_E_READ(self.hdr_e)
            Krita.instance().activeWindow().activeView().setHDRExposure(self.hdr_e)
        else:
            self.hdr_e = zero
            self.HDR_E_READ(self.hdr_e)
    def HDR_E_RESET(self):
        self.HDR_E_READ(zero)
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            Krita.instance().activeWindow().activeView().setHDRExposure(zero)

    def HDR_G_READ(self, value):
        # Variable
        self.hdr_g = round(value, 3)
        # Block Signals
        self.hdr_g_slider.blockSignals(True)
        self.layout.hdr_g_value.blockSignals(True)
        # Widgets
        self.hdr_g_slider.Update(value / k_gamma, self.layout.hdr_g_slider.width(), self.gray_natural, self.gray_contrast, 1)
        self.layout.hdr_g_value.setValue(value)
        # Block Signals
        self.hdr_g_slider.blockSignals(False)
        self.layout.hdr_g_value.blockSignals(False)
        # Updates
        self.layout.hdr_g_slider.update()
        self.layout.hdr_g_value.update()
    def HDR_G_Minus(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.hdr_g = self.hdr_g - u_gamma
            if self.hdr_g <= zero:
                self.hdr_g = zero
            self.HDR_G_READ(self.hdr_g)
            Krita.instance().activeWindow().activeView().setHDRGamma(self.hdr_g)
    def HDR_G_Plus(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.hdr_g = self.hdr_g + u_gamma
            if self.hdr_g >= k_gamma:
                self.hdr_g = k_gamma
            self.HDR_G_READ(self.hdr_g)
            Krita.instance().activeWindow().activeView().setHDRGamma(self.hdr_g)
    def HDR_G_Slider_Modify(self, SIGNAL_VALUE):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.hdr_g = SIGNAL_VALUE * k_gamma
            self.HDR_G_READ(self.hdr_g)
            Krita.instance().activeWindow().activeView().setHDRGamma(self.hdr_g)
        else:
            self.hdr_g = unit
            self.HDR_G_READ(self.hdr_g)
    def HDR_G_Value_Modify(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.hdr_g = self.layout.hdr_g_value.value()
            self.HDR_G_READ(self.hdr_g)
            Krita.instance().activeWindow().activeView().setHDRGamma(self.hdr_g)
        else:
            self.hdr_g = unit
            self.HDR_G_READ(self.hdr_g)
    def HDR_G_RESET(self):
        self.HDR_G_READ(unit)
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            Krita.instance().activeWindow().activeView().setHDRGamma(unit)

    # Blend
    def BLEND_READ(self, value):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.vie_blend = value
        else:
            self.vie_blend = "..."
        self.layout.brush_blend.setText(self.vie_blend)
    def BLEND_WRITE(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.vie_blend = self.layout.brush_blend.text()
            try:
                Krita.instance().activeWindow().activeView().setCurrentBlendingMode(self.vie_blend)
            except:
                Krita.instance().activeWindow().activeView().setCurrentBlendingMode("normal")
        else:
            self.vie_blend = "..."
            self.layout.brush_blend.setText(self.vie_blend)

    #//
    #\\ Widget Events ##########################################################
    # Docker Events
    def showEvent(self, event):
        # Layout loads as vertical Size Policy Ignore for correct loading purposes and after the loadding is done I can set it up to the correct Size policy so it works well after, This happens after the init function has ended
        self.window.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.Ratio()
        # Start Timer when the Docker is Present
        if check_timer >= 1:
            self.timer.start()
    def enterEvent(self, event):
        # Check Krita Once before editing Tela
        self.Krita_2_Tela()
        # Confirm Panel
        self.Ratio()
    def leaveEvent(self, event):
        # Clear Text
        self.layout.label.setText("")
        # Save Settings
        self.Default_Save()
    def resizeEvent(self, event):
        # Maintian Ratio
        self.Ratio()
    def closeEvent(self, event):
        # Stop Delta Situation
        self.layout.doc_delta_reference.setChecked(False)
        # Stop QTimer
        if check_timer >= 1:
            self.timer.stop()
        # Save Settings
        self.Default_Save()

    #//
    #\\ Settings ###############################################################
    def Version_Settings(self):
        self.Default_Boot()
        try:
            version = self.Settings_Load_Version()
            if tela_version == version:
                self.Settings_Load_Misc()
        except:
            QtCore.qDebug("Tela - Load Error - Wrong Version")

    def Default_Boot(self):
        # DOCUMENT
        self.GUIDES_Delta_Reference()
        self.layout.gui_sort.setChecked(False)
        self.layout.gui_mirror.setChecked(False)
        self.layout.gui_mirror.setEnabled(False)
        # VIEW
        self.sof_n.Setup_SOF(self.gray_contrast)
        self.SOF_1_READ(self.sof_1)
        self.SOF_2_READ(self.sof_2)
        self.SOF_3_READ(self.sof_3)
        # UI
        self.Menu_Display()
    def Default_Save(self):
        self.Settings_Save_Misc()
        self.Settings_Save_Version()

    def Settings_Load_Version(self):
        try:
            version = Krita.instance().readSetting("Tela", "version", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        except:
            version = "False"
        return version
    def Settings_Save_Version(self):
        Krita.instance().writeSetting("Tela", "version", str(tela_version))

    def Settings_Load_Misc(self):
        try:
            t_string = Krita.instance().readSetting("Tela", "Misc", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            t_split = t_string.split(",")
            # UI
            self.layout.menu.setCurrentIndex(eval(t_split[0]))
            # Locked Values
            self.sof_1_lock = float(t_split[1])
            self.sof_2_lock = float(t_split[2])
            self.sof_3_lock = float(t_split[3])
            self.sof_n.Setup_SOF(self.gray_contrast)
            # Active Values
            self.sof_1 = float(t_split[1])
            self.sof_2 = float(t_split[2])
            self.sof_3 = float(t_split[3])
            self.SOF_1_READ(self.sof_1)
            self.SOF_2_READ(self.sof_2)
            self.SOF_3_READ(self.sof_3)
        except:
            QtCore.qDebug("Tela - Load Error")
    def Settings_Save_Misc(self):
        try:
            # Save Settings
            t_list = (
                str(self.layout.menu.currentIndex()),
                str(self.sof_1_lock),
                str(self.sof_2_lock),
                str(self.sof_3_lock),
                )
            t_string = ','.join(t_list)
            Krita.instance().writeSetting("Tela", "Misc", t_string)
        except:
            pass

    #//
    #\\ Change the Canvas ######################################################
    def canvasChanged(self, canvas):
        # Pop Up Message
        # QMessageBox.information(QWidget(), i18n("Warnning"), i18n("message"))

        # Log Viewer Message
        # QtCore.qDebug("message")
        # QtCore.qWarning("message")
        # QtCore.qCritical("message")
        # self.update()
        pass

    #//
