from krita import *
from PyQt5 import QtWidgets, QtCore, QtGui, QtSvg
import math
import time


class Channel_Slider(QWidget):
    SIGNAL_VALUE = QtCore.pyqtSignal(float)
    SIGNAL_RELEASE = QtCore.pyqtSignal(int)
    SIGNAL_HALF = QtCore.pyqtSignal(int)
    SIGNAL_MINUS = QtCore.pyqtSignal(int)
    SIGNAL_PLUS = QtCore.pyqtSignal(int)

    # Init
    def __init__(self, parent):
        super(Channel_Slider, self).__init__(parent)
        # Start
        self.Variables()
        # Size Hint Expand
        self.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.MinimumExpanding)
    def sizeHint(self):
        return QtCore.QSize(5000,20)
    def Variables(self):
        # Variables
        self.width = 1
        self.channel_padding = 2
        self.cursor_width = 6
        self.value_x = 0
        self.gray_natural = QColor('#383838')
        self.gray_contrast = QColor('#d4d4d4')
        self.channel = "..."
        self.lock = "..."

    # Relay
    def Channel(self, channel):
        self.channel = channel
    def Update(self, value, channel_width, gray_natural, gray_contrast, lock):
        # Update the variables
        self.channel_width = channel_width
        self.value_x = value * self.channel_width
        # Limit Range
        if self.value_x <= 0:
            self.value_x = 0
        if self.value_x >= self.channel_width:
            self.value_x = self.channel_width
        # Grays
        self.gray_natural = QColor(gray_natural)
        self.gray_contrast = QColor(gray_contrast)
        # Lock Value
        self.lock = lock

    # Interaction
    def mousePressEvent(self, event):
        if event.modifiers() == QtCore.Qt.ShiftModifier:
            self.Emit_Value_Half(event)
        elif event.modifiers() == QtCore.Qt.ControlModifier:
            self.Emit_Value_Pin(event)
        elif event.modifiers() == QtCore.Qt.AltModifier:
            self.Emit_Value_Unit(event)
        else:
            self.Emit_Value(event)
    def mouseMoveEvent(self, event):
        if event.modifiers() == QtCore.Qt.ShiftModifier:
            self.Emit_Value_Half(event)
        elif event.modifiers() == QtCore.Qt.ControlModifier:
            self.Emit_Value_Pin(event)
        elif event.modifiers() == QtCore.Qt.AltModifier:
            pass
        else:
            self.Emit_Value(event)
    def mouseDoubleClickEvent(self, event):
        if event.modifiers() == QtCore.Qt.ShiftModifier:
            self.Emit_Value_Half(event)
        elif event.modifiers() == QtCore.Qt.ControlModifier:
            self.Emit_Value_Pin(event)
        elif event.modifiers() == QtCore.Qt.AltModifier:
            pass
        else:
            self.Emit_Value(event)
    def mouseReleaseEvent(self, event):
        if event.modifiers() == QtCore.Qt.ShiftModifier:
            self.Emit_Value_Half(event)
        elif event.modifiers() == QtCore.Qt.ControlModifier:
            self.Emit_Value_Pin(event)
        elif event.modifiers() == QtCore.Qt.AltModifier:
            pass
        else:
            self.Emit_Value(event)
        self.SIGNAL_RELEASE.emit(0)

    # Emission
    def Emit_Value(self, event):
        # Limit Value inside Range
        self.value_x = event.pos().x()
        if self.value_x <= 0:
            self.value_x = 0
        if self.value_x >= self.channel_width:
            self.value_x = self.channel_width
        # Convert Value to Range
        percentage = self.value_x / self.channel_width
        self.SIGNAL_VALUE.emit(percentage)
    def Emit_Value_Half(self, event): # SHIFT
        self.SIGNAL_HALF.emit(1)
    def Emit_Value_Pin(self, event): # CTRL
        position = event.pos().x()
        if self.channel == "ROTATION":
            # Pin to 360 (delta 10º)
            pp = self.channel_width / 72
            if (position >= 0 and position < (pp*1)):
                self.value_x = 0
            if (position >= (pp*1) and position < (pp*3)):
                self.value_x = pp*2
            if (position >= (pp*3) and position < (pp*5)):
                self.value_x = pp*4
            if (position >= (pp*5) and position < (pp*7)):
                self.value_x = pp*6
            if (position >= (pp*7) and position < (pp*9)):
                self.value_x = pp*8
            if (position >= (pp*9) and position < (pp*11)):
                self.value_x = pp*10
            if (position >= (pp*11) and position < (pp*13)):
                self.value_x = pp*12
            if (position >= (pp*13) and position < (pp*15)):
                self.value_x = pp*14
            if (position >= (pp*15) and position < (pp*17)):
                self.value_x = pp*16
            if (position >= (pp*17) and position < (pp*19)):
                self.value_x = pp*18
            if (position >= (pp*19) and position < (pp*21)):
                self.value_x = pp*20
            if (position >= (pp*21) and position < (pp*23)):
                self.value_x = pp*22
            if (position >= (pp*23) and position < (pp*25)):
                self.value_x = pp*24
            if (position >= (pp*25) and position < (pp*27)):
                self.value_x = pp*26
            if (position >= (pp*27) and position < (pp*29)):
                self.value_x = pp*28
            if (position >= (pp*29) and position < (pp*31)):
                self.value_x = pp*30
            if (position >= (pp*31) and position < (pp*33)):
                self.value_x = pp*32
            if (position >= (pp*33) and position < (pp*35)):
                self.value_x = pp*34
            if (position >= (pp*35) and position < (pp*37)):
                self.value_x = pp*36
            if (position >= (pp*37) and position < (pp*39)):
                self.value_x = pp*38
            if (position >= (pp*39) and position < (pp*41)):
                self.value_x = pp*40
            if (position >= (pp*41) and position < (pp*43)):
                self.value_x = pp*42
            if (position >= (pp*43) and position < (pp*45)):
                self.value_x = pp*44
            if (position >= (pp*45) and position < (pp*47)):
                self.value_x = pp*46
            if (position >= (pp*47) and position < (pp*49)):
                self.value_x = pp*48
            if (position >= (pp*49) and position < (pp*51)):
                self.value_x = pp*50
            if (position >= (pp*51) and position < (pp*53)):
                self.value_x = pp*52
            if (position >= (pp*53) and position < (pp*55)):
                self.value_x = pp*54
            if (position >= (pp*55) and position < (pp*57)):
                self.value_x = pp*56
            if (position >= (pp*57) and position < (pp*59)):
                self.value_x = pp*58
            if (position >= (pp*59) and position < (pp*61)):
                self.value_x = pp*60
            if (position >= (pp*61) and position < (pp*63)):
                self.value_x = pp*62
            if (position >= (pp*63) and position < (pp*65)):
                self.value_x = pp*64
            if (position >= (pp*65) and position < (pp*67)):
                self.value_x = pp*66
            if (position >= (pp*67) and position < (pp*69)):
                self.value_x = pp*68
            if (position >= (pp*69) and position < (pp*71)):
                self.value_x = pp*70
            if (position >= (pp*71) and position < (pp*72)):
                self.value_x = pp*0
        else:
            # Pin to 11
            pp = self.channel_width / 20
            if (position >= 0 and position < (pp*1)):
                self.value_x = 0
            if (position >= (pp*1) and position < (pp*3)):
                self.value_x = pp*2
            if (position >= (pp*3) and position < (pp*5)):
                self.value_x = pp*4
            if (position >= (pp*5) and position < (pp*7)):
                self.value_x = pp*6
            if (position >= (pp*7) and position < (pp*9)):
                self.value_x = pp*8
            if (position >= (pp*9) and position < (pp*11)):
                self.value_x = pp*10
            if (position >= (pp*11) and position < (pp*13)):
                self.value_x = pp*12
            if (position >= (pp*13) and position < (pp*15)):
                self.value_x = pp*14
            if (position >= (pp*15) and position < (pp*17)):
                self.value_x = pp*16
            if (position >= (pp*17) and position < (pp*19)):
                self.value_x = pp*18
            if (position >= (pp*19) and position < (pp*20)):
                self.value_x = pp*20
        # Convert Value to Range
        percentage = self.value_x / self.channel_width
        self.SIGNAL_VALUE.emit(percentage)
    def Emit_Value_Unit(self, event): # ALT
        if event.x() <= (self.channel_width*0.5):
            self.SIGNAL_MINUS.emit(1)
        else:
            self.SIGNAL_PLUS.emit(1)

    # Paint Style
    def paintEvent(self, event):
        self.drawCursor(event)
    def drawCursor(self, event):
        # Start Qpainter
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # Available Space Calculations
        width = event.rect().width()
        height = event.rect().height()

        # Letters Contrast
        painter.setPen(self.gray_contrast)
        painter.setFont(QFont('Helvetica', 6, QtGui.QFont.Bold))
        painter.drawText(event.rect(), Qt.AlignHCenter|Qt.AlignVCenter, str(self.channel)+" ["+str(self.lock)+"]")

        # Style
        top = 1
        bot = height-1
        # Cursor Amount Square
        polygon = QPolygon([
            QPoint(self.value_x+1, top),
            QPoint(1, top),
            QPoint(1, bot),
            QPoint(self.value_x+1, bot)
            ])
        # Draw Cursor
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(self.gray_contrast))
        painter.drawPolygon(polygon)

        # Masking
        square = QPainterPath()
        square.moveTo(self.value_x+1, top)
        square.lineTo(1, top)
        square.lineTo(1, bot)
        square.lineTo(self.value_x+1, bot)
        painter.setClipPath(square)
        # Letters Natural
        painter.setPen(self.gray_natural)
        painter.setFont(QFont('Helvetica', 6, QtGui.QFont.Bold))
        painter.drawText(event.rect(), Qt.AlignHCenter|Qt.AlignVCenter, str(self.channel)+" ["+str(self.lock)+"]")


