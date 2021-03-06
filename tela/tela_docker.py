# Tela is a Krita plugin for Quick Settings.
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


#\\ Import Modules #############################################################
# Python Modules
import os
import math
import time
# Krita Modules
from krita import *
# PyQt5 Modules
from PyQt5 import Qt, QtWidgets, QtCore, QtGui, QtSvg, uic
from PyQt5.Qt import Qt
# Tela Modules
from .tela_modulo import (
    Channel_Slider,
    Clicks,
    Panel,
    Record,
    Dialog_UI,
    )
from .tela_extension import TelaExtension

#//
#\\ Global Variables ###########################################################
# Set Window Title Name
DOCKER_NAME = "Tela"
# Timer
check_timer = 50  # 1000 = 1 SECOND (Zero will Disable checks)
# Tela Version Date
tela_version = "2021_09_09"
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
ui_75 = 75
ui_80 = 80
ui_85 = 85
ui_90 = 90
ui_95 = 95
ui_100 = 100
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
# Blends https://invent.kde.org/graphics/krita/-/blob/master/libs/pigment/KoCompositeOpRegistry.h
blends = [
    "normal",
    "erase",
    "in",
    "out",
    "alphadarken",
    "destination-in",
    "destination-atop",

    "xor",
    "or",
    "and",
    "nand",
    "nor",
    "xnor",
    "implication",
    "not_implication",
    "converse",
    "not_converse",

    "plus",
    "minus",
    "add",
    "subtract",
    "inverse_subtract",
    "diff",
    "multiply",
    "divide",
    "arc_tangent",
    "geometric_mean",
    "additive_subtractive",
    "negation",

    "modulo",
    "modulo_continuous",
    "divisive_modulo",
    "divisive_modulo_continuous",
    "modulo_shift",
    "modulo_shift_continuous",

    "equivalence",
    "allanon",
    "parallel",
    "grain_merge",
    "grain_extract",
    "exclusion",
    "hard mix",
    "hard_mix_photoshop",
    "hard_mix_softer_photoshop",
    "overlay",
    "behind",
    "greater",
    "hard overlay",
    "interpolation",
    "interpolation 2x",
    "penumbra a",
    "penumbra b",
    "penumbra c",
    "penumbra d",

    "darken",
    "burn",
    "linear_burn",
    "gamma_dark",
    "shade_ifs_illusions",
    "fog_darken_ifs_illusions",
    "easy burn",

    "lighten",
    "dodge",
    "linear_dodge",
    "screen",
    "hard_light",
    "soft_light_ifs_illusions",
    "soft_light_pegtop_delphi",
    "soft_light",
    "soft_light_svg",
    "gamma_light",
    "gamma_illumination",
    "vivid_light",
    "flat_light",
    "linear light",
    "pin_light",
    "pnorm_a",
    "pnorm_b",
    "super_light",
    "tint_ifs_illusions",
    "fog_lighten_ifs_illusions",
    "easy dodge",
    "luminosity_sai",

    "hue",
    "color",
    "saturation",
    "inc_saturation",
    "dec_saturation",
    "luminize",
    "inc_luminosity",
    "dec_luminosity",

    "hue_hsv",
    "color_hsv",
    "saturation_hsv",
    "inc_saturation_hsv",
    "dec_saturation_hsv",
    "value",
    "inc_value",
    "dec_value",

    "hue_hsl",
    "color_hsl",
    "saturation_hsl",
    "inc_saturation_hsl",
    "dec_saturation_hsl",
    "lightness",
    "inc_lightness",
    "dec_lightness",

    "hue_hsi",
    "color_hsi",
    "saturation_hsi",
    "inc_saturation_hsi",
    "dec_saturation_hsi",
    "intensity",
    "inc_intensity",
    "dec_intensity",

    "copy",
    "copy_red",
    "copy_green",
    "copy_blue",
    "tangent_normalmap",

    "colorize",
    "bumpmap",
    "combine_normal",
    "clear",
    "dissolve",
    "displace",
    "nocomposition",
    "pass through",
    "darker color",
    "lighter color",
    "undefined",

    "reflect",
    "glow",
    "freeze",
    "heat",
    "glow_heat",
    "heat_glow",
    "reflect_freeze",
    "freeze_reflect",
    "heat_glow_freeze_reflect_hybrid"
    ]

#//


