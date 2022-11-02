from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import sys
import pygame
import cv2

        
class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # Load the ui file
        uic.loadUi("Squad Task.ui", self)

        # GUI title
        self.title = self.findChild(QLabel, "title")
        # camera1
        self.camera1 = self.findChild(QLabel, "camera1")
        # camera2
        self.camera2 = self.findChild(QLabel, "camera2")
        # vehicle indicators
        self.group1 = self.findChild(QGroupBox, "groupBox")
        self.grapper = self.findChild(QLabel, "grapper")
        self.grapper2 = self.findChild(QLabel, "grapper_2")
        self.forward = self.findChild(QLabel, "forward")
        self.backward = self.findChild(QLabel, "backward")
        self.right = self.findChild(QLabel, "right")
        self.left = self.findChild(QLabel, "left")
        self.cw = self.findChild(QLabel, "cw")
        self.ccw = self.findChild(QLabel, "ccw")
        self.up = self.findChild(QLabel, "up")
        self.down = self.findChild(QLabel, "down")
        # timer
        self.group2 = self.findChild(QGroupBox, "groupBox_3")
        self.startBtn = self.findChild(QPushButton, "start")
        self.stopBtn = self.findChild(QPushButton, "stop")
        self.resetBtn = self.findChild(QPushButton, "reset")
        self.time = self.findChild(QLabel, "time")
        # sensor readings
        self.group3 = self.findChild(QGroupBox, "groupBox_4")
        # scripts
        self.group4 = self.findChild(QGroupBox, "groupBox_5")
        self.codes = self.findChild(QComboBox, "comboBox")
        self.runBtn = self.findChild(QPushButton, "run")
        # current mode
        self.group5 = self.findChild(QGroupBox, "groupBox_6")
        self.currentMode = self.findChild(QLabel, "currentMode")
        self.mode1 = self.findChild(QPushButton, "mode1")
        self.mode2 = self.findChild(QPushButton, "mode2")
        self.mode3 = self.findChild(QPushButton, "mode3")
        self.mode4 = self.findChild(QPushButton, "mode4")
        

        # showing the images in labels
        self.pixmap = QPixmap("icons/grapper-close.png")
        self.pixmap = self.pixmap.scaled(
            75, 120, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.grapper.setPixmap(self.pixmap)
        self.pixmap = QPixmap("icons/grapper-close-horizontalpng.png")
        self.grapper2.setPixmap(self.pixmap)
        self.pixmap = QPixmap("icons/frwrd-arrow.png")
        self.pixmap = self.pixmap.scaled(
            50, 30, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.forward.setPixmap(self.pixmap)
        self.pixmap = QPixmap("icons/bckwrd-arrow.png")
        self.pixmap = self.pixmap.scaled(
            50, 30, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.backward.setPixmap(self.pixmap)
        self.pixmap = QPixmap("icons/right-arrow.png")
        self.pixmap = self.pixmap.scaled(
            30, 50, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.right.setPixmap(self.pixmap)
        self.pixmap = QPixmap("icons/left-arrow.png")
        self.pixmap = self.pixmap.scaled(
            30, 50, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.left.setPixmap(self.pixmap)
        self.pixmap = QPixmap("icons/cw.png")
        self.pixmap = self.pixmap.scaled(
            125, 60, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.cw.setPixmap(self.pixmap)
        self.pixmap = QPixmap("icons/ccw.png")
        self.pixmap = self.pixmap.scaled(
            125, 60, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.ccw.setPixmap(self.pixmap)
        self.pixmap = QPixmap("icons/upward-arrow.png")
        self.pixmap = self.pixmap.scaled(
            60, 60, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.up.setPixmap(self.pixmap)
        self.pixmap = QPixmap("icons/downward-arrow.png")
        self.pixmap = self.pixmap.scaled(
            60, 60, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.down.setPixmap(self.pixmap)

        # change font color to white
        self.title.setStyleSheet("color: white;")
        self.camera1.setStyleSheet("color: white;")
        self.camera2.setStyleSheet("color: white;")
        self.group1.setStyleSheet("color: white;")
        self.group2.setStyleSheet("color: white;")
        self.group3.setStyleSheet("color: white;")
        self.group4.setStyleSheet("color: white;")
        self.group5.setStyleSheet("color: white;")

        # show the app
        self.show()

        # running different scripts
        self.codes.addItem("Code 1")
        self.codes.addItem("Code 2")
        self.codes.addItem("Code 3")
        self.codes.addItem("Code 4")
        self.runBtn.clicked.connect(self.runScript)
        
        # changing modes
        self.mode1.clicked.connect(self.changeMode1)
        self.mode2.clicked.connect(self.changeMode2)
        self.mode3.clicked.connect(self.changeMode3)
        self.mode4.clicked.connect(self.changeMode4)

        # making the timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTimer)
        self.startBtn.clicked.connect(self.startTimer)
        self.stopBtn.clicked.connect(self.stopTimer)
        self.resetBtn.clicked.connect(self.resetTimer)
        self.seconds = 0
        self.minutes = 0
        self.hours = 0

        # show the cameras
        self.camera = Camera()
        self.camera.start()
        self.camera.ImageUpdate.connect(self.ImageUpdateSlot)

        # take inputs from the joystick
        self.joystick = Joystick()
        self.joystick.start()
        self.joystick.button.connect(self.joystickUpdateSlot)

    # running scripts callback function
    def runScript(self):
        self.code = self.codes.currentIndex()+1
        exec(open(f'code{self.code}.py').read())
            
    # changing modes callback functions
    def changeMode1(self):
        self.currentMode.setText(f"Current Mode: Autonomous")

    def changeMode2(self):
        self.currentMode.setText(f"Current Mode: Depth Hold")

    def changeMode3(self):
        self.currentMode.setText(f"Current Mode: Stabilize")

    def changeMode4(self):
        self.currentMode.setText(f"Current Mode: Manual")

    # camera callback function
    def ImageUpdateSlot(self, Image):
        self.camera1.setPixmap(QPixmap.fromImage(Image))
        self.camera2.setPixmap(QPixmap.fromImage(Image.convertToFormat(QImage.Format_Grayscale8)))
        
    # joystick callback function
    def joystickUpdateSlot(self, id, type):

        if id == 14:
            if type == 'press':
                self.pixmap = QPixmap("icons/right-arrowred.png")
                self.pixmap = self.pixmap.scaled(
                    30, 50, Qt.IgnoreAspectRatio, Qt.FastTransformation)
                self.right.setPixmap(self.pixmap) 
            elif type == 'release':
                self.pixmap = QPixmap("icons/right-arrow.png")
                self.pixmap = self.pixmap.scaled(
                    30, 50, Qt.IgnoreAspectRatio, Qt.FastTransformation)
                self.right.setPixmap(self.pixmap) 

        elif id == 13:
            if type == 'press':
                self.pixmap = QPixmap("icons/left-arrowred.png")
                self.pixmap = self.pixmap.scaled(
                    30, 50, Qt.IgnoreAspectRatio, Qt.FastTransformation)
                self.left.setPixmap(self.pixmap) 
            elif type == 'release':
                self.pixmap = QPixmap("icons/left-arrow.png")
                self.pixmap = self.pixmap.scaled(
                    30, 50, Qt.IgnoreAspectRatio, Qt.FastTransformation)
                self.left.setPixmap(self.pixmap) 

        elif id == 11:
            if type == 'press':
                self.pixmap = QPixmap("icons/frwrd-arrowred.png")
                self.pixmap = self.pixmap.scaled(
                50, 30, Qt.IgnoreAspectRatio, Qt.FastTransformation)
                self.forward.setPixmap(self.pixmap) 
            elif type == 'release':
                self.pixmap = QPixmap("icons/frwrd-arrow.png")
                self.pixmap = self.pixmap.scaled(
                50, 30, Qt.IgnoreAspectRatio, Qt.FastTransformation)
                self.forward.setPixmap(self.pixmap) 

        elif id == 12:
            if type == 'press':
                self.pixmap = QPixmap("icons/bckwrd-arrowred.png")
                self.pixmap = self.pixmap.scaled(
                50, 30, Qt.IgnoreAspectRatio, Qt.FastTransformation)
                self.backward.setPixmap(self.pixmap) 
            elif type == 'release':
                self.pixmap = QPixmap("icons/bckwrd-arrow.png")
                self.pixmap = self.pixmap.scaled(
                50, 30, Qt.IgnoreAspectRatio, Qt.FastTransformation)
                self.backward.setPixmap(self.pixmap)  

        elif id == 3:
            if type == 'press':
                self.pixmap = QPixmap("icons/upward-arrowred.png")
                self.pixmap = self.pixmap.scaled(
                60, 60, Qt.IgnoreAspectRatio, Qt.FastTransformation)
                self.up.setPixmap(self.pixmap) 
            elif type == 'release':
                self.pixmap = QPixmap("icons/upward-arrow.png")
                self.pixmap = self.pixmap.scaled(
                60, 60, Qt.IgnoreAspectRatio, Qt.FastTransformation)
                self.up.setPixmap(self.pixmap)

        elif id == 0:
            if type == 'press':
                self.pixmap = QPixmap("icons/downward-arrowred.png")
                self.pixmap = self.pixmap.scaled(
                60, 60, Qt.IgnoreAspectRatio, Qt.FastTransformation)
                self.down.setPixmap(self.pixmap) 
            elif type == 'release':
                self.pixmap = QPixmap("icons/downward-arrow.png")
                self.pixmap = self.pixmap.scaled(
                60, 60, Qt.IgnoreAspectRatio, Qt.FastTransformation)
                self.down.setPixmap(self.pixmap)

        elif id == 10:
            if type == 'press':
                self.pixmap = QPixmap("icons/cwred.png")
                self.pixmap = self.pixmap.scaled(
                125, 60, Qt.IgnoreAspectRatio, Qt.FastTransformation)
                self.cw.setPixmap(self.pixmap) 
            elif type == 'release':
                self.pixmap = QPixmap("icons/cw.png")
                self.pixmap = self.pixmap.scaled(
                125, 60, Qt.IgnoreAspectRatio, Qt.FastTransformation)
                self.cw.setPixmap(self.pixmap)

        elif id == 9:
            if type == 'press':
                self.pixmap = QPixmap("icons/ccwred.png")
                self.pixmap = self.pixmap.scaled(
                125, 60, Qt.IgnoreAspectRatio, Qt.FastTransformation)
                self.ccw.setPixmap(self.pixmap) 
            elif type == 'release':
                self.pixmap = QPixmap("icons/ccw.png")
                self.pixmap = self.pixmap.scaled(
                125, 60, Qt.IgnoreAspectRatio, Qt.FastTransformation)
                self.ccw.setPixmap(self.pixmap)

        elif id == 1:
            if type == 'press':
                self.pixmap = QPixmap("icons/grapper-open.png")
                self.pixmap = self.pixmap.scaled(
                75, 120, Qt.IgnoreAspectRatio, Qt.FastTransformation)
                self.grapper.setPixmap(self.pixmap) 
            elif type == 'release':
                self.pixmap = QPixmap("icons/grapper-close.png")
                self.pixmap = self.pixmap.scaled(
                75, 120, Qt.IgnoreAspectRatio, Qt.FastTransformation)
                self.grapper.setPixmap(self.pixmap)

        elif id == 2:
            if type == 'press':
                self.pixmap = QPixmap("icons/grapper-open-horizontal.png")
                self.grapper2.setPixmap(self.pixmap) 
            elif type == 'release':
                self.pixmap = QPixmap("icons/grapper-close-horizontalpng.png")
                self.grapper2.setPixmap(self.pixmap)

    # timer callback functions
    def showTimer(self):
        self.seconds += 1
        if self.seconds >= 3600:
            self.hours = int(self.seconds / 3600)
            self.seconds = self.seconds % 3600
            if self.seconds >= 60:
                self.minutes = int(self.seconds / 3600)
                self.seconds = self.seconds % 3600
        else:
            if self.seconds >= 60:
                self.minutes = int(self.seconds / 60)
                self.seconds = self.seconds % 60
        
        if self.seconds < 10:
            self.second = '0' + str(self.seconds)
        else:
            self.second = str(self.seconds)
        if self.minutes < 10:
            self.minute = '0' + str(self.minutes)
        else:
            self.minute = str(self.minutes)
        if self.hours < 10:
            self.hour = '0' + str(self.hours)
        else:
            self.hour = str(self.hours)

        self.time.setText(self.hour+':'+self.minute+':'+self.second)

    def startTimer(self):
        self.timer.start(1000)
        self.startWatch = True
        self.startBtn.setEnabled(False)
        self.stopBtn.setEnabled(True)

    def stopTimer(self):
        self.timer.stop()
        self.startBtn.setText("Resume")
        self.startBtn.setEnabled(True)
        self.stopBtn.setEnabled(False)

    def resetTimer(self):
        self.timer.stop()
        self.seconds = 0
        self.minutes = 0
        self.hours = 0
        self.startBtn.setText("Start")
        self.time.setText("00:00:00")
        self.startBtn.setEnabled(True)
        self.stopBtn.setEnabled(False)
    
    # overriding the close event
    def closeEvent(self, event):
        self.camera.stop()
        self.joystick.stop()
        
# thread for the camera
class Camera(QThread):
    ImageUpdate = pyqtSignal(QImage)
    def run(self):
        self.ThreadActive = True
        Capture = cv2.VideoCapture(0)
        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret:
                    Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    FlippedImage = cv2.flip(Image, 1)
                    ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_RGB888)
                    Pic = ConvertToQtFormat.scaled(491, 491, Qt.KeepAspectRatio)
                    self.ImageUpdate.emit(Pic)

    def stop(self):
        self.ThreadActive = False
        self.quit()

# thread for the joystick
class Joystick(QThread):
    button = pyqtSignal(int,str)
    def run(self):
        self.ThreadActive = True
        pygame.init()
        joysticks = []
        for i in range(pygame.joystick.get_count()):
            joysticks.append(pygame.joystick.Joystick(i))
        for joystick in joysticks:
            joystick.init()
        while self.ThreadActive:
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:
                    self.button.emit(event.button, "press")
                if event.type == pygame.JOYBUTTONUP:
                    self.button.emit(event.button, "release")
            
    def stop(self):
        self.ThreadActive = False
        self.quit()

                    
# Initialize the app
app = QApplication(sys.argv)
app.setStyleSheet("""
    UI {
        background-image: url("icons/b.jpg"); 
        background-repeat: no-repeat; 
        background-position: center;
    }
""")
UIWindow = UI()
app.exec_()