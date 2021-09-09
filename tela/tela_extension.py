from krita import *
from PyQt5 import Qt, QtWidgets, QtCore, QtGui, QtSvg, uic
from PyQt5.Qt import Qt


EXTENSION_ID = 'pykrita_tela_extension'

class TelaExtension(Extension):
    """
    Extension Shortcuts and HUD.
    """
    SIGNAL_KEY = QtCore.pyqtSignal(str)
    SIGNAL_HUD = QtCore.pyqtSignal(int)

    #\\ Initialize #############################################################
    def __init__(self, parent):
        super().__init__(parent)

    #//
    #\\ Actions ################################################################
    def createActions(self, window):
        # Shortcut Keys
        action_size_minus = window.createAction(EXTENSION_ID+"_size_minus", "T. Size Minus", "tools/scripts")
        action_size_minus.triggered.connect(self.Size_Minus)
        action_size_plus = window.createAction(EXTENSION_ID+"_size_plus", "T. Size Plus", "tools/scripts")
        action_size_plus.triggered.connect(self.Size_Plus)

        action_opacity_minus = window.createAction(EXTENSION_ID+"_opacity_minus", "T. Opacity Minus", "tools/scripts")
        action_opacity_minus.triggered.connect(self.Opacity_Minus)
        action_opacity_plus = window.createAction(EXTENSION_ID+"_opacity_plus", "T. Opacity Plus", "tools/scripts")
        action_opacity_plus.triggered.connect(self.Opacity_Plus)

        action_flow_minus = window.createAction(EXTENSION_ID+"_flow_minus", "T. Flow Minus", "tools/scripts")
        action_flow_minus.triggered.connect(self.Flow_Minus)
        action_flow_plus = window.createAction(EXTENSION_ID+"_flow_plus", "T. Flow Plus", "tools/scripts")
        action_flow_plus.triggered.connect(self.Flow_Plus)

        action_rotation_minus = window.createAction(EXTENSION_ID+"_rotation_minus", "T. Rotation Minus", "tools/scripts")
        action_rotation_minus.triggered.connect(self.Rotation_Minus)
        action_rotation_plus = window.createAction(EXTENSION_ID+"_rotation_plus", "T. Rotation Plus", "tools/scripts")
        action_rotation_plus.triggered.connect(self.Rotation_Plus)

        action_zoom_minus = window.createAction(EXTENSION_ID+"_zoom_minus", "T. Zoom Minus", "tools/scripts")
        action_zoom_minus.triggered.connect(self.Zoom_Minus)
        action_zoom_plus = window.createAction(EXTENSION_ID+"_zoom_plus", "T. Zoom Plus", "tools/scripts")
        action_zoom_plus.triggered.connect(self.Zoom_Plus)

        action_exposure_minus = window.createAction(EXTENSION_ID+"_exposure_minus", "T. Exposure Minus", "tools/scripts")
        action_exposure_minus.triggered.connect(self.Exposure_Minus)
        action_exposure_plus = window.createAction(EXTENSION_ID+"_exposure_plus", "T. Exposure Plus", "tools/scripts")
        action_exposure_plus.triggered.connect(self.Exposure_Plus)

        action_gamma_minus = window.createAction(EXTENSION_ID+"_gamma_minus", "T. Gamma Minus", "tools/scripts")
        action_gamma_minus.triggered.connect(self.Gamma_Minus)
        action_gamma_plus = window.createAction(EXTENSION_ID+"_gamma_plus", "T. Gamma Plus", "tools/scripts")
        action_gamma_plus.triggered.connect(self.Gamma_Plus)

        # Panel HUD
        action_panel_hud = window.createAction(EXTENSION_ID+"_panel_hud", "T. Panel HUD", "tools/scripts")
        action_panel_hud.triggered.connect(self.Panel_HUD)
        action_panel_hud.setAutoRepeat(False)

    #//
    #\\ KEY ####################################################################
    def Size_Minus(self):
        self.SIGNAL_KEY.emit("Size Minus")
    def Size_Plus(self):
        self.SIGNAL_KEY.emit("Size Plus")

    def Opacity_Minus(self):
        self.SIGNAL_KEY.emit("Opacity Minus")
    def Opacity_Plus(self):
        self.SIGNAL_KEY.emit("Opacity Plus")

    def Flow_Minus(self):
        self.SIGNAL_KEY.emit("Flow Minus")
    def Flow_Plus(self):
        self.SIGNAL_KEY.emit("Flow Plus")

    def Rotation_Minus(self):
        self.SIGNAL_KEY.emit("Rotation Minus")
    def Rotation_Plus(self):
        self.SIGNAL_KEY.emit("Rotation Plus")

    def Zoom_Minus(self):
        self.SIGNAL_KEY.emit("Zoom Minus")
    def Zoom_Plus(self):
        self.SIGNAL_KEY.emit("Zoom Plus")

    def Exposure_Minus(self):
        self.SIGNAL_KEY.emit("Exposure Plus")
    def Exposure_Plus(self):
        self.SIGNAL_KEY.emit("Exposure Plus")

    def Gamma_Minus(self):
        self.SIGNAL_KEY.emit("Gamma Minus")
    def Gamma_Plus(self):
        self.SIGNAL_KEY.emit("Gamma Plus")

    #//
    #\\ Panel HUD ##############################################################
    def Panel_HUD(self):
        self.SIGNAL_HUD.emit(0)

    #//
    #\\ Events #################################################################
    def canvasChanged(self, canvas):
        pass
    #//
