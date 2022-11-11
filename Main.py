
from PyQt5.QtCore import QDir, Qt, QUrl, QEvent
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QLineEdit)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction
from PyQt5.QtGui import QIcon,QWheelEvent
import sys
import os

def get_hms_from_mili(mili):
    seconds=int((mili/1000)%60)
    minutes=int((mili/(1000*60))%60)
    hours=int((mili/(1000*60*60))%24)
    return f"{hours}:{minutes}:{seconds}"


class VideoWindow(QMainWindow):

    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)
        
        
        self.init_playback_options()
        
        self.InitFCRTextBoxes()

        self.setWindowTitle("PyQt Video Player Widget Example - pythonprogramminglanguage.com") 
        self.setAcceptDrops(True)
        
        videoWidget = self.init_media_player()


        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Maximum)

        self.InitActions()

        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)

        # Create layouts to place inside widget
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)

        layout = QVBoxLayout()
        layout.addWidget(self.FCRTextBox)
        layout.addWidget(self.DefectTextBox)
        layout.addWidget(self.pipeRunTextBox)

        layout.addWidget(self.errorLabel)
        layout.addWidget(self.current_rate_label)
        layout.addWidget(self.current_position_label)
        layout.addLayout(controlLayout)
        layout.addWidget(videoWidget)

        # Set widget to contain window contents
        wid.setLayout(layout)

    def init_playback_options(self):
        self.current_rate = 1.0
        self.current_rate_label = QLabel(self)
        self.current_rate_label.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Maximum)
        self.add_to_current_rate(1.0)
        self.current_position_label = QLabel(self)
        self.current_position_label.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Maximum)
        self.currentVideo = ""
        self.In = 0
        self.Out = 0

    def init_media_player(self):
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videoWidget = QVideoWidget()

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)
        return videoWidget

    def InitActions(self):
        # Create new action
        openAction = QAction(QIcon('open.png'), '&Open', self)        
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open movie')
        openAction.triggered.connect(self.openFile)
        
        # Create InPoint action
        InPointAction = QAction(QIcon('open.png'), '&InPoint', self)        
        InPointAction.setShortcut('I')
        InPointAction.setStatusTip('SetInpoint')
        InPointAction.triggered.connect(self.setInPoint)  
        
        # Create Output action
        OutPointAction = QAction(QIcon('open.png'), '&OutPoint', self)        
        OutPointAction.setShortcut('O')
        OutPointAction.setStatusTip('SetOutpoint')
        OutPointAction.triggered.connect(self.setOutPoint)
        
        # Save Output action
        SaveOutputAction = QAction(QIcon('open.png'), '&SaveOutput', self)        
        SaveOutputAction.setShortcut('Ctrl+S')
        SaveOutputAction.setStatusTip('SetSaveOutput')
        SaveOutputAction.triggered.connect(self.SaveOutput)
        
        # Create exit action
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.exitCall)
        
        # Create Faster action
        FasterAction = QAction(QIcon('Faster.png'), '&Faster', self)        
        FasterAction.setShortcut('Up')
        FasterAction.setStatusTip('Faster')
        FasterAction.triggered.connect(self.fasterAction)
        
        # Create Slower action
        SlowerAction = QAction(QIcon('Slower.png'), '&Slower', self)        
        SlowerAction.setShortcut('Down')
        SlowerAction.setStatusTip('Slower')
        SlowerAction.triggered.connect(self.slowerAction)
        

        # Create menu bar and add action
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        #fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)
        fileMenu.addAction(InPointAction)
        fileMenu.addAction(OutPointAction)
        fileMenu.addAction(SaveOutputAction)
        fileMenu.addAction(FasterAction)
        fileMenu.addAction(SlowerAction)

    def InitFCRTextBoxes(self):
        self.FCRTextBox = QLineEdit(self)
        self.FCRTextBox.setText("FCR")
        self.DefectTextBox = QLineEdit(self)
        self.DefectTextBox.setText("Defect")
        self.pipeRunTextBox = QLineEdit(self)
        self.pipeRunTextBox.setText("PipeRun")
     
    def add_to_current_rate(self,num):
        self.current_rate*=num
        self.current_rate_label.setText(f"Rate: {self.current_rate}")
        
    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                QDir.homePath())
        
        self.doOpenFile(fileName)

    def doOpenFile(self,fileName):
        if fileName != '':
            self.currentVideo = fileName
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)
            self.play()

    def exitCall(self):
        sys.exit(app.exec_())
    
    def fasterAction(self):
        self.add_to_current_rate(2)
        
    def slowerAction(self):
        self.add_to_current_rate(0.5)

    def play(self):
        self.playButton.setFocus()
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()
        
    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)
        self.current_position_label.setText(f"Current Position: {get_hms_from_mili(self.mediaPlayer.position())}")

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.setErrorLabel("Error: " + self.mediaPlayer.errorString())
        
        
    def setErrorLabel(self, inString):
        self.errorLabel.setText(inString)
        
    def setInPoint(self):
        self.In = self.mediaPlayer.position()
        self.setErrorLabel(f"In: {get_hms_from_mili(self.In)} | Out: {get_hms_from_mili(self.Out)}")


    def setOutPoint(self):
        self.Out = self.mediaPlayer.position()
        self.setErrorLabel(f"In: {get_hms_from_mili(self.In)} | Out: {get_hms_from_mili(self.Out)}")
        
    def SaveOutput(self):
        self.setErrorLabel('Saving...')
        file_format = self.currentVideo.split('.')[-1]
        out_file_name = f"Output/{self.FCRTextBox.text()}_{self.DefectTextBox.text()}_{self.pipeRunTextBox.text()}.{file_format}"
       
        command = f"ffmpeg -i \"{self.currentVideo}\" -ss {get_hms_from_mili(self.In)} -to {get_hms_from_mili(self.Out)} -c:v copy -c:a copy \"{out_file_name}\""
        
        print(command)
        os.system(command) 
        self.setErrorLabel('Done!')
        
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        lines = []
        for url in event.mimeData().urls():
            lines.append(url.toLocalFile())
            
        fileToOpen = lines[0].replace('"','')
        self.doOpenFile(fileToOpen)
        
    def wheelEvent(self,event):
        if not self.currentVideo == "":
            self.mediaPlayer.setPosition(self.mediaPlayer.position() + 1000*self.current_rate*event.angleDelta().y()/120)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoWindow()
    player.resize(640, 480)
    player.show()
    sys.exit(app.exec_())