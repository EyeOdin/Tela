from krita import *
from PyQt5 import QtWidgets, QtCore, QtGui, QtSvg
import math


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
        # Confirm 10 Percentil Values
        position = event.pos().x()
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
        painter.setPen(QtCore.Qt.NoPen)
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
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QBrush(self.gray_contrast))
        painter.drawRect(0,0, 200, 200)
        # Finish
        painter.end()


class Panel_Canvas(QWidget):
    SIGNAL_CANVAS = QtCore.pyqtSignal(float)

    # Inut
    def __init__(self, parent):
        super(Panel_Canvas, self).__init__(parent)
        self.Variables()
    def sizeHint(self):
        return QtCore.QSize(5000,5000)
    def Variables(self):
        self.eraser = False
        self.can_rotation = 0
        self.can_zoom = 1
        self.doc_width = 0
        self.doc_height = 0
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

    # Relay
    def Update_Panel(self,
        eraser,
        can_rotation, can_zoom,
        doc_width, doc_height,
        ui_d_ref, delta_new,
        gui_hor_norm, gui_ver_norm,
        panel_width, panel_height,
        gray_natural, gray_contrast
        ):
        self.eraser = eraser
        self.can_rotation = can_rotation
        self.can_zoom = can_zoom
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

        # Calculations (size of square)
        self.angle = self.Math_2D_Points_Lines_Angle(
            self.doc_width,0,
            0,0,
            self.doc_width,self.doc_height,
            )
        # Size
        margin = 5
        if self.panel_width <= self.panel_height:
            self.size = self.panel_width-(2*margin)
        if self.panel_width > self.panel_height:
            self.size = self.panel_height-(2*margin)
        # Points
        self.doc_p1_x = (self.panel_width*0.5) - ((self.size*0.5) * math.cos(math.radians(self.angle+self.can_rotation)))
        self.doc_p1_y = (self.panel_height*0.5) - ((self.size*0.5) * math.sin(math.radians(self.angle+self.can_rotation)))
        self.doc_p2_x = (self.panel_width*0.5) - ((self.size*0.5) * math.cos(math.radians(180-self.angle+self.can_rotation)))
        self.doc_p2_y = (self.panel_height*0.5) - ((self.size*0.5) * math.sin(math.radians(180-self.angle+self.can_rotation)))
        self.doc_p3_x = (self.panel_width*0.5) - ((self.size*0.5) * math.cos(math.radians(180+self.angle+self.can_rotation)))
        self.doc_p3_y = (self.panel_height*0.5) - ((self.size*0.5) * math.sin(math.radians(180+self.angle+self.can_rotation)))
        self.doc_p4_x = (self.panel_width*0.5) - ((self.size*0.5) * math.cos(math.radians(-self.angle+self.can_rotation)))
        self.doc_p4_y = (self.panel_height*0.5) - ((self.size*0.5) * math.sin(math.radians(-self.angle+self.can_rotation)))

    # Mouse Interaction
    def mousePressEvent(self, event):
        self.mouseCursor(event)
    def mouseMoveEvent(self, event):
        self.mouseCursor(event)
    def mouseDoubleClickEvent(self, event):
        self.mouseCursor(event)
    def mouseReleaseEvent(self, event):
        self.mouseCursor(event)

    def mouseCursor(self, event):
        pass

    # Paint
    def paintEvent(self, event):
        self.drawColors(event)
    def drawColors(self, event):
        # Start Qpainter
        painter = QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setPen(QtCore.Qt.NoPen)

        # Background
        if self.eraser == True:
            painter.setBrush(QBrush(self.gray_contrast))
            painter.drawRect(0,0, self.panel_width, self.panel_height)

        # Pen
        if self.eraser == True:
            painter.setPen(QPen(QColor(self.gray_natural), 2, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
        else:
            painter.setPen(QPen(QColor(self.gray_contrast), 2, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))

        # Size
        margin = 5
        if self.panel_width <= self.panel_height:
            self.size = self.panel_width-(2*margin)
        if self.panel_width > self.panel_height:
            self.size = self.panel_height-(2*margin)
        painter.drawEllipse((self.panel_width*0.5)-(self.size*0.5), (self.panel_height*0.5)-(self.size*0.5), self.size, self.size)
        # Lines
        square = QPainterPath()
        square.moveTo(self.doc_p1_x, self.doc_p1_y)
        square.lineTo(self.doc_p2_x, self.doc_p2_y)
        square.lineTo(self.doc_p3_x, self.doc_p3_y)
        square.lineTo(self.doc_p4_x, self.doc_p4_y)
        square.lineTo(self.doc_p1_x, self.doc_p1_y)
        painter.drawPath(square)
        # Pie
        painter.drawPie(QRect((self.panel_width*0.5)-(self.size*0.5),(self.panel_height*0.5)-(self.size*0.5),self.size,self.size), 0, -16*self.can_rotation)
        # Points
        painter.setBrush(QBrush(self.gray_contrast))
        painter.drawEllipse(self.doc_p1_x-margin,self.doc_p1_y-margin, 10,10)
        painter.drawEllipse(self.doc_p2_x-margin,self.doc_p2_y-margin, 10,10)
        painter.drawEllipse(self.doc_p3_x-margin,self.doc_p3_y-margin, 10,10)
        painter.drawEllipse(self.doc_p4_x-margin,self.doc_p4_y-margin, 10,10)

    def Math_2D_Points_Lines_Angle(self, x1, y1, x2, y2, x3, y3):
        v1 = (x1-x2, y1-y2)
        v2 = (x3-x2, y3-y2)
        v1_theta = math.atan2(v1[1], v1[0])
        v2_theta = math.atan2(v2[1], v2[0])
        angle = (v2_theta - v1_theta) * (180.0 / math.pi)
        if angle < 0:
            angle += 360.0
        return angle


class Panel_View(QWidget):
    SIGNAL_VIEW = QtCore.pyqtSignal(list)

    # Inut
    def __init__(self, parent):
        super(Panel_View, self).__init__(parent)
        self.Variables()
        self.Cursor()
    def sizeHint(self):
        return QtCore.QSize(5000,5000)
    def Variables(self):
        self.eraser = False
        self.size = 0.04 # 40%
        self.opacity = 1
        self.flow = 1
        self.exposure = 0
        self.gamma = 1
        self.panel_width = 1
        self.panel_height = 1
        self.gray_natural = QColor('#383838')
        self.gray_contrast = QColor('#d4d4d4')
        self.line = 2
        self.cursor = 6
        self.value_x = 0
        self.value_y = 0
    def Cursor(self):
        # Variables
        self.hex = '#000000'
        # Module Style
        self.style = Style()
        # LMB SVG Cursor
        self.cursor_lmb = QtSvg.QSvgWidget(self)
        self.array_lmb = self.style.SVG_Cursor_LMB()
        self.cursor_lmb.load(self.array_lmb)
        # Style SVG Cursors
        self.cursor_size = 20
        self.cursor_half = self.cursor_size / 2
        self.cursor_lmb.setGeometry(QtCore.QRect(-self.cursor_half, -self.cursor_half, self.cursor_size, self.cursor_size))
        self.unseen = self.style.Transparent()
        self.cursor_lmb.setStyleSheet(self.unseen)
        # Cursor Scale
        self.scale_factor = 180

    # Relay
    def Update_Panel(self, eraser, size, opacity, flow, exposure, gamma, panel_width, panel_height, gray_natural, gray_contrast):
        self.eraser = eraser
        self.size = size
        self.opacity = opacity
        self.flow = flow
        self.exposure = exposure
        self.gamma = gamma
        self.panel_width = panel_width
        self.panel_height = panel_height
        self.gray_natural = QColor(gray_natural)
        self.gray_contrast = QColor(gray_contrast)
        # Change cursor
        self.value_x = self.opacity * self.panel_width
        self.value_y = (1-self.flow) * self.panel_height
        self.cursor_lmb.move(self.value_x-(self.cursor_lmb.width() / 2), self.value_y-(self.cursor_lmb.height() / 2))

    # Mouse Interaction
    def mousePressEvent(self, event):
        self.mouseCursor(event)
    def mouseMoveEvent(self, event):
        self.mouseCursor(event)
    def mouseDoubleClickEvent(self, event):
        self.mouseCursor(event)
    def mouseReleaseEvent(self, event):
        self.mouseCursor(event)

    def mouseCursor(self, event):
        # Mouse Position
        self.value_x = event.x()
        self.value_y = event.y()
        # Limit Position
        if self.value_x <= 0:
            self.value_x = 0
        if self.value_x >= self.panel_width:
            self.value_x = self.panel_width
        if self.value_y <= 0:
            self.value_y = 0
        if self.value_y >= self.panel_height:
            self.value_y = self.panel_height
        # Move Cursor
        self.cursor_lmb.move(self.value_x-(self.cursor_lmb.width() / 2), self.value_y-(self.cursor_lmb.height() / 2))
        # Emit Values
        self.SIGNAL_VIEW.emit([
            0,
            self.value_x / self.panel_width,
            (self.panel_height - self.value_y) / self.panel_height,
            ])

    # Paint
    def paintEvent(self, event):
        self.drawColors(event)
    def drawColors(self, event):
        # Start Qpainter
        painter = QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setPen(QtCore.Qt.NoPen)

        # Background
        if self.eraser == True:
            painter.setBrush(QBrush(self.gray_contrast))
            painter.drawRect(0,0, self.panel_width, self.panel_height)

        # Pen
        if self.eraser == True:
            painter.setPen(QPen(QColor(self.gray_natural), 2, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
        else:
            painter.setPen(QPen(QColor(self.gray_contrast), 2, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))

        # Size
        painter.drawEllipse((self.panel_width*0.5)-(self.size*0.5)+0.5, (self.panel_height*0.5)-(self.size*0.5)+0.5, self.size, self.size)

        # Lines
        lines = QPainterPath()
        lines.moveTo(self.panel_width*0.5, 0)
        lines.lineTo(self.panel_width*0.5, self.panel_height)
        lines.moveTo(0, self.panel_height*0.5)
        lines.lineTo(self.panel_width, self.panel_height*0.5)
        painter.drawPath(lines)


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