class Clicks(QWidget):
    SIGNAL_APPLY = QtCore.pyqtSignal(int)
    SIGNAL_SAVE = QtCore.pyqtSignal(int)
    SIGNAL_CLEAN = QtCore.pyqtSignal(int)

    # Init
    def __init__(self, parent):
        super(Clicks, self).__init__(parent)
    def sizeHint(self):
        return QtCore.QSize(200,200)

    # Relay
    def Setup_SOF(self, gray_contrast):
        self.gray_contrast = QColor(gray_contrast)

    # Interaction
    def mousePressEvent(self, event):
        if event.modifiers() == QtCore.Qt.ShiftModifier:
            self.SIGNAL_APPLY.emit(0)
        if event.modifiers() == QtCore.Qt.ControlModifier:
            self.SIGNAL_SAVE.emit(1)
        if event.modifiers() == QtCore.Qt.AltModifier:
            self.SIGNAL_CLEAN.emit(2)
    def mouseDoubleClickEvent(self, event):
        self.SIGNAL_APPLY.emit(0)

    # Paint Style
    def paintEvent(self, event):
        self.drawColors(event)
    def drawColors(self, event):
        # QPainter Start
        painter = QPainter()
        painter.begin(self)
        # Background
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(self.gray_contrast))
        painter.drawRect(0,0, 200, 200)
        # Finish
        painter.end()


class Panel(QWidget):
    SIGNAL_ROTATE = QtCore.pyqtSignal(float)

    # Inut
    def __init__(self, parent):
        super(Panel, self).__init__(parent)
        self.thread = Image()
        self.Variables()
        self.Thread_Start()
    def sizeHint(self):
        return QtCore.QSize(5000,5000)
    def Variables(self):
        self.status = False
        self.q_image = False

        self.eraser = False

        self.sof_1 = 0.04 # 40%
        self.sof_2 = 1
        self.sof_3 = 1

        self.can_rotation = 0
        self.can_zoom = 1
        self.exposure = 0
        self.gamma = 1

        self.doc_width = 1
        self.doc_height = 1
        self.ui_d_ref = False
        self.delta_new = [0,0,0,0]
        self.gui_hor_norm = []
        self.gui_ver_norm = []

        self.panel_width = 0
        self.panel_height = 0
        self.gray_natural = QColor('#383838')
        self.gray_contrast = QColor('#d4d4d4')

        self.angle = 0
        self.radius = 0
        self.size = 0

        self.doc_p1_x = 0
        self.doc_p1_y = 0
        self.doc_p2_x = 0
        self.doc_p2_y = 0
        self.doc_p3_x = 0
        self.doc_p3_y = 0
        self.doc_p4_x = 0
        self.doc_p4_y = 0

        self.doc_thumb = QImage()
        self.sx = 0
        self.sy = 0

    # Relay
    def Update_Panel(self, status, q_image, eraser, sof_1, sof_2, sof_3, can_rotation, can_zoom, exposure, gamma, mirror, wrap, doc_width, doc_height, ui_d_ref, delta_new, gui_hor_norm, gui_ver_norm, panel_width, panel_height, gray_natural, gray_contrast):
        self.status = status
        self.q_image = q_image
        self.eraser = eraser
        self.sof_1 = sof_1 # Brush Size
        self.sof_2 = sof_2 # Brush Opacity
        self.sof_3 = sof_3 # Brush Flow
        self.can_rotation = can_rotation
        self.can_zoom = can_zoom
        self.exposure = exposure
        self.gamma = gamma
        self.mirror = mirror
        self.wrap = wrap
        self.doc_width = doc_width
        self.doc_height = doc_height
        self.ui_d_ref = ui_d_ref
        self.delta_new = delta_new
        self.gui_hor_norm = gui_hor_norm
        self.gui_ver_norm = gui_ver_norm
        self.panel_width = panel_width
        self.panel_height = panel_height
        self.gray_natural = QColor(gray_natural)
        self.gray_contrast = QColor(gray_contrast)

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

        # Guides
        delta_top_x = self.doc_p2_x - self.doc_p1_x
        delta_top_y = self.doc_p2_y - self.doc_p1_y
        delta_bot_x = self.doc_p3_x - self.doc_p4_x
        delta_bot_y = self.doc_p3_y - self.doc_p4_y

        delta_lef_x = self.doc_p4_x - self.doc_p1_x
        delta_lef_y = self.doc_p4_y - self.doc_p1_y
        delta_rig_x = self.doc_p3_x - self.doc_p2_x
        delta_rig_y = self.doc_p3_y - self.doc_p2_y

        self.guides_ver_top = []
        self.guides_ver_bot = []
        for i in range(0, len(self.gui_ver_norm)):
            self.guides_ver_top.append([
                self.doc_p1_x + (delta_top_x*(self.gui_ver_norm[i] / self.doc_width)),
                self.doc_p1_y + (delta_top_y*(self.gui_ver_norm[i] / self.doc_width))
                ])
            self.guides_ver_bot.append([
                self.doc_p4_x + (delta_bot_x*(self.gui_ver_norm[i] / self.doc_width)),
                self.doc_p4_y + (delta_bot_y*(self.gui_ver_norm[i] / self.doc_width))
                ])

        self.guides_hor_lef = []
        self.guides_hor_rig = []
        for i in range(0, len(self.gui_hor_norm)):
            self.guides_hor_lef.append([
                self.doc_p1_x + (delta_lef_x*(self.gui_hor_norm[i] / self.doc_height)),
                self.doc_p1_y + (delta_lef_y*(self.gui_hor_norm[i] / self.doc_height))
                ])
            self.guides_hor_rig.append([
                self.doc_p2_x + (delta_rig_x*(self.gui_hor_norm[i] / self.doc_height)),
                self.doc_p2_y + (delta_rig_y*(self.gui_hor_norm[i] / self.doc_height))
                ])

        # QImage Scale Calculations
        dw = self.Math_2D_Points_Distance(self.doc_p1_x,self.doc_p1_y, self.doc_p2_x,self.doc_p2_y)
        dh = self.Math_2D_Points_Distance(self.doc_p1_x,self.doc_p1_y, self.doc_p3_x,self.doc_p3_y)
        six = (dw / self.doc_width)
        siy = (dh / self.doc_height)
        sox = (self.doc_width / dw)
        soy = (self.doc_height / dh)
        self.sx = doc_width*six
        self.sy = doc_height*siy
        # QImage Thumbnail to Scale
        self.thread.size(self.q_image, self.sx, self.sy)

    # Thread
    def Thread_Start(self):
        self.thread.SIGNAL_IMAGE['QImage'].connect(self.Thread_Image)
        self.thread.start()
    def Thread_Image(self, image):
        self.doc_thumb = image

    # Mouse Interaction
    def mousePressEvent(self, event):
        self.origin_x = event.x()
        self.origin_y = event.y()
        if event.modifiers() == QtCore.Qt.ShiftModifier:
            pass
        if event.modifiers() == QtCore.Qt.ControlModifier:
            pass
        if event.modifiers() == QtCore.Qt.AltModifier:
            pass
        else:
            self.MouseN(event)
    def mouseMoveEvent(self, event):
        self.MouseN(event)
    def mouseDoubleClickEvent(self, event):
        self.MouseN(event)
    def mouseReleaseEvent(self, event):
        self.MouseN(event)

    def MouseN(self, event):
        # Event Position
        self.event_x = event.x()
        self.event_y = event.y()

        # Rotation
        dist = self.Math_2D_Points_Distance(self.panel_width*0.5, self.panel_height*0.5, self.origin_x, self.origin_y)
        if self.panel_width > self.panel_height:
            self.side = self.panel_height
        else:
            self.side = self.panel_width
        if (dist > ((self.side * 0.5)* 0.9) and dist < ((self.side*0.5)*1.1) ):
            # Angle in 360
            self.angle = self.Math_2D_Points_Lines_Angle(
                self.panel_width*0.5,0,
                self.panel_width*0.5,self.panel_height*0.5,
                self.event_x, self.event_y,
                )
            # Ctrl Modifier to Snap values
            if event.modifiers() == QtCore.Qt.ControlModifier:
                pp = 5
                if (self.angle >= 0 and self.angle < (pp*1)):
                    self.angle = 0
                if (self.angle >= (pp*1) and self.angle < (pp*3)):
                    self.angle = pp*2
                if (self.angle >= (pp*3) and self.angle < (pp*5)):
                    self.angle = pp*4
                if (self.angle >= (pp*5) and self.angle < (pp*7)):
                    self.angle = pp*6
                if (self.angle >= (pp*7) and self.angle < (pp*9)):
                    self.angle = pp*8
                if (self.angle >= (pp*9) and self.angle < (pp*11)):
                    self.angle = pp*10
                if (self.angle >= (pp*11) and self.angle < (pp*13)):
                    self.angle = pp*12
                if (self.angle >= (pp*13) and self.angle < (pp*15)):
                    self.angle = pp*14
                if (self.angle >= (pp*15) and self.angle < (pp*17)):
                    self.angle = pp*16
                if (self.angle >= (pp*17) and self.angle < (pp*19)):
                    self.angle = pp*18
                if (self.angle >= (pp*19) and self.angle < (pp*21)):
                    self.angle = pp*20
                if (self.angle >= (pp*21) and self.angle < (pp*23)):
                    self.angle = pp*22
                if (self.angle >= (pp*23) and self.angle < (pp*25)):
                    self.angle = pp*24
                if (self.angle >= (pp*25) and self.angle < (pp*27)):
                    self.angle = pp*26
                if (self.angle >= (pp*27) and self.angle < (pp*29)):
                    self.angle = pp*28
                if (self.angle >= (pp*29) and self.angle < (pp*31)):
                    self.angle = pp*30
                if (self.angle >= (pp*31) and self.angle < (pp*33)):
                    self.angle = pp*32
                if (self.angle >= (pp*33) and self.angle < (pp*35)):
                    self.angle = pp*34
                if (self.angle >= (pp*35) and self.angle < (pp*37)):
                    self.angle = pp*36
                if (self.angle >= (pp*37) and self.angle < (pp*39)):
                    self.angle = pp*38
                if (self.angle >= (pp*39) and self.angle < (pp*41)):
                    self.angle = pp*40
                if (self.angle >= (pp*41) and self.angle < (pp*43)):
                    self.angle = pp*42
                if (self.angle >= (pp*43) and self.angle < (pp*45)):
                    self.angle = pp*44
                if (self.angle >= (pp*45) and self.angle < (pp*47)):
                    self.angle = pp*46
                if (self.angle >= (pp*47) and self.angle < (pp*49)):
                    self.angle = pp*48
                if (self.angle >= (pp*49) and self.angle < (pp*51)):
                    self.angle = pp*50
                if (self.angle >= (pp*51) and self.angle < (pp*53)):
                    self.angle = pp*52
                if (self.angle >= (pp*53) and self.angle < (pp*55)):
                    self.angle = pp*54
                if (self.angle >= (pp*55) and self.angle < (pp*57)):
                    self.angle = pp*56
                if (self.angle >= (pp*57) and self.angle < (pp*59)):
                    self.angle = pp*58
                if (self.angle >= (pp*59) and self.angle < (pp*61)):
                    self.angle = pp*60
                if (self.angle >= (pp*61) and self.angle < (pp*63)):
                    self.angle = pp*62
                if (self.angle >= (pp*63) and self.angle < (pp*65)):
                    self.angle = pp*64
                if (self.angle >= (pp*65) and self.angle < (pp*67)):
                    self.angle = pp*66
                if (self.angle >= (pp*67) and self.angle < (pp*69)):
                    self.angle = pp*68
                if (self.angle >= (pp*69) and self.angle < (pp*71)):
                    self.angle = pp*70
                if (self.angle >= (pp*71) and self.angle < (pp*72)):
                    self.angle = pp*0
            # Emit
            angle = self.angle/360
            self.SIGNAL_ROTATE.emit(angle)

    # Paint
    def paintEvent(self, event):
        self.drawColors(event)
    def drawColors(self, event):
        # Start Qpainter
        painter = QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.NoBrush)

        # Background
        if self.eraser == True:
            painter.setBrush(QBrush(self.gray_contrast))
            painter.drawRect(0,0, self.panel_width, self.panel_height)
            painter.setBrush(Qt.NoBrush)

        # QImage
        if (self.status == True and self.q_image == True):
            # Calculations
            if self.ui_d_ref == False:
                t = [self.doc_p1_x, self.doc_p1_y]
            else:
                t = self.Math_2D_Points_Lines_Intersection(
                    self.guides_ver_top[0][0], self.guides_ver_top[0][1],
                    self.guides_ver_bot[0][0], self.guides_ver_bot[0][1],
                    self.guides_hor_lef[0][0], self.guides_hor_lef[0][1],
                    self.guides_hor_rig[0][0], self.guides_hor_rig[0][1],
                    )
            # Save State for Painter
            painter.save()
            # Transformation
            painter.translate(t[0], t[1])
            painter.rotate(self.can_rotation)
            painter.scale(1,1)

            # Draw QImage
            if self.mirror == True:
                painter.drawImage(
                    0,0,
                    self.doc_thumb.mirrored(True, False))
            else:
                painter.drawImage(
                    0,0,
                    self.doc_thumb)
            # Restore Painter Coordinates
            painter.restore()

        # Pen
        if self.eraser == True:
            painter.setPen(QPen(QColor(self.gray_natural), 2, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
        else:
            painter.setPen(QPen(QColor(self.gray_contrast), 2, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))

        # Rotation Size
        margin = 5
        if self.panel_width <= self.panel_height:
            self.size = self.panel_width-(2*margin)
        if self.panel_width > self.panel_height:
            self.size = self.panel_height-(2*margin)
        painter.drawEllipse((self.panel_width*0.5)-(self.size*0.5), (self.panel_height*0.5)-(self.size*0.5), self.size, self.size)
        # Rotation Pie
        painter.drawPie(QRect((self.panel_width*0.5)-(self.size*0.5),(self.panel_height*0.5)-(self.size*0.5),self.size,self.size), 16*90, -16*self.can_rotation)
        # Dimension Lines
        square = QPainterPath()
        square.moveTo(self.doc_p1_x, self.doc_p1_y)
        square.lineTo(self.doc_p2_x, self.doc_p2_y)
        square.lineTo(self.doc_p3_x, self.doc_p3_y)
        square.lineTo(self.doc_p4_x, self.doc_p4_y)
        square.lineTo(self.doc_p1_x, self.doc_p1_y)
        if self.status == False:
            square.moveTo(self.doc_p1_x, self.doc_p1_y)
            square.lineTo(self.doc_p3_x, self.doc_p3_y)
            square.moveTo(self.doc_p2_x, self.doc_p2_y)
            square.lineTo(self.doc_p4_x, self.doc_p4_y)
        painter.drawPath(square)

        # SOF 1
        if self.status == True:
            rel_width = self.Math_2D_Points_Distance(self.doc_p1_x,self.doc_p1_y, self.doc_p2_x,self.doc_p2_y)
            rel_sof_1 = (self.sof_1 * rel_width) / self.doc_width
            painter.drawEllipse((self.panel_width*0.5)-(rel_sof_1*0.5), (self.panel_height*0.5)-(rel_sof_1*0.5), rel_sof_1, rel_sof_1)

        # Points
        painter.setPen(Qt.NoPen)
        if self.eraser == True:
            painter.setBrush(QBrush(self.gray_natural))
        else:
            painter.setBrush(QBrush(self.gray_contrast))
        painter.drawEllipse(self.doc_p1_x-margin,self.doc_p1_y-margin, 10,10)
        painter.drawEllipse(self.doc_p2_x-margin,self.doc_p2_y-margin, 10,10)
        painter.drawEllipse(self.doc_p3_x-margin,self.doc_p3_y-margin, 10,10)
        painter.drawEllipse(self.doc_p4_x-margin,self.doc_p4_y-margin, 10,10)

        # Guides
        painter.setPen(QPen(QColor(128,50,50), 2, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
        painter.setBrush(Qt.NoBrush)
        guides = QPainterPath()
        for i in range(0, len(self.gui_ver_norm)):
            guides.moveTo(self.guides_ver_top[i][0], self.guides_ver_top[i][1])
            guides.lineTo(self.guides_ver_bot[i][0], self.guides_ver_bot[i][1])
        for i in range(0, len(self.gui_hor_norm)):
            guides.moveTo(self.guides_hor_lef[i][0], self.guides_hor_lef[i][1])
            guides.lineTo(self.guides_hor_rig[i][0], self.guides_hor_rig[i][1])
        painter.drawPath(guides)

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
class Image(QThread):
    SIGNAL_IMAGE = QtCore.pyqtSignal(QImage)

    def __init__(self, parent = None):
        QThread.__init__(self, parent)

        self.doc_thumb = QImage()
        self.doc_default = QImage()

        self.q_image = False
        self.width = 0
        self.height = 0

    def size(self, q_image, width, height):
        self.q_image = q_image
        self.width = width
        self.height = height

    def run(self):
        while True:
            if self.q_image == True:
                # QImage query
                doc_thumb = Krita.instance().activeDocument().thumbnail(self.width , self.height)
                if self.doc_thumb != doc_thumb:
                    self.doc_thumb = doc_thumb
                    self.SIGNAL_IMAGE.emit(self.doc_thumb)
            else:
                self.doc_thumb = self.doc_default
                self.SIGNAL_IMAGE.emit(self.doc_default)
            time.sleep(1)


class Style(QWidget):
    def SVG_Cursor_LMB(self):
        string_cursor_lmb = str(
        "<svg width=\"100\" height=\"100\" viewBox=\"0 0 75.000003 75.000003\" version=\"1.1\" id=\"svg54\"> \n" +
        "  <defs id=\"defs46\" /> \n" +
        "  <path \n" +
        "     style=\"display:inline;fill:\#000000;fill-opacity:1;stroke:none;stroke-width:1.47647631\" \n" +
        "     d=\"M 50,0 A 49.999998,49.999998 0 0 0 0,50 49.999998,49.999998 0 0 0 50,100 49.999998,49.999998 0 0 0 100,50 49.999998,49.999998 0 0 0 50,0 Z m 0,6 A 43.999998,43.999998 0 0 1 94,50 43.999998,43.999998 0 0 1 50,94 43.999998,43.999998 0 0 1 6,50 43.999998,43.999998 0 0 1 50,6 Z\" \n" +
        "     id=\"circle824\" \n" +
        "     transform=\"scale(0.75000003)\" \n" +
        "     inkscape:label=\"Black\" \n" +
        "     inkscape:connector-curvature=\"0\" /> \n" +
        "  <path \n" +
        "     style=\"display:inline;fill:\#ffffff;fill-opacity:1;stroke:none;stroke-width:1.29929912\" \n" +
        "     d=\"M 50,6 A 43.999998,43.999998 0 0 0 6,50 43.999998,43.999998 0 0 0 50,94 43.999998,43.999998 0 0 0 94,50 43.999998,43.999998 0 0 0 50,6 Z m 0,6.5 A 37.500001,37.500001 0 0 1 87.5,50 37.500001,37.500001 0 0 1 50,87.5 37.500001,37.500001 0 0 1 12.5,50 37.500001,37.500001 0 0 1 50,12.5 Z\" \n" +
        "     transform=\"scale(0.75000003)\" \n" +
        "     id=\"circle821\" \n" +
        "     inkscape:label=\"White\" \n" +
        "     inkscape:connector-curvature=\"0\" /> \n" +
        "</svg> "
        )
        array_cursor_lmb = bytearray(string_cursor_lmb, encoding='utf-8')
        return array_cursor_lmb
    def SVG_Cursor_RMB(self, color):
        color = str(color)
        string_cursor_rmb = str(
        "<svg width=\"100\" height=\"100\" viewBox=\"0 0 75.000003 75.000003\" version=\"1.1\" id=\"svg54\"> \n" +
        "  <defs id=\"defs46\" /> \n" +
        "  <path \n" +
        "     style=\"display:inline;fill:\#000000;fill-opacity:1;stroke:none;stroke-width:1.47647631\" \n" +
        "     d=\"M 50,0 A 49.999998,49.999998 0 0 0 0,50 49.999998,49.999998 0 0 0 50,100 49.999998,49.999998 0 0 0 100,50 49.999998,49.999998 0 0 0 50,0 Z m 0,6 A 43.999998,43.999998 0 0 1 94,50 43.999998,43.999998 0 0 1 50,94 43.999998,43.999998 0 0 1 6,50 43.999998,43.999998 0 0 1 50,6 Z\" \n" +
        "     id=\"circle824\" \n" +
        "     transform=\"scale(0.75000003)\" \n" +
        "     inkscape:label=\"Black\" \n" +
        "     inkscape:connector-curvature=\"0\" /> \n" +
        "  <circle \n" +
        "     style=\"display:inline;fill:"+color+";fill-opacity:1;stroke:none;stroke-width:0.97447437\" \n" +
        "     id=\"circle816\" \n" +
        "     cx=\"37.5\" \n" +
        "     cy=\"37.500004\" \n" +
        "     inkscape:label=\"Color\" \n" +
        "     r=\"33\" /> \n" +
        "</svg> "
        )
        array_cursor_rmb = bytearray(string_cursor_rmb, encoding='utf-8')
        return array_cursor_rmb
    def SVG_Cursor_NODE(self, color):
        string_cursor_node = str(
        "<svg width=\"64\" height=\"64\" viewBox=\"0 0 48.000002 48.000002\" version=\"1.1\" id=\"svg54\"> \n" +
        "  <defs id=\"defs46\" /> \n" +
        "  <circle \n" +
        "     style=\"fill:"+color+";stroke-width:0.0;stroke:none\" \n" +
        "     id=\"path831\" \n" +
        "     cx=\"24.000002\" \n" +
        "     cy=\"24.000002\" \n" +
        "     r=\"24.000002\" /> \n" +
        "</svg>"
        )
        array_cursor_node = bytearray(string_cursor_node, encoding='utf-8')
        return array_cursor_node
    def SVG_Cursor_POINT(self, color1, color2):
        string_cursor_point = str(
        "<svg width=\"64\" height=\"64\" viewBox=\"0 0 48.000002 48.000002\" version=\"1.1\" id=\"svg54\"> \n" +
        "  <defs id=\"defs46\" /> \n" +
        "  <path \n" +
        "     id=\"path834\" \n" +
        "     style=\"fill:"+color1+";fill-opacity:1;stroke:none;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1\" \n" +
        "     d=\"M 32,0 0,32 32,64 64,32 Z M 32,14 50,32 32,50 13.999999,32 Z\" \n" +
        "     transform=\"scale(0.75000003)\" \n" +
        "     inkscape:label=\"OUT\" \n" +
        "     sodipodi:nodetypes=\"cccccccccc\" /> \n" +
        "  <path \n" +
        "     style=\"fill:"+color2+";fill-opacity:1;stroke:none;stroke-width:0.75px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1\" \n" +
        "     d=\"M 24.000001,10.5 10.5,24.000001 24.000001,37.500002 37.500002,24.000001\" \n" +
        "     id=\"path845\" \n" +
        "     sodipodi:nodetypes=\"cccc\" \n" +
        "     inkscape:label=\"IN\" /> \n" +
        "</svg> "
        )
        array_cursor_point = bytearray(string_cursor_point, encoding='utf-8')
        return array_cursor_point
    def Transparent(self):
        transparent = "background-color: rgba(0, 0, 0, 0); border: 1px solid rgba(0, 0, 0, 0) ;"
        return transparent