class TelaDocker(DockWidget):
    """
    Quick Settings
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
        self.Extension()
        self.Thread_Start()
        self.Pulse()

        # Settings
        self.Version_Settings()

    def Variables(self):
        # Internal
        self.sync = False # Ensures no overlapping sync cycles
        self.ui_mode = [True, False, False, False, False]
        self.timer_state = False
        self.interval = 0.1
        # Active Document
        self.d_cm = None
        self.d_cd = None
        self.d_cp = None
        # Panels
        self.q_image = QImage()
        self.panel_width = 0
        self.panel_height = 0
        # Eraser
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
        self.record_window = False
    def User_Interface(self):
        # Path Name
        self.dir_name = str(os.path.dirname(os.path.realpath(__file__)))
        # Window Title
        self.setWindowTitle(DOCKER_NAME)
        # Tela Widget
        self.window = QWidget()
        self.layout = uic.loadUi(self.dir_name + '/tela_docker.ui', self.window)
        self.setWidget(self.window)
        # Tela Dialog Settings
        self.dialog = Dialog_UI(self)
        self.dialog.accept() # Hides the Dialog
        # Theme Variables
        self.krita_value = 59
        self.krita_contrast = 196
        self.gray_natural = self.HEX_6string(self.krita_value/255,self.krita_value/255,self.krita_value/255)
        self.gray_contrast = self.HEX_6string(self.krita_contrast/255,self.krita_contrast/255,self.krita_contrast/255)
    def Connects(self):
        #\\ MENU ###############################################################
        self.layout.check.stateChanged.connect(self.Krita_TIMER)
        self.layout.dialog.clicked.connect(self.Menu_DIALOG)
        self.dialog.panel.toggled.connect(self.Menu_PANEL)
        self.dialog.brush.toggled.connect(self.Menu_BRUSH)
        self.dialog.canvas.toggled.connect(self.Menu_CANVAS)
        self.dialog.document.toggled.connect(self.Menu_DOCUMENT)
        self.dialog.guides.toggled.connect(self.Menu_GUIDES)

        #//
        #\\ PANEL ##############################################################
        self.panel = Panel(self.layout.panel)
        self.panel.SIGNAL_ROTATE.connect(self.Panel_Rotation)
        # self.panel.SIGNAL_SOF.connect(self.Panel_SOF)

        #//
        #\\ BRUSH ##############################################################
        # Blend
        self.layout.brush_blend.returnPressed.connect(self.BLEND_WRITE)
        # Text Completer
        completer = QCompleter(blends)
        self.layout.brush_blend.setCompleter(completer)

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

        #//
        #\\ CANVAS #############################################################
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

        # Check Boxes
        self.layout.can_mirror.toggled.connect(self.CANVAS_Mirror_TOGGLE)
        self.layout.can_wrap.toggled.connect(self.CANVAS_Wrap_TOGGLE)

        #//
        #\\ DOCUMENT ###########################################################
        self.layout.doc_width.editingFinished.connect(self.DOC_Width_WRITE)
        self.layout.doc_height.editingFinished.connect(self.DOC_Height_WRITE)
        self.layout.doc_resolution.editingFinished.connect(self.DOC_Resolution_WRITE)
        self.layout.doc_delta_reference.toggled.connect(self.GUIDES_Delta_Reference)
        self.layout.doc_delta_up.valueChanged.connect(self.GUIDES_Delta)
        self.layout.doc_delta_left.valueChanged.connect(self.GUIDES_Delta)
        self.layout.doc_delta_right.valueChanged.connect(self.GUIDES_Delta)
        self.layout.doc_delta_down.valueChanged.connect(self.GUIDES_Delta)

        #//
        #\\ GUIDES #############################################################
        self.layout.gui_horizontal_group.itemDoubleClicked.connect(self.GUIDES_Horizontal_EDIT)
        self.layout.gui_vertical_group.itemDoubleClicked.connect(self.GUIDES_Vertical_EDIT)
        self.layout.gui_mirror.toggled.connect(self.GUIDES_Mirror)
        self.layout.gui_sort.toggled.connect(self.GUIDES_Sort)
        self.layout.gui_visible.toggled.connect(self.GUIDES_Visible_WRITE)
        self.layout.gui_lock.toggled.connect(self.GUIDES_Lock_WRITE)

        #//
        #\\ RECORD #############################################################
        self.dialog.preview_interval.valueChanged.connect(self.Preview_Interval)
        self.layout.record_window.toggled.connect(self.Record_Window)

        #//
    def Style_Widget(self):
        # BRUSH
        self.layout.sof_n.setStyleSheet(bg_alpha)
        self.layout.sof_1_slider.setStyleSheet(bg_alpha)
        self.layout.sof_2_slider.setStyleSheet(bg_alpha)
        self.layout.sof_3_slider.setStyleSheet(bg_alpha)
        self.layout.hdr_e_slider.setStyleSheet(bg_alpha)
        self.layout.hdr_g_slider.setStyleSheet(bg_alpha)
        # CANVAS
        self.layout.panel.setStyleSheet(bg_alpha)
        self.layout.can_rotation_slider.setStyleSheet(bg_alpha)
        self.layout.can_zoom_slider.setStyleSheet(bg_alpha)

        # Icons Module
        self.icon_corner = self.Icon_Corner(self.gray_contrast)
        self.svg_ui = QtSvg.QSvgWidget(self.layout.dialog)
        self.svg_ui.load(self.icon_corner)
    def Extension(self):
        # Install Extension for Tela Docker
        extension = TelaExtension(parent=Krita.instance())
        Krita.instance().addExtension(extension)
        # Connect Extension Signals
        extension.SIGNAL_KEY.connect(self.Tela_Key)
        extension.SIGNAL_HUD.connect(self.Tela_HUD)
    def Thread_Start(self):
        self.thread = Image()
        self.thread.SIGNAL_IMAGE['QImage'].connect(self.Thread_Image)
        self.thread.Active(True)
        self.thread.start()
    def Pulse(self):
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
    #\\ Menu Displays ##########################################################
    # Dialog
    def Menu_DIALOG(self):
        self.dialog.show()
    # Menus
    def Menu_PANEL(self):
        font = self.dialog.panel.font()
        self.ui_mode[0] = self.dialog.panel.isChecked()
        if self.ui_mode[0] == True:
            self.dialog.panel.setText("[PANEL]")
            self.thread.Active(True)
            self.thread.start()
            font.setBold(True)
        else:
            self.dialog.panel.setText("PANEL")
            self.thread.Active(False)
            font.setBold(False)
        self.dialog.panel.setFont(font)
        self.Adjust_Spacing()
    def Menu_BRUSH(self):
        font = self.dialog.brush.font()
        self.ui_mode[1] = self.dialog.brush.isChecked()
        if self.ui_mode[1] == True:
            self.dialog.brush.setText("[BRUSH]")
            font.setBold(True)

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

            self.layout.channels_sof.setContentsMargins(zero,unit,zero,zero)
            self.layout.channels_sof.setSpacing(unit)
        else:
            self.dialog.brush.setText("BRUSH")
            font.setBold(False)

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

            self.layout.channels_sof.setContentsMargins(zero,zero,zero,zero)
            self.layout.channels_sof.setSpacing(zero)
        self.dialog.brush.setFont(font)
        self.Adjust_Spacing()
    def Menu_CANVAS(self):
        font = self.dialog.canvas.font()
        self.ui_mode[2] = self.dialog.canvas.isChecked()
        if self.ui_mode[2] == True:
            self.dialog.canvas.setText("[CANVAS]")
            font.setBold(True)

            self.layout.can_rotation_slider.setMinimumHeight(ui_10)
            self.layout.can_rotation_slider.setMaximumHeight(ui_20)
            self.layout.can_rotation_value.setMinimumHeight(ui_10)
            self.layout.can_rotation_value.setMaximumHeight(ui_20)

            self.layout.can_zoom_slider.setMinimumHeight(ui_10)
            self.layout.can_zoom_slider.setMaximumHeight(ui_20)
            self.layout.can_zoom_value.setMinimumHeight(ui_10)
            self.layout.can_zoom_value.setMaximumHeight(ui_20)

            self.layout.hdr_e_slider.setMinimumHeight(ui_10)
            self.layout.hdr_e_slider.setMaximumHeight(ui_20)
            self.layout.hdr_e_value.setMinimumHeight(ui_10)
            self.layout.hdr_e_value.setMaximumHeight(ui_20)

            self.layout.hdr_g_slider.setMinimumHeight(ui_10)
            self.layout.hdr_g_slider.setMaximumHeight(ui_20)
            self.layout.hdr_g_value.setMinimumHeight(ui_10)
            self.layout.hdr_g_value.setMaximumHeight(ui_20)

            self.layout.can_mirror.setMinimumHeight(ui_10)
            self.layout.can_mirror.setMaximumHeight(ui_20)
            self.layout.can_wrap.setMinimumHeight(ui_10)
            self.layout.can_wrap.setMaximumHeight(ui_20)

            self.layout.canvas_transform.setContentsMargins(zero,unit,zero,zero)
            self.layout.canvas_transform.setSpacing(unit)
            self.layout.channels_hdr.setContentsMargins(zero,unit,zero,zero)
            self.layout.channels_hdr.setSpacing(unit)
            self.layout.canvas_checks.setContentsMargins(zero,unit,zero,zero)
            self.layout.canvas_checks.setSpacing(unit)
        else:
            self.dialog.canvas.setText("CANVAS")
            font.setBold(False)

            self.layout.can_rotation_slider.setMinimumHeight(zero)
            self.layout.can_rotation_slider.setMaximumHeight(zero)
            self.layout.can_rotation_value.setMinimumHeight(zero)
            self.layout.can_rotation_value.setMaximumHeight(zero)

            self.layout.can_zoom_slider.setMinimumHeight(zero)
            self.layout.can_zoom_slider.setMaximumHeight(zero)
            self.layout.can_zoom_value.setMinimumHeight(zero)
            self.layout.can_zoom_value.setMaximumHeight(zero)

            self.layout.hdr_e_slider.setMinimumHeight(zero)
            self.layout.hdr_e_slider.setMaximumHeight(zero)
            self.layout.hdr_e_value.setMinimumHeight(zero)
            self.layout.hdr_e_value.setMaximumHeight(zero)

            self.layout.hdr_g_slider.setMinimumHeight(zero)
            self.layout.hdr_g_slider.setMaximumHeight(zero)
            self.layout.hdr_g_value.setMinimumHeight(zero)
            self.layout.hdr_g_value.setMaximumHeight(zero)

            self.layout.can_mirror.setMinimumHeight(zero)
            self.layout.can_mirror.setMaximumHeight(zero)
            self.layout.can_wrap.setMinimumHeight(zero)
            self.layout.can_wrap.setMaximumHeight(zero)

            self.layout.canvas_transform.setContentsMargins(zero,zero,zero,zero)
            self.layout.canvas_transform.setSpacing(zero)
            self.layout.channels_hdr.setContentsMargins(zero,zero,zero,zero)
            self.layout.channels_hdr.setSpacing(zero)
            self.layout.canvas_checks.setContentsMargins(zero,zero,zero,zero)
            self.layout.canvas_checks.setSpacing(zero)
        self.dialog.canvas.setFont(font)
        self.Adjust_Spacing()
    def Menu_DOCUMENT(self):
        font = self.dialog.document.font()
        self.ui_mode[3] = self.dialog.document.isChecked()
        if self.ui_mode[3] == True:
            self.dialog.document.setText("[DOCUMENT]")
            font.setBold(True)

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

            self.layout.document_layout.setContentsMargins(zero,unit,zero,zero)
            self.layout.document_layout.setSpacing(unit)
        else:
            self.dialog.document.setText("DOCUMENT")
            font.setBold(False)

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

            self.layout.document_layout.setContentsMargins(zero,zero,zero,zero)
            self.layout.document_layout.setSpacing(zero)
        self.dialog.document.setFont(font)
        self.Adjust_Spacing()
    def Menu_GUIDES(self):
        font = self.dialog.guides.font()
        self.ui_mode[4] = self.dialog.guides.isChecked()
        if self.ui_mode[4] == True:
            self.dialog.guides.setText("[GUIDES]")
            font.setBold(True)

            self.layout.gui_horizontal_label.setMinimumHeight(ui_10)
            self.layout.gui_horizontal_label.setMaximumHeight(ui_20)
            self.layout.gui_vertical_label.setMinimumHeight(ui_10)
            self.layout.gui_vertical_label.setMaximumHeight(ui_20)
            self.layout.gui_horizontal_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)
            self.layout.gui_vertical_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)
            self.layout.gui_horizontal_group.setMinimumHeight(zero)
            self.layout.gui_horizontal_group.setMaximumHeight(ui_100)
            self.layout.gui_vertical_group.setMinimumHeight(zero)
            self.layout.gui_vertical_group.setMaximumHeight(ui_100)

            self.layout.gui_sort.setMinimumHeight(ui_10)
            self.layout.gui_sort.setMaximumHeight(ui_20)
            self.layout.gui_mirror.setMinimumHeight(ui_10)
            self.layout.gui_mirror.setMaximumHeight(ui_20)
            self.layout.gui_visible.setMinimumHeight(ui_10)
            self.layout.gui_visible.setMaximumHeight(ui_20)
            self.layout.gui_lock.setMinimumHeight(ui_10)
            self.layout.gui_lock.setMaximumHeight(ui_20)

            self.layout.guides_group.setContentsMargins(zero,unit,zero,zero)
            self.layout.guides_group.setSpacing(unit)
            self.layout.guides_options.setContentsMargins(zero,unit,zero,zero)
            self.layout.guides_options.setSpacing(unit)
        else:
            self.dialog.guides.setText("GUIDES")
            font.setBold(False)

            self.layout.gui_horizontal_label.setMinimumHeight(zero)
            self.layout.gui_horizontal_label.setMaximumHeight(zero)
            self.layout.gui_vertical_label.setMinimumHeight(zero)
            self.layout.gui_vertical_label.setMaximumHeight(zero)
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

            self.layout.guides_group.setContentsMargins(zero,zero,zero,zero)
            self.layout.guides_group.setSpacing(zero)
            self.layout.guides_options.setContentsMargins(zero,zero,zero,zero)
            self.layout.guides_options.setSpacing(zero)
        self.dialog.guides.setFont(font)
        self.Adjust_Spacing()
    # Vertical Spacer
    def Adjust_Spacing(self):
        panel = self.dialog.panel.isChecked()
        guides = self.dialog.guides.isChecked()
        # Adjust Vertical Spacer
        if (panel == True and guides == False):
            # Panel
            self.layout.panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)
            # Guides
            self.layout.gui_horizontal_group.setMinimumHeight(zero)
            self.layout.gui_horizontal_group.setMaximumHeight(zero)
            self.layout.gui_horizontal_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            self.layout.gui_vertical_group.setMinimumHeight(zero)
            self.layout.gui_vertical_group.setMaximumHeight(zero)
            self.layout.gui_vertical_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            # Spacer
            self.layout.vertical_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        if (panel == False and guides == True):
            # Panel
            self.layout.panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            # Guides
            self.layout.gui_horizontal_group.setMinimumHeight(zero)
            self.layout.gui_horizontal_group.setMaximumHeight(max_val)
            self.layout.gui_horizontal_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)
            self.layout.gui_vertical_group.setMinimumHeight(zero)
            self.layout.gui_vertical_group.setMaximumHeight(max_val)
            self.layout.gui_vertical_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)
            # Spacer
            self.layout.vertical_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        if (panel == True and guides == True):
            # Panel
            self.layout.panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)
            # Guides
            self.layout.gui_horizontal_group.setMinimumHeight(zero)
            self.layout.gui_horizontal_group.setMaximumHeight(max_val)
            self.layout.gui_horizontal_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)
            self.layout.gui_vertical_group.setMinimumHeight(zero)
            self.layout.gui_vertical_group.setMaximumHeight(max_val)
            self.layout.gui_vertical_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)
            # Spacer
            self.layout.vertical_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        if (panel == False and guides == False):
            # Panel
            self.layout.panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            # Guides
            self.layout.gui_horizontal_group.setMinimumHeight(zero)
            self.layout.gui_horizontal_group.setMaximumHeight(zero)
            self.layout.gui_horizontal_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            self.layout.gui_vertical_group.setMinimumHeight(zero)
            self.layout.gui_vertical_group.setMaximumHeight(zero)
            self.layout.gui_vertical_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            # Spacer
            self.layout.vertical_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)
        self.update()
    # Handles
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
    # Record
    def Preview_Interval(self):
        self.interval = self.dialog.preview_interval.value()
    def Record_Window(self):
        self.record_window = self.layout.record_window.isChecked()
        if self.record_window == True:
            self.record = Record()
            self.record.SIGNAL_CLOSE.connect(self.Record_Close)
            self.Panel_Update()
        else:
            self.record.Close()
            self.record.SIGNAL_CLOSE.disconnect(self.Record_Close)

    #//
    #\\ Conversions ############################################################
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
        tela_hex = str("#"+hex1+hex2+hex3)
        return tela_hex
    # Trignometry
    def Math_2D_Points_Distance(self, x1, y1, x2, y2):
        dd = math.sqrt( math.pow((x1-x2),2) + math.pow((y1-y2),2) )
        return dd
    def Math_2D_Points_Lines_Intersection(self, x1, y1, x2, y2, x3, y3, x4, y4):
        try:
            xx = ((x2*y1-x1*y2)*(x4-x3)-(x4*y3-x3*y4)*(x2-x1)) / ((x2-x1)*(y4-y3)-(x4-x3)*(y2-y1))
            yy = ((x2*y1-x1*y2)*(y4-y3)-(x4*y3-x3*y4)*(y2-y1)) / ((x2-x1)*(y4-y3)-(x4-x3)*(y2-y1))
        except:
            xx = 0
            yy = 0
        return xx, yy
    def Math_2D_Points_Lines_Angle(self, x1, y1, x2, y2, x3, y3):
        v1 = (x1-x2, y1-y2)
        v2 = (x3-x2, y3-y2)
        v1_theta = math.atan2(v1[1], v1[0])
        v2_theta = math.atan2(v2[1], v2[0])
        angle = (v2_theta - v1_theta) * (180.0 / math.pi)
        if angle < 0:
            angle += 360.0
        return angle

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
                font.setBold(True)
                self.layout.check.setText("DIS")
                self.Krita_2_Tela()
                self.timer.start()
        else:
            font.setBold(False)
            self.layout.check.setText("C<1")
            self.layout.check.setEnabled(False)
        self.Panel_Update()
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
                if (self.timer_state == 1 or self.timer_state == 2):
                    try: # To avoid the window change error miss match
                        # Eraser
                        self.eraser = Krita.instance().action("erase_action").isChecked()

                        # Krita instance Classes
                        c = Krita.instance().activeWindow().activeView().canvas()
                        ad = Krita.instance().activeDocument()
                        av = Krita.instance().activeWindow().activeView()

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
                        # Read View
                        vie_size = av.brushSize()
                        vie_opacity = av.paintingOpacity()
                        vie_flow = av.paintingFlow()
                        vie_exposure = av.HDRExposure()
                        vie_gamma = av.HDRGamma()
                        vie_blend = av.currentBlendingMode()

                        # Update Active Document
                        self.d_cm = Krita.instance().activeDocument().colorModel()
                        self.d_cd = Krita.instance().activeDocument().colorDepth()
                        self.d_cp = Krita.instance().activeDocument().colorProfile()
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
                            else:
                                self.GUIDES_Horizontal_LIST_NOR()
                            self.gui_hor_previous = self.gui_hor_norm
                        if self.gui_ver_previous != gui_ver:
                            self.gui_ver_norm = gui_ver
                            if self.ui_d_ref == True:
                                self.GUIDES_Vertical_LIST_REF()
                            else:
                                self.GUIDES_Vertical_LIST_NOR()
                            self.gui_ver_previous = self.gui_ver_norm
                        if self.ui_g_visible != ui_g_visible:
                            self.GUIDES_Visible_READ(ui_g_visible)
                        if self.ui_g_lock != ui_g_lock:
                            self.GUIDES_Lock_READ(ui_g_lock)
                        # Update View
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

                        # Update Panel
                        self.Panel_Update()
                    except:
                        self.Default_Values()
                        self.Panel_Update()
                else:
                    self.Panel_Update()
            else:
                self.Default_Values()
                self.Panel_Update()

            # Sync Control Variable
            self.sync = False
    def Default_Values(self):
        self.eraser = False
        # Document
        self.d_cm = None
        self.d_cd = None
        self.d_cp = None
        # Canvas
        if self.can_rotation != 0:
            self.CANVAS_Rotation_READ(0)
        if self.can_zoom != 1:
            self.CANVAS_Zoom_READ(1)
        if self.can_mirror != 0:
            self.CANVAS_Mirror_READ(0)
        if self.can_wrap != 0:
            self.CANVAS_Wrap_READ(0)
        # Document
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
        #View
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

    #//
    #\\ PANEL ##################################################################
    def Panel_Update(self):
        # Calculations
        self.Panel_Calculations()
        # Panel Values
        if self.ui_mode[0] == True:
            if ((self.canvas() is not None) and (self.canvas().view() is not None)):
                self.panel.Update_Panel(
                    self.timer_state, self.q_image,
                    self.eraser,
                    self.sof_1, self.sof_2, self.sof_3,
                    self.can_rotation, self.can_zoom,
                    self.hdr_e, self.hdr_g,
                    self.can_mirror, self.can_wrap,
                    self.doc_width, self.doc_height,

                    self.angle, self.size,
                    self.doc_p1_x, self.doc_p1_y,
                    self.doc_p2_x, self.doc_p2_y,
                    self.doc_p3_x, self.doc_p3_y,
                    self.doc_p4_x, self.doc_p4_y,
                    self.width, self.height,

                    self.ui_d_ref, self.delta_new,
                    self.gui_hor_norm, self.gui_ver_norm,
                    self.panel_width, self.panel_height,
                    self.gray_natural, self.gray_contrast,
                    )
            else:
                self.Panel_Default()
        else:
            self.Panel_Default()
        self.layout.panel.update()

        # QImage Variables Update
        if self.timer_state == 1:
            if ((self.canvas() is not None) and (self.canvas().view() is not None)):
                self.thread.Variables(self.d_cm, self.timer_state, self.width, self.height, self.doc_width, self.doc_height, self.interval)
            else: # No Active Document
                self.thread.Variables(None, 0, 1, 1, 1, 1, self.interval)
        else: # selftimer_state = 0 or 1
            self.thread.Variables(None, 0, 1, 1, 1, 1, self.interval)
        # Record Window Update
        if self.record_window == True:
            self.record.Update(self.doc_width, self.doc_height, self.q_image)
    def Panel_Calculations(self):
        # Panel Size
        self.panel_width = self.layout.panel.width()
        self.panel_height = self.layout.panel.height()

        # Correct Canvas so no division by Zero
        if self.doc_width <= 0:
            self.doc_width = 1
        if self.doc_height <= 0:
            self.doc_height = 1

        # Calculations (size of canvas)
        self.angle = self.Math_2D_Points_Lines_Angle(self.doc_width,0, 0,0, self.doc_width,self.doc_height)
        # Canvas Size
        margin = 5
        if self.panel_width <= self.panel_height:
            self.size = self.panel_width-(2*margin)
        if self.panel_width > self.panel_height:
            self.size = self.panel_height-(2*margin)
        # Canvas Points
        self.doc_p1_x = (self.panel_width*0.5) - ((self.size*0.5) * math.cos(math.radians(self.angle+self.can_rotation)))
        self.doc_p1_y = (self.panel_height*0.5) - ((self.size*0.5) * math.sin(math.radians(self.angle+self.can_rotation)))
        self.doc_p2_x = (self.panel_width*0.5) - ((self.size*0.5) * math.cos(math.radians(180-self.angle+self.can_rotation)))
        self.doc_p2_y = (self.panel_height*0.5) - ((self.size*0.5) * math.sin(math.radians(180-self.angle+self.can_rotation)))
        self.doc_p3_x = (self.panel_width*0.5) - ((self.size*0.5) * math.cos(math.radians(180+self.angle+self.can_rotation)))
        self.doc_p3_y = (self.panel_height*0.5) - ((self.size*0.5) * math.sin(math.radians(180+self.angle+self.can_rotation)))
        self.doc_p4_x = (self.panel_width*0.5) - ((self.size*0.5) * math.cos(math.radians(-self.angle+self.can_rotation)))
        self.doc_p4_y = (self.panel_height*0.5) - ((self.size*0.5) * math.sin(math.radians(-self.angle+self.can_rotation)))

        # QImage Scale Calculations
        dw = self.Math_2D_Points_Distance(self.doc_p1_x,self.doc_p1_y, self.doc_p2_x,self.doc_p2_y)
        six = (dw / self.doc_width)
        self.width = self.doc_width * six
        dh = self.Math_2D_Points_Distance(self.doc_p1_x,self.doc_p1_y, self.doc_p3_x,self.doc_p3_y)
        siy = (dh / self.doc_height)
        self.height = self.doc_height * siy
    def Panel_Default(self):
        self.panel.Update_Panel(
            False, self.q_image,
            False,
            0.04, 1, 1,
            0, 1,
            0, 1,
            False, False,
            1, 1,

            self.angle, self.size,
            self.doc_p1_x, self.doc_p1_y,
            self.doc_p2_x, self.doc_p2_y,
            self.doc_p3_x, self.doc_p3_y,
            self.doc_p4_x, self.doc_p4_y,
            self.width, self.height,

            False, [0,0,0,0],
            [], [],
            self.panel_width, self.panel_height,
            '#383838', '#d4d4d4',
            )
    # Signals
    def Panel_SOF(self, SIGNAL_SOF):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            if self.timer_state != 0:
                """
                # Size
                self.sof_1 = SIGNAL_PANEL[0] * k_size
                self.sof_1_slider.Update(self.lin_to_cir(self.sof_1 / k_size), self.layout.sof_1_slider.width(), self.gray_natural, self.gray_contrast, self.sof_1_lock)
                self.layout.sof_1_value.setValue(self.sof_1)
                Krita.instance().activeWindow().activeView().setBrushSize(self.sof_1)
                """
                # Opacity
                self.sof_2 = SIGNAL_PANEL[1]
                self.sof_2_slider.Update(self.sof_2, self.layout.sof_2_slider.width(), self.gray_natural, self.gray_contrast, self.sof_2_lock)
                self.layout.sof_2_value.setValue(self.sof_2 * k_opacity)
                Krita.instance().activeWindow().activeView().setPaintingOpacity(self.sof_2)
                # Flow
                self.sof_3 = SIGNAL_PANEL[2]
                self.sof_3_slider.Update(self.sof_3, self.layout.sof_3_slider.width(), self.gray_natural, self.gray_contrast, self.sof_3_lock)
                self.layout.sof_3_value.setValue(self.sof_3 * k_flow)
                Krita.instance().activeWindow().activeView().setPaintingFlow(self.sof_3)
    def Panel_Rotation(self, SIGNAL_ROTATE):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            if self.timer_state != 0:
                self.can_rotation = SIGNAL_ROTATE * k_rotation
                self.CANVAS_Rotation_READ(self.can_rotation)
                Krita.instance().activeWindow().activeView().canvas().setRotation(self.Rotation_Send(self.can_rotation))
            else:
                self.can_rotation = zero
                self.CANVAS_Rotation_READ(self.can_rotation)
        else:
            self.can_rotation = zero
            self.CANVAS_Rotation_READ(self.can_rotation)

    #//
    #\\ BRUSH (VIEW) ###########################################################
    # Blend
    def BLEND_READ(self, value):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.vie_blend = value
        else:
            self.vie_blend = "..."
        self.layout.brush_blend.setText(self.vie_blend)
    def BLEND_WRITE(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            # Read user input
            self.vie_blend = self.layout.brush_blend.text()
            # Check if Input is Valid
            check = "normal"
            for i in range(0, len(blends)):
                if blends[i] == str(self.vie_blend):
                    check = blends[i]
            # Apply Blend Mode
            Krita.instance().activeWindow().activeView().setCurrentBlendingMode(check)
            # Clear Focus to not have a stuck cursor
            self.layout.brush_blend.clearFocus()
        else:
            self.vie_blend = "..."
            self.layout.brush_blend.setText(self.vie_blend)

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
    def SOF_1_Minus(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.sof_1 = self.sof_1 - 1
            if self.sof_1 <= zero:
                self.sof_1 = zero
            self.sof_1_slider.Update(self.lin_to_cir(self.sof_1 / k_size), self.layout.sof_1_slider.width(), self.gray_natural, self.gray_contrast, self.sof_1_lock)
            self.layout.sof_1_value.setValue(self.sof_1)
            self.sof_1_slider.update()
    def SOF_1_Plus(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.sof_1 = self.sof_1 + 1
            if self.sof_1 >= k_size:
                self.sof_1 = k_size
            self.sof_1_slider.Update(self.lin_to_cir(self.sof_1 / k_size), self.layout.sof_1_slider.width(), self.gray_natural, self.gray_contrast, self.sof_1_lock)
            self.layout.sof_1_value.setValue(self.sof_1)
            self.sof_1_slider.update()
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

    def SOF_2_READ(self, value):
        self.sof_2 = value
        self.sof_2_slider.Update(value, self.layout.sof_2_slider.width(), self.gray_natural, self.gray_contrast, self.sof_2_lock)
        self.layout.sof_2_value.setValue(value * k_opacity)
        self.layout.sof_2_slider.update()
        self.layout.sof_2_value.update()
    def SOF_2_Minus(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.sof_2 = self.sof_2 - (unit/k_opacity)
            if self.sof_2 <= zero:
                self.sof_2 = zero
            self.sof_2_slider.Update(self.sof_2, self.layout.sof_2_slider.width(), self.gray_natural, self.gray_contrast, self.sof_2_lock)
            self.layout.sof_2_value.setValue(self.sof_2 * k_opacity)
            self.sof_2_slider.update()
    def SOF_2_Plus(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.sof_2 = self.sof_2 + (unit/k_opacity)
            if self.sof_2 >= unit:
                self.sof_2 = unit
            self.sof_2_slider.Update(self.sof_2, self.layout.sof_2_slider.width(), self.gray_natural, self.gray_contrast, self.sof_2_lock)
            self.layout.sof_2_value.setValue(self.sof_2 * k_opacity)
            self.sof_2_slider.update()
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

    #//
    #\\ CANVAS (CANVAS/VIEW/CANVAS) ############################################
    # Canvas
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

    # View
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

    # Canvas
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
    #\\ DOCUMENT (DOCUMENT) ####################################################
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

    #//
    #\\ GUIDES (DOCUMENT) ######################################################
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
            if self.sync == False:
                # Sync Control Variable
                self.sync = True

                # Safe guard Guides
                ad = Krita.instance().activeDocument()
                gui_hor = ad.horizontalGuides()
                gui_ver = ad.verticalGuides()
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
                    self.delta_new[2], # right???
                    self.delta_new[3], # down
                    ]

                # Clear Lists
                self.layout.gui_horizontal_group.clear()
                self.layout.gui_vertical_group.clear()
                # Correct Guide List
                for i in range(0, len(gui_hor)):
                    gui_hor[i] = gui_hor[i] - du
                    self.layout.gui_horizontal_group.insertItem(i, str(int(gui_hor[i])))
                for y in range(0, len(gui_ver)):
                    gui_ver[y] = gui_ver[y] - dl
                    self.layout.gui_vertical_group.insertItem(y, str(int(gui_ver[y])))
                # Apply Guides
                Krita.instance().activeDocument().setHorizontalGuides(gui_hor)
                Krita.instance().activeDocument().setVerticalGuides(gui_ver)

                # Sync Control Variable
                self.sync = False

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
    #\\ Module Signals #########################################################
    # Thread
    def Thread_Image(self, q_image):
        self.q_image = q_image
    # Record Window
    def Record_Close(self, SIGNAL_CLOSE):
        self.layout.record_window.setChecked(False)
    # Extension
    def Tela_Key(self, SIGNAL_KEY):
        if SIGNAL_KEY == "Size Minus":
            self.SOF_1_Minus()
        if SIGNAL_KEY == "Size Plus":
            self.SOF_1_Plus()

        if SIGNAL_KEY == "Opacity Minus":
            self.SOF_2_Minus()
        if SIGNAL_KEY == "Opacity Plus":
            self.SOF_2_Plus()

        if SIGNAL_KEY == "Flow Minus":
            self.SOF_3_Minus()
        if SIGNAL_KEY == "Flow Plus":
            self.SOF_3_Plus()

        if SIGNAL_KEY == "Rotation Minus":
            self.CANVAS_Rotation_Minus()
        if SIGNAL_KEY == "Rotation Plus":
            self.CANVAS_Rotation_Plus()

        if SIGNAL_KEY == "Zoom Minus":
            self.CANVAS_Zoom_Minus()
        if SIGNAL_KEY == "Zoom Plus":
            self.CANVAS_Zoom_Plus()

        if SIGNAL_KEY == "Exposure Minus":
            self.HDR_E_Minus()
        if SIGNAL_KEY == "Exposure Plus":
            self.HDR_E_Plus()

        if SIGNAL_KEY == "Gamma Minus":
            self.HDR_G_Minus()
        if SIGNAL_KEY == "Gamma Plus":
            self.HDR_G_Plus()
    def Tela_HUD(self, SIGNAL_HUD):
        pass

    #//
    #\\ Style ##################################################################
    # Icons
    def Icon_Corner(self, hex):
        string = str(
        "<svg width=\"20\" height=\"20\" viewBox=\"0 0 5.2916666 5.2916666\" version=\"1.1\"> \n" +
        "  <g \n" +
        "     inkscape:label=\"Layer 1\" inkscape:groupmode=\"layer\" id=\"layer1\"> \n" +
        "    <path \n" +
        "       style=\"fill:"+hex+";fill-opacity:1;stroke:none;stroke-width:0.264583px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1\" \n" +
        "       d=\"M 1.3229166,3.9687499 H 3.9687499 V 1.3229166 Z\" \n" +
        "       id=\"path281\" \n" +
        "       inkscape:label=\"tri\" /> \n" +
        "  </g> \n" +
        "</svg> "
        )
        array = bytearray(string, encoding='utf-8')
        return array

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
        # QTimer
        if check_timer >= 1:
            self.timer.start()
    def leaveEvent(self, event):
        # Save Settings
        self.Default_Save()
        # Clear Text
        self.layout.label.setText("")
    def resizeEvent(self, event):
        # Maintian Ratio
        self.Ratio()
    def closeEvent(self, event):
        # Stop Delta Situation
        self.layout.doc_delta_reference.setChecked(False)
        # Stop QTimer
        if check_timer >= 1:
            self.timer.stop()
        # Stop Thread
        self.thread.Active(False)
        # Record Window Close
        try:
            self.record.Close()
        except:
            pass
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
                self.Settings_Load_UI()
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
        self.dialog.panel.setChecked(True)
        self.dialog.brush.setChecked(False)
        self.dialog.canvas.setChecked(False)
        self.dialog.document.setChecked(False)
        self.dialog.guides.setChecked(False)
        self.Menu_PANEL()
        self.Menu_BRUSH()
        self.Menu_CANVAS()
        self.Menu_DOCUMENT()
        self.Menu_GUIDES()
        # Dialog
        self.dialog.preview_interval.setValue(self.interval)
        self.record_window = False
    def Default_Save(self):
        self.Settings_Save_Misc()
        self.Settings_Save_UI()
        self.Settings_Save_Version()

    def Settings_Load_Version(self):
        try:
            version = Krita.instance().readSetting("Tela", "version", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        except:
            version = "False"
        return version
    def Settings_Save_Version(self):
        Krita.instance().writeSetting("Tela", "version", str(tela_version))

    def Settings_Load_UI(self):
        try:
            ui_string = Krita.instance().readSetting("Tela", "UI", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            ui_split = ui_string.split(",")
            self.dialog.panel.setChecked(eval(ui_split[0]))
            self.dialog.brush.setChecked(eval(ui_split[1]))
            self.dialog.canvas.setChecked(eval(ui_split[2]))
            self.dialog.document.setChecked(eval(ui_split[3]))
            self.dialog.guides.setChecked(eval(ui_split[4]))
            self.dialog.preview_interval.setValue(eval(ui_split[5]))
        except:
            QtCore.qWarning("Tela - Load Error - UI")
    def Settings_Save_UI(self):
        ui_list = (
            str(self.dialog.panel.isChecked()),
            str(self.dialog.brush.isChecked()),
            str(self.dialog.canvas.isChecked()),
            str(self.dialog.document.isChecked()),
            str(self.dialog.guides.isChecked()),
            str(self.dialog.preview_interval.value()),
            )
        ui_string = ','.join(ui_list)
        Krita.instance().writeSetting("Tela", "UI", ui_string)

    def Settings_Load_Misc(self):
        try:
            t_string = Krita.instance().readSetting("Tela", "Misc", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            t_split = t_string.split(",")
            # Locked Values
            self.sof_1_lock = float(t_split[0])
            self.sof_2_lock = float(t_split[1])
            self.sof_3_lock = float(t_split[2])
            self.sof_n.Setup_SOF(self.gray_contrast)
            # Active Values
            self.sof_1 = float(t_split[0])
            self.sof_2 = float(t_split[1])
            self.sof_3 = float(t_split[2])
            self.SOF_1_READ(self.sof_1)
            self.SOF_2_READ(self.sof_2)
            self.SOF_3_READ(self.sof_3)
        except:
            QtCore.qDebug("Tela - Load Error")
    def Settings_Save_Misc(self):
        try:
            # Save Settings
            t_list = (
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
        pass

    #//
    #\\ Notes ##################################################################
    # Pop Up Message
    # QMessageBox.information(QWidget(), i18n("Warnning"), i18n("message"))

    # Log Viewer Message
    # QtCore.qDebug("message")
    # QtCore.qWarning("message")
    # QtCore.qCritical("message")
    # self.update()

    #//


class Image(QThread):
    SIGNAL_IMAGE = QtCore.pyqtSignal(QImage)

    #\\ Thread #################################################################
    def __init__(self, parent = None):
        QThread.__init__(self, parent)
        self.q_image = QImage()
        self.default = QImage(1,1,QImage.Format_RGBA8888)
        self.active = True
        self.d_cm = None
        self.timer_state = 0
        self.width = 0
        self.height = 0
        self.interval = 0.1
    def Variables(self, d_cm, timer_state, width, height, doc_width, doc_height, interval):
        self.d_cm = d_cm
        self.timer_state = timer_state
        self.width = width
        self.height = height
        self.doc_width = doc_width
        self.doc_height = doc_height
        self.interval = interval
    def Active(self, active):
        # This exists because the run cant be stopped naturally with self.thread.stop()
        self.active = active
    def run(self):
        while self.active:
            if self.timer_state == 1:
                try:
                    if (self.d_cm == "A" or self.d_cm == "GRAYA"):
                        pass
                    if (self.d_cm == "RGBA" or self.d_cm == None):
                        pixelData = Krita.instance().activeDocument().pixelData(0,0, self.doc_width, self.doc_height)
                        q_image = QImage(pixelData, self.doc_width, self.doc_height, QImage.Format_RGBA8888)
                        q_image = q_image.rgbSwapped()
                    if self.d_cm == "CMYKA":
                        pixelData = Krita.instance().activeDocument().pixelData(0,0, self.doc_width, self.doc_height)
                        q_image = QImage(pixelData, self.doc_width, self.doc_height, QImage.Format_RGBA8888)
                    if self.d_cm == "YCbCrA":
                        pass
                    if self.d_cm == "XYZA":
                        pass
                    if self.d_cm == "LABA":
                        pass

                    # q_image = q_image.scaled(self.width, self.height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    if self.q_image != q_image:
                        self.q_image = q_image
                    self.SIGNAL_IMAGE.emit(self.q_image)
                except:
                    self.q_image = self.default
                    self.SIGNAL_IMAGE.emit(self.default)
            else:
                self.q_image = self.default
                self.SIGNAL_IMAGE.emit(self.default)
            time.sleep(self.interval)

    #//
