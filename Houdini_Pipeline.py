# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Houdini_PipelineaFkohJ.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
import sys
import os
import re
import json
import importlib.util
import subprocess
import glob
import winreg
import socket
import threading

from functools import partial
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, QThread, Signal, Slot, QSettings, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontMetrics, QFontDatabase, QGradient, QShortcut,
    QIcon, QImage, QKeySequence, QLinearGradient, QUndoStack, QUndoCommand,
    QPainter, QPalette, QPixmap, QRadialGradient, QDesktopServices,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox, QHeaderView,
    QLabel, QLineEdit, QMainWindow, QDockWidget, QMenu, QCheckBox,
    QMenuBar, QProgressBar, QListWidget, QPushButton, QSizePolicy,
    QSpinBox, QStatusBar, QTabWidget, QTextEdit, QToolButton, QDialog,
    QHBoxLayout, QVBoxLayout, QTreeWidget, QFileDialog, QTreeWidgetItem,
    QMessageBox, QWidget)

    #Configuring Absolute Path
current_directory = os.path.dirname(os.path.abspath(__file__))
module_directory = os.path.join(current_directory, 'Scripts')
icon_directory = os.path.join(current_directory, 'icons')


if module_directory not in sys.path:
    sys.path.insert(0, module_directory)

modules = {}
for filename in os.listdir(module_directory):
    if filename.endswith('.py') and filename != '__init__.py':
        module_name = os.path.splitext(filename)[0]

        # hou 모듈을 사용하는 스크립트를 건너뛰기 위한 조건을 추가할 수 있습니다.
        # 예: if "hou_dependent" in filename: continue

        module_spec = importlib.util.spec_from_file_location(module_name, os.path.join(module_directory, filename))
        module = importlib.util.module_from_spec(module_spec)
        try:
            module_spec.loader.exec_module(module)
            modules[module_name] = module  # 모듈 이름을 키로 사용하여 딕셔너리에 추가
        except ImportError:
            print(f"Module {module_name} could not be loaded.")

class ServerThread(QObject):
    update_signal = Signal(str)

    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.empty_data_count = 0  # 빈 데이터 수신 횟수 카운터 추가

    def run(self):
        while True:
            try:
                print("Waiting for data...")
                data = self.connection.recv(1024)
                print(f"Data received: {data}")

                if not data:
                    self.empty_data_count += 1
                    print("Received empty data. Count:", self.empty_data_count)
                    if self.empty_data_count > 5:  # 조건 수정 가능
                        print("Too many empty data received. Closing connection.")
                        self.connection.close()  # 연결 종료
                        break
                    continue

                self.empty_data_count = 0  # 유효한 데이터 수신 시 카운터 초기화
                message = json.loads(data.decode('utf-8'))
                print(f"Decoded message: {message}")
                self.update_signal.emit(message['status'])
            except json.JSONDecodeError as e:
                print(f"JSON Decode Error: {e}")
                break
            except Exception as e:
                print(f"General Error: {e}")
                break

class Ui_MainWindow(object):
    settings = QSettings("YourOrganization", "YourApplication")
    tab_memos = {}
    saved_memo_content = ""
    lastEditedLineEdit = None  # 마지막으로 변경된 QLineEdit 추적

    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        icon_path = os.path.join(icon_directory,'icon.png')
        MainWindow.setWindowIcon(QIcon(icon_path))
        MainWindow.resize(1520, 852)


        # 사이드바 추가
        self.sideBarDockWidget = QDockWidget("Navigator",MainWindow)
        self.sideBarDockWidget.setObjectName(u"sideBarDockWidget")
        self.sideBarListWidget = QListWidget(self.sideBarDockWidget)
        self.sideBarListWidget.setObjectName(u"sideBarListWidget")

        self.sideBarDockWidget.setWidget(self.sideBarListWidget)
        MainWindow.addDockWidget(Qt.LeftDockWidgetArea, self.sideBarDockWidget)

        # 사이드바에 탭 이름들 추가
        self.updateSidebarWithTabs()

        self.actiontesrt = QAction(MainWindow)
        self.actiontesrt.setObjectName(u"actiontesrt")
        self.actionNew = QAction(MainWindow)
        self.actionNew.setObjectName(u"actionNew")
        self.actionClose = QAction(MainWindow)
        self.actionClose.setObjectName(u"actionClose")
        self.actionLoad = QAction(MainWindow)
        self.actionLoad.setObjectName(u"actionLoad")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionRedo = QAction(MainWindow)
        self.actionRedo.setObjectName(u"actionRedo")
        self.actionUndo = QAction(MainWindow)
        self.actionUndo.setObjectName(u"actionUndo")
        self.HelpT = QAction(MainWindow)
        self.HelpT.setObjectName(u"HelpT")
        self.AboutT = QAction(MainWindow)
        self.AboutT.setObjectName(u"AboutT")
        self.actionSidebarControler = QAction(MainWindow)
        self.actionSidebarControler.setObjectName(u"actionSidebarControler")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.ToolWidget = QTabWidget(self.centralwidget)
        self.ToolWidget.setObjectName(u"ToolWidget")
        self.ToolWidget.setGeometry(QRect(10, 10, 1331, 791))

        # 탭 변경 시그널 연결 (현재 선택된 탭이 변경될 때)
        self.ToolWidget.currentChanged.connect(self.updateSidebarWithTabs)

        # 사이드바 리스트의 itemClicked 시그널에 슬롯 연결
        self.sideBarListWidget.itemClicked.connect(self.onSidebarItemClicked)

        # 사이드바 너비 조절
        self.adjustSidebarWidth()

        # 사이드바 초기 업데이트
        self.updateSidebarWithTabs()

        self.MasterTap = QWidget()
        self.MasterTap.setObjectName(u"MasterTap")
        self.MaProjectSaveB = QPushButton(self.MasterTap)
        self.MaProjectSaveB.setObjectName(u"MaProjectSaveB")
        self.MaProjectSaveB.setGeometry(QRect(470, 10, 61, 23))
        self.MaListLogB = QPushButton(self.MasterTap)
        self.MaListLogB.setObjectName(u"MaListLogB")
        self.MaListLogB.setGeometry(QRect(830, 440, 41, 23))
        self.MaListReloadB = QPushButton(self.MasterTap)
        self.MaListReloadB.setObjectName(u"MaListReloadB")
        self.MaListReloadB.setGeometry(QRect(830, 410, 41, 23))
        icon_reload = QIcon(os.path.join(icon_directory, 'refresh.png'))
        self.MaListReloadB.setIcon(icon_reload)
        self.MaListT = QLabel(self.MasterTap)
        self.MaListT.setObjectName(u"MaListT")
        self.MaListT.setGeometry(QRect(20, 410, 101, 20))
        self.MaCountV = QSpinBox(self.MasterTap)
        self.MaCountV.setObjectName(u"MaCountV")
        self.MaCountV.setGeometry(QRect(750, 10, 111, 22))
        self.MaCountV.setMinimum(1)
        self.MaCountV.setValue(1)
        self.MaProjectLoadB = QPushButton(self.MasterTap)
        self.MaProjectLoadB.setObjectName(u"MaProjectLoadB")
        self.MaProjectLoadB.setGeometry(QRect(540, 10, 61, 23))
        self.MaStartFrameT = QLabel(self.MasterTap)
        self.MaStartFrameT.setObjectName(u"MaStartFrameT")
        self.MaStartFrameT.setGeometry(QRect(20, 250, 111, 20))
        self.MaProjectT = QLabel(self.MasterTap)
        self.MaProjectT.setObjectName(u"MaProjectT")
        self.MaProjectT.setGeometry(QRect(20, 10, 101, 20))
        self.MaListTree = QTreeWidget(self.MasterTap)
        self.MaListTree.headerItem().setText(0, "")
        font = QFont()
        font.setBold(False)
        __qtreewidgetitem = QTreeWidgetItem(self.MaListTree)
        __qtreewidgetitem.setTextAlignment(2, Qt.AlignLeading|Qt.AlignVCenter);
        __qtreewidgetitem.setCheckState(0, Qt.Checked);
        __qtreewidgetitem.setFont(0, font);
        __qtreewidgetitem1 = QTreeWidgetItem(self.MaListTree)
        __qtreewidgetitem1.setCheckState(0, Qt.Checked);
        __qtreewidgetitem2 = QTreeWidgetItem(self.MaListTree)
        __qtreewidgetitem2.setCheckState(0, Qt.Checked);
        __qtreewidgetitem3 = QTreeWidgetItem(self.MaListTree)
        __qtreewidgetitem3.setCheckState(0, Qt.Checked);
        self.MaListTree.setObjectName(u"MaListTree")
        self.MaListTree.setGeometry(QRect(150, 410, 671, 291))
        self.MaProjectV = QLineEdit(self.MasterTap)
        self.MaProjectV.setObjectName(u"MaProjectV")
        self.MaProjectV.setGeometry(QRect(150, 10, 301, 20))
        self.MaAllCreateB = QPushButton(self.MasterTap)
        self.MaAllCreateB.setObjectName(u"MaAllCreateB")
        self.MaAllCreateB.setGeometry(QRect(150, 370, 121, 23))
        self.MaShotPathV = QLineEdit(self.MasterTap)
        self.MaShotPathV.setObjectName(u"MaShotPathV")
        self.MaShotPathV.setGeometry(QRect(150, 290, 671, 21))
        self.MastBox = QGroupBox(self.MasterTap)
        self.MastBox.setObjectName(u"MastBox")
        self.MastBox.setGeometry(QRect(10, 50, 881, 191))
        self.mastTap = QTabWidget(self.MastBox)
        self.mastTap.setObjectName(u"mastTap")
        self.mastTap.setGeometry(QRect(10, 20, 861, 161))
        self.MaShotPathT = QLabel(self.MasterTap)
        self.MaShotPathT.setObjectName(u"MaShotPathT")
        self.MaShotPathT.setGeometry(QRect(20, 290, 101, 20))
        self.MaShotPathB = QToolButton(self.MasterTap)
        self.MaShotPathB.setObjectName(u"MaShotPathB")
        self.MaShotPathB.setGeometry(QRect(830, 290, 41, 21))
        self.MaCountT = QLabel(self.MasterTap)
        self.MaCountT.setObjectName(u"MaCountT")
        self.MaCountT.setGeometry(QRect(620, 10, 121, 20))
        self.MaStartFrameV = QLineEdit(self.MasterTap)
        self.MaStartFrameV.setObjectName(u"MaStartFrameV")
        self.MaStartFrameV.setGeometry(QRect(150, 250, 101, 20))
        self.MaSelCreateB = QPushButton(self.MasterTap)
        self.MaSelCreateB.setObjectName(u"MaSelCreateB")
        self.MaSelCreateB.setGeometry(QRect(280, 370, 161, 23))
        self.MaCachePathB = QToolButton(self.MasterTap)
        self.MaCachePathB.setObjectName(u"MaCachePathB")
        self.MaCachePathB.setGeometry(QRect(830, 330, 41, 21))
        self.MaCachePathV = QLineEdit(self.MasterTap)
        self.MaCachePathV.setObjectName(u"MaCachePathV")
        self.MaCachePathV.setGeometry(QRect(150, 330, 671, 21))
        self.MaCachePathT = QLabel(self.MasterTap)
        self.MaCachePathT.setObjectName(u"MaCachePathT")
        self.MaCachePathT.setGeometry(QRect(20, 330, 111, 20))
        self.ToolWidget.addTab(self.MasterTap, "")
        self.SimulationTap = QWidget()
        self.SimulationTap.setObjectName(u"SimulationTap")
        self.SimListT = QLabel(self.SimulationTap)
        self.SimListT.setObjectName(u"SimListT")
        self.SimListT.setGeometry(QRect(20, 130, 101, 20))

        self.SequenceBox = QGroupBox(self.SimulationTap)
        self.SequenceBox.setObjectName(u"SequenceBox")
        self.SequenceBox.setGeometry(QRect(20, 10, 971, 111))

        self.SimListB = QPushButton(self.SimulationTap)
        self.SimListB.setObjectName(u"SimListB")
        self.SimListB.setGeometry(QRect(130, 620, 121, 23))
        self.SimSelB = QPushButton(self.SimulationTap)
        self.SimSelB.setObjectName(u"SimSelB")
        self.SimSelB.setGeometry(QRect(130, 590, 121, 23))
        self.SimDeselB = QPushButton(self.SimulationTap)
        self.SimDeselB.setObjectName(u"SimDeselB")
        self.SimDeselB.setGeometry(QRect(260, 590, 121, 23))
        self.SimStartFrameV = QLineEdit(self.SequenceBox)
        self.SimStartFrameV.setObjectName(u"SimStartFrameV")
        self.SimStartFrameV.setEnabled(True)
        self.SimStartFrameV.setGeometry(QRect(110, 70, 101, 20))
        self.SimStartFrameT = QLabel(self.SequenceBox)
        self.SimStartFrameT.setObjectName(u"SimStartFrameT")
        self.SimStartFrameT.setGeometry(QRect(20, 70, 111, 20))
        self.SimResT = QLabel(self.SequenceBox)
        self.SimResT.setObjectName(u"SimResT")
        self.SimResT.setGeometry(QRect(310, 30, 111, 20))
        self.SimResV_X = QLineEdit(self.SequenceBox)
        self.SimResV_X.setObjectName(u"SimResV_X")
        self.SimResV_X.setEnabled(True)
        self.SimResV_X.setGeometry(QRect(390, 70, 101, 20))
        self.SimResV_Y = QLineEdit(self.SequenceBox)
        self.SimResV_Y.setObjectName(u"SimResV_Y")
        self.SimResV_Y.setEnabled(True)
        self.SimResV_Y.setGeometry(QRect(520, 70, 101, 20))
        self.SimResT_1 = QLabel(self.SequenceBox)
        self.SimResT_1.setObjectName(u"SimResT_1")
        self.SimResT_1.setGeometry(QRect(500, 70, 16, 20))
        self.SimResB = QComboBox(self.SequenceBox)
        self.SimResB.addItem("")
        self.SimResB.addItem("")
        self.SimResB.addItem("")
        self.SimResB.setObjectName(u"SimResB")
        self.SimResB.setGeometry(QRect(390, 30, 101, 22))
        self.SimFrameRateV = QLineEdit(self.SequenceBox)
        self.SimFrameRateV.setObjectName(u"SimFrameRateV")
        self.SimFrameRateV.setEnabled(True)
        self.SimFrameRateV.setGeometry(QRect(110, 30, 101, 20))
        self.SimFrameRateT = QLabel(self.SequenceBox)
        self.SimFrameRateT.setObjectName(u"SimFrameRateT")
        self.SimFrameRateT.setGeometry(QRect(20, 30, 111, 20))
        self.SimResB.currentIndexChanged.connect(self.updateResolutionFields)
        self.SimListReloadB = QPushButton(self.SimulationTap)
        self.SimListReloadB.setObjectName(u"SimListReloadB")
        self.SimListReloadB.setGeometry(QRect(1000, 130, 41, 23))
        self.SimListReloadB.setIcon(icon_reload)
        self.SimBar = QProgressBar(self.SimulationTap)
        self.SimBar.setObjectName(u"SimBar")
        self.SimBar.setEnabled(True)
        self.SimBar.setGeometry(QRect(130, 650, 120, 10))
        self.SimBar.setTextVisible(False)
        # 배경색을 블랙과 화이트의 농도로 설정
        black_intensity = 242  # 블랙의 농도 (0부터 255까지)
        white_intensity = 255  # 화이트의 농도 (0부터 255까지)
        style = f"""
            QProgressBar {{
                border: none;
                background-color: rgba({black_intensity}, {black_intensity}, {black_intensity}, 255);
            }}

            QProgressBar::chunk {{
                background-color: rgb(36, 145, 255);   
            }}
        """
        self.SimBar.setStyleSheet(style)

        self.existing_data = {}
        self.SimListTree = QTreeWidget(self.SimulationTap)
        self.SimListTree.setObjectName(u"SimListTree")
        self.SimListTree.setGeometry(QRect(130, 130, 861, 451))
        self.ToolWidget.addTab(self.SimulationTap, "")

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1367, 22))
        self.menutes = QMenu(self.menubar)
        self.menutes.setObjectName(u"menutes")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menutes.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menutes.addAction(self.actionNew)
        self.menutes.addSeparator()
        self.menutes.addAction(self.actionSave)
        self.menutes.addAction(self.actionLoad)
        self.menutes.addSeparator()
        self.menutes.addAction(self.actionClose)
        self.menuEdit.addAction(self.actionRedo)
        self.menuEdit.addAction(self.actionUndo)
        self.menuView.addAction(self.actionSidebarControler)
        self.menuHelp.addAction(self.HelpT)

        # 사이드바 가시성 변경 시그널 연결
        self.sideBarDockWidget.visibilityChanged.connect(self.on_sidebar_visibility_changed)

        # View / Navigator에 대한 액션 연결
        self.actionSidebarControler.triggered.connect(self.on_off_sidebar)
        self.actionSidebarControler.setCheckable(True)  # 체크 가능 상태로 설정
        self.actionSidebarControler.setChecked(True)

        # HelpT 액션 추가
        # 주의: 여기서 'self' 대신 'MainWindow' 객체를 사용합니다.
        self.menuHelp.addAction(self.HelpT)
        self.menuHelp.addAction(self.AboutT)

        # 메뉴에 추가
        self.menubar.addMenu(self.menuHelp)

        # HelpT 액션에 슬롯 연결
        self.HelpT.triggered.connect(self.open_help)

        # AboutT 액션에 슬롯 연결
        self.AboutT.triggered.connect(self.open_about)

        self.RenderFarmTap = QWidget()
        self.RenderFarmTap.setObjectName(u"RenderFarm")
        self.Client_T = QGroupBox(self.RenderFarmTap)
        self.Client_T.setObjectName(u"Client_T")
        self.Client_T.setGeometry(QRect(20, 470, 601, 281))
        self.ClientListTree = QTreeWidget(self.Client_T)
        QTreeWidgetItem(self.ClientListTree)
        QTreeWidgetItem(self.ClientListTree)
        QTreeWidgetItem(self.ClientListTree)
        self.ClientListTree.setObjectName(u"ClientListTree")
        self.ClientListTree.setGeometry(QRect(10, 60, 581, 211))
        self.ClientAdd_B = QPushButton(self.Client_T)
        self.ClientAdd_B.setObjectName(u"ClientAdd_B")
        self.ClientAdd_B.setGeometry(QRect(10, 30, 75, 24))
        self.ClientDel_B = QPushButton(self.Client_T)
        self.ClientDel_B.setObjectName(u"ClientDel_B")
        self.ClientDel_B.setGeometry(QRect(90, 30, 75, 24))
        self.Job_T = QGroupBox(self.RenderFarmTap)
        self.Job_T.setObjectName(u"Job_T")
        self.Job_T.setGeometry(QRect(20, 30, 1211, 421))
        self.JobListTree = QTreeWidget(self.Job_T)
        QTreeWidgetItem(self.JobListTree)
        QTreeWidgetItem(self.JobListTree)
        QTreeWidgetItem(self.JobListTree)
        QTreeWidgetItem(self.JobListTree)
        self.JobListTree.setObjectName(u"JobListTree")
        self.JobListTree.setGeometry(QRect(10, 50, 1191, 361))
        self.update_B = QPushButton(self.Job_T)
        self.update_B.setObjectName(u"update_B")
        self.update_B.setGeometry(QRect(1120, 20, 75, 24))
        self.JobNote = QTabWidget(self.RenderFarmTap)
        self.JobNote.setObjectName(u"JobNote")
        self.JobNote.setGeometry(QRect(630, 480, 591, 261))
        self.JobInfo = QWidget()
        self.JobInfo.setObjectName(u"JobInfo")
        self.JobInfoPlay_B = QPushButton(self.JobInfo)
        self.JobInfoPlay_B.setObjectName(u"JobInfoPlay_B")
        self.JobInfoPlay_B.setGeometry(QRect(10, 10, 51, 23))
        self.JobInfoProgress = QProgressBar(self.JobInfo)
        self.JobInfoProgress.setObjectName(u"JobInfoProgress")
        self.JobInfoProgress.setGeometry(QRect(70, 10, 71, 23))
        self.JobInfoProgress.setValue(24)
        self.JobInfoProgress.setTextVisible(False)
        self.JobInfoProgress.setInvertedAppearance(False)
        self.JobInfoPreview = QLabel(self.JobInfo)
        self.JobInfoPreview.setObjectName(u"JobInfoPreview")
        self.JobInfoPreview.setGeometry(QRect(10, 50, 281, 171))
        self.JobNote.addTab(self.JobInfo, "")
        self.JobSetting = QWidget()
        self.JobSetting.setObjectName(u"JobSetting")
        self.JobNote.addTab(self.JobSetting, "")
        self.JobLog = QWidget()
        self.JobLog.setObjectName(u"JobLog")
        self.JobNote.addTab(self.JobLog, "")
        self.ToolWidget.addTab(self.RenderFarmTap, "")

        self.retranslateUi(MainWindow)

        self.MaCountV.valueChanged.connect(self.updateTabs)
        self.addInitialTab()

        self.MaProjectSaveB.clicked.connect(self.saveFile)
        self.MaProjectLoadB.clicked.connect(self.loadFile)

        self.MaStartFrameV.textChanged.connect(self.on_ma_start_frame_v_changed)


        self.MaShotPathB.clicked.connect(self.ShotselectDirectory)
        self.MaCachePathB.clicked.connect(self.CacheselectDirectory)

        self.MaShotPathB.clicked.connect(self.load_folder_list)
        self.MaShotPathB.clicked.connect(self.update_sim_list_tree)
        self.MaAllCreateB.clicked.connect(self.create_and_run_cmd_for_all_shots)
        self.MaSelCreateB.clicked.connect(self.create_and_run_cmd_for_shots)

        self.MaListReloadB.clicked.connect(self.load_folder_list)
        self.MaListReloadB.clicked.connect(self.update_sim_list_tree)
        self.MaListLogB.clicked.connect(self.open_memo_dialog)
        self.saved_memo_content = ""

        self.SimListB.clicked.connect(self.update_render_cmd)
        self.SimSelB.clicked.connect(self.select_all_sim_items)
        self.SimDeselB.clicked.connect(self.deselect_all_sim_items)
        self.SimFrameRateV.setText(QCoreApplication.translate("Dialog", u"24", None))
        self.SimFrameRateT.setText(QCoreApplication.translate("Dialog", u"Frame Rate", None))
        self.SimStartFrameV.setText(QCoreApplication.translate("Dialog", u"", None))
        self.SimStartFrameT.setText(QCoreApplication.translate("Dialog", u"Start Frame", None))
        self.SimResT.setText(QCoreApplication.translate("Dialog", u"Resolution", None))
        self.SimResV_X.setText(QCoreApplication.translate("Dialog", u"1920", None))
        self.SimResV_Y.setText(QCoreApplication.translate("Dialog", u"1080", None))
        self.SequenceBox.setTitle(QCoreApplication.translate("Dialog", u"Sequence", None))
        self.SimResT_1.setText(QCoreApplication.translate("Dialog", u"X", None))
        self.SimResB.setItemText(0, QCoreApplication.translate("Dialog", u"FHD_1080", None))
        self.SimResB.setItemText(1, QCoreApplication.translate("Dialog", u"4K_2160", None))
        self.SimResB.setItemText(2, QCoreApplication.translate("Dialog", u"Custom", None))

        self.SimListReloadB.clicked.connect(self.load_folder_list)
        self.SimListReloadB.clicked.connect(self.update_sim_list_tree)




        self.ToolWidget.setCurrentIndex(0)
        self.mastTap.setCurrentIndex(0)


        self.statusbar.showMessage('Ready')

        # 사이드바 업데이트
        self.updateSidebarWithTabs()

        # QUndoStack 초기화
        self.undoStack = QUndoStack()

        # 전역 Undo 및 Redo 액션 생성
        undo_action = QAction("Undo", MainWindow)
        undo_action.setShortcut("Ctrl+Z")
        undo_action.triggered.connect(self.undoAction)  # undoAction 메서드에 연결

        redo_action = QAction("Redo", MainWindow)
        redo_action.setShortcut("Ctrl+Shift+Z")
        redo_action.triggered.connect(self.redoAction)  # redoAction 메서드에 연결


        QMetaObject.connectSlotsByName(MainWindow)

    def setupSimListTree(self):
        # SimListTree의 최상위 항목에 "Start Frame"과 "End Frame"에 대한 QLineEdit 추가
        for i in range(self.SimListTree.topLevelItemCount()):
            top_item = self.SimListTree.topLevelItem(i)
            self.addLineEditToStartFrameColumn(top_item)
            self.addLineEditToEndFrameColumn(top_item)

    def addLineEditToStartFrameColumn(self, item, column=3):
        MaStartFrame = self.MaStartFrameV.text()
        line_edit = QLineEdit()
        line_edit.setText(item.text(column))  # 현재 "Start Frame"의 텍스트를 QLineEdit에 설정
        line_edit.editingFinished.connect(lambda it=item, le=line_edit: self.onStartFrameChanged(it, le.text()))
        line_edit.setFixedSize(130,20)
        line_edit.setText(MaStartFrame)
        self.SimListTree.setItemWidget(item, column, line_edit)

    def addLineEditToEndFrameColumn(self, item, column=4):
        line_edit = QLineEdit()
        line_edit.setText(item.text(column))  # 현재 "End Frame"의 텍스트를 QLineEdit에 설정
        line_edit.editingFinished.connect(lambda it=item, le=line_edit: self.onEndFrameChanged(it, le.text()))
        line_edit.setFixedSize(65,20)
        self.SimListTree.setItemWidget(item, column, line_edit)

    def onStartFrameChanged(self, item, text):
        # "Start Frame" 값이 변경되었을 때의 동작을 정의
        item.setText(3, text)  # 변경된 값을 샷 아이템의 "Start Frame" 열에 설정
    def onEndFrameChanged(self, item, text):
        # "End Frame" 값이 변경될 때 수행할 동작
        print(f"End Frame of {item.text(0)} changed to {text}")
    def updateResolutionFields(self, index):
        if self.SimResB.itemText(index) == "FHD_1080":
            self.SimResV_X.setText("1920")
            self.SimResV_Y.setText("1080")
            self.SimResV_X.setReadOnly(True)
            self.SimResV_Y.setReadOnly(True)
        elif self.SimResB.itemText(index) == "4K_2160":
            self.SimResV_X.setText("3840")
            self.SimResV_Y.setText("2160")
            self.SimResV_X.setReadOnly(True)
            self.SimResV_Y.setReadOnly(True)
        elif self.SimResB.itemText(index) == "Custom":
            self.SimResV_X.setReadOnly(False)
            self.SimResV_Y.setReadOnly(False)

    # Undo 액션에 연결할 메서드
    def undoAction(self):
        if self.lastEditedLineEdit and self.undoStack.canUndo():
            self.undoStack.undo()
            self.lastEditedLineEdit.setFocus()  # 포커스 이동

    # Redo 액션에 연결할 메서드
    def redoAction(self):
        if self.lastEditedLineEdit and self.undoStack.canRedo():
            self.undoStack.redo()
            self.lastEditedLineEdit.setFocus()  # 포커스 이동

    def retranslateUi(self, MainWindow):

        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actiontesrt.setText(QCoreApplication.translate("MainWindow", u"tesrt", None))
        self.actionNew.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.actionClose.setText(QCoreApplication.translate("MainWindow", u"Close", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.actionLoad.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.actionRedo.setText(QCoreApplication.translate("MainWindow", u"Redo", None))
        self.actionUndo.setText(QCoreApplication.translate("MainWindow", u"Undo", None))
        self.HelpT.setText(QCoreApplication.translate("MainWindow", u"Watch The Guide Video", None))
        self.AboutT.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.actionSidebarControler.setText(QCoreApplication.translate("MainWindow", u"Navigator", None))
        self.MaProjectSaveB.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.MaListLogB.setText(QCoreApplication.translate("MainWindow", u"Log", None))
        self.MaListT.setText(QCoreApplication.translate("MainWindow", u"Shot List", None))
        self.MaProjectLoadB.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.MaStartFrameT.setText(QCoreApplication.translate("MainWindow", u"Start Frame", None))
        self.MaProjectT.setText(QCoreApplication.translate("MainWindow", u"Project", None))
        ___qtreewidgetitem = self.MaListTree.headerItem()
        ___qtreewidgetitem.setText(8, QCoreApplication.translate("MainWindow", u"", None));
        ___qtreewidgetitem.setText(7, QCoreApplication.translate("MainWindow", u"CH", None));
        ___qtreewidgetitem.setText(6, QCoreApplication.translate("MainWindow", u"Statement", None));
        ___qtreewidgetitem.setText(5, QCoreApplication.translate("MainWindow", u"CFX Version", None));
        ___qtreewidgetitem.setText(4, QCoreApplication.translate("MainWindow", u"Ani Version", None));
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("MainWindow", u"Modeling", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("MainWindow", u"T Pose", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("MainWindow", u"Shot Number", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"", None));


        __sortingEnabled = self.MaListTree.isSortingEnabled()
        self.MaListTree.setSortingEnabled(False)
        ___qtreewidgetitem1 = self.MaListTree.topLevelItem(0)
        ___qtreewidgetitem1.setText(6, QCoreApplication.translate("MainWindow", u"Error", None));
        ___qtreewidgetitem1.setText(5, QCoreApplication.translate("MainWindow", u"v02", None));
        ___qtreewidgetitem1.setText(4, QCoreApplication.translate("MainWindow", u"v03", None));
        ___qtreewidgetitem1.setText(3, QCoreApplication.translate("MainWindow", u"Issue detected", None));
        ___qtreewidgetitem1.setText(2, QCoreApplication.translate("MainWindow", u"OK", None));
        ___qtreewidgetitem1.setText(1, QCoreApplication.translate("MainWindow", u"ABC_ep01_001_0010", None));
        ___qtreewidgetitem2 = self.MaListTree.topLevelItem(1)
        ___qtreewidgetitem2.setText(6, QCoreApplication.translate("MainWindow", u"Error", None));
        ___qtreewidgetitem2.setText(5, QCoreApplication.translate("MainWindow", u"v02", None));
        ___qtreewidgetitem2.setText(4, QCoreApplication.translate("MainWindow", u"v03", None));
        ___qtreewidgetitem2.setText(3, QCoreApplication.translate("MainWindow", u"Issue detected", None));
        ___qtreewidgetitem2.setText(2, QCoreApplication.translate("MainWindow", u"None", None));
        ___qtreewidgetitem2.setText(1, QCoreApplication.translate("MainWindow", u"ABC_ep01_001_0020", None));
        ___qtreewidgetitem3 = self.MaListTree.topLevelItem(2)
        ___qtreewidgetitem3.setText(6, QCoreApplication.translate("MainWindow", u"Done", None));
        ___qtreewidgetitem3.setText(5, QCoreApplication.translate("MainWindow", u"v04", None));
        ___qtreewidgetitem3.setText(4, QCoreApplication.translate("MainWindow", u"v04", None));
        ___qtreewidgetitem3.setText(3, QCoreApplication.translate("MainWindow", u"OK", None));
        ___qtreewidgetitem3.setText(2, QCoreApplication.translate("MainWindow", u"OK", None));
        ___qtreewidgetitem3.setText(1, QCoreApplication.translate("MainWindow", u"ABC_ep01_001_0030", None));
        ___qtreewidgetitem4 = self.MaListTree.topLevelItem(3)
        ___qtreewidgetitem4.setText(6, QCoreApplication.translate("MainWindow", u"Done", None));
        ___qtreewidgetitem4.setText(5, QCoreApplication.translate("MainWindow", u"v02", None));
        ___qtreewidgetitem4.setText(4, QCoreApplication.translate("MainWindow", u"v02", None));
        ___qtreewidgetitem4.setText(3, QCoreApplication.translate("MainWindow", u"OK", None));
        ___qtreewidgetitem4.setText(2, QCoreApplication.translate("MainWindow", u"OK", None));
        ___qtreewidgetitem4.setText(1, QCoreApplication.translate("MainWindow", u"ABC_ep01_001_0040", None));
        self.MaListTree.setSortingEnabled(__sortingEnabled)
        self.MaListTree.header().setSectionResizeMode(0, QHeaderView.Fixed)
        self.MaListTree.header().resizeSection(0, 55)
        self.MaListTree.header().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.MaListTree.header().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.MaListTree.header().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.MaListTree.header().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.MaListTree.header().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.MaListTree.header().setSectionResizeMode(6, QHeaderView.ResizeToContents)
        self.MaListTree.header().setSectionResizeMode(7, QHeaderView.ResizeToContents)

        self.MaProjectV.setText(QCoreApplication.translate("MainWindow", u"ABC", None))
        self.MaAllCreateB.setText(QCoreApplication.translate("MainWindow", u"Create All Scenes", None))
        self.MaShotPathV.setText(QCoreApplication.translate("MainWindow", u"", None))
        self.MastBox.setTitle(QCoreApplication.translate("MainWindow", u"Master", None))
        self.MaShotPathT.setText(QCoreApplication.translate("MainWindow", u"Shot Path", None))
        self.MaShotPathB.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.MaCountT.setText(QCoreApplication.translate("MainWindow", u"Master File Counts", None))
        self.MaStartFrameV.setText(QCoreApplication.translate("MainWindow", u"", None))
        self.MaSelCreateB.setText(QCoreApplication.translate("MainWindow", u"Create Selected Scenes", None))
        self.MaCachePathB.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.MaCachePathV.setText(QCoreApplication.translate("MainWindow", u"", None))
        self.MaCachePathT.setText(QCoreApplication.translate("MainWindow", u"Output Cache Path", None))
        self.ToolWidget.setTabText(self.ToolWidget.indexOf(self.MasterTap), QCoreApplication.translate("MainWindow", u"Master", None))
        self.SimListT.setText(QCoreApplication.translate("MainWindow", u"Shot List", None))
        self.SimListB.setText(QCoreApplication.translate("MainWindow", u"Run", None))
        self.SimSelB.setText(QCoreApplication.translate("MainWindow", u"Select All", None))
        self.SimDeselB.setText(QCoreApplication.translate("MainWindow", u"Deselect All", None))
        ___qtreewidgetitem5 = self.SimListTree.headerItem()
        ___qtreewidgetitem5.setText(8, QCoreApplication.translate("MainWindow", u"", None));
        ___qtreewidgetitem5.setText(7, QCoreApplication.translate("MainWindow", u"", None));
        ___qtreewidgetitem5.setText(6, QCoreApplication.translate("MainWindow", u"Viewport Preview", None));
        ___qtreewidgetitem5.setText(5, QCoreApplication.translate("MainWindow", u"Sequence Preview", None));
        ___qtreewidgetitem5.setText(4, QCoreApplication.translate("MainWindow", u"End Frame", None));
        ___qtreewidgetitem5.setText(3, QCoreApplication.translate("MainWindow", u"Simulation Start Frame", None));
        ___qtreewidgetitem5.setText(2, QCoreApplication.translate("MainWindow", u"Statement", None));
        ___qtreewidgetitem5.setText(1, QCoreApplication.translate("MainWindow", u"CFX Version", None));
        ___qtreewidgetitem5.setText(0, QCoreApplication.translate("MainWindow", u"Shot Number", None));

        __sortingEnabled1 = self.SimListTree.isSortingEnabled()
        self.SimListTree.setSortingEnabled(False)

        self.SimListTree.setSortingEnabled(__sortingEnabled1)
        self.SimListTree.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.SimListTree.header().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.SimListTree.header().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.SimListTree.header().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.SimListTree.header().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.SimListTree.header().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.SimListTree.header().setSectionResizeMode(6, QHeaderView.ResizeToContents)
        self.SimListTree.header().setSectionResizeMode(7, QHeaderView.ResizeToContents)

        self.ToolWidget.setTabText(self.ToolWidget.indexOf(self.SimulationTap), QCoreApplication.translate("MainWindow", u"Simulation", None))
        self.menutes.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))

        self.Client_T.setTitle(QCoreApplication.translate("Dialog", u"Client", None))
        ___qtreewidgetitem21 = self.ClientListTree.headerItem()
        ___qtreewidgetitem21.setText(4, QCoreApplication.translate("Dialog", u"Ping", None));
        ___qtreewidgetitem21.setText(3, QCoreApplication.translate("Dialog", u"Last Status Update", None));
        ___qtreewidgetitem21.setText(2, QCoreApplication.translate("Dialog", u"Status ", None));
        ___qtreewidgetitem21.setText(1, QCoreApplication.translate("Dialog", u"Machine Name", None));
        ___qtreewidgetitem21.setText(0, QCoreApplication.translate("Dialog", u"Worker Name", None));

        __sortingEnabled2 = self.ClientListTree.isSortingEnabled()
        self.ClientListTree.setSortingEnabled(False)
        ___qtreewidgetitem22 = self.ClientListTree.topLevelItem(0)
        ___qtreewidgetitem22.setText(4, QCoreApplication.translate("Dialog", u"72", None));
        ___qtreewidgetitem22.setText(3, QCoreApplication.translate("Dialog", u"3.3 s ago", None));
        ___qtreewidgetitem22.setText(2, QCoreApplication.translate("Dialog", u"Idle", None));
        ___qtreewidgetitem22.setText(1, QCoreApplication.translate("Dialog", u"DESKTOP-N5BDMQI", None));
        ___qtreewidgetitem22.setText(0, QCoreApplication.translate("Dialog", u"1", None));
        ___qtreewidgetitem23 = self.ClientListTree.topLevelItem(1)
        ___qtreewidgetitem23.setText(4, QCoreApplication.translate("Dialog", u"30", None));
        ___qtreewidgetitem23.setText(3, QCoreApplication.translate("Dialog", u"5.1 s ago", None));
        ___qtreewidgetitem23.setText(2, QCoreApplication.translate("Dialog", u"Rendering", None));
        ___qtreewidgetitem23.setText(1, QCoreApplication.translate("Dialog", u"DESKTOP-LPNJ54", None));
        ___qtreewidgetitem23.setText(0, QCoreApplication.translate("Dialog", u"2", None));
        ___qtreewidgetitem24 = self.ClientListTree.topLevelItem(2)
        ___qtreewidgetitem24.setText(2, QCoreApplication.translate("Dialog", u"Offline", None));
        ___qtreewidgetitem24.setText(1, QCoreApplication.translate("Dialog", u"DESKTOP-K5UBJ21", None));
        ___qtreewidgetitem24.setText(0, QCoreApplication.translate("Dialog", u"3", None));
        self.ClientListTree.setSortingEnabled(__sortingEnabled2)

        self.ClientAdd_B.setText(QCoreApplication.translate("Dialog", u"Add", None))
        self.ClientDel_B.setText(QCoreApplication.translate("Dialog", u"Delete", None))
        self.Job_T.setTitle(QCoreApplication.translate("Dialog", u"Job", None))
        ___qtreewidgetitem25 = self.JobListTree.headerItem()
        ___qtreewidgetitem25.setText(6, QCoreApplication.translate("Dialog", u"Submit Date", None));
        ___qtreewidgetitem25.setText(5, QCoreApplication.translate("Dialog", u"Frames", None));
        ___qtreewidgetitem25.setText(4, QCoreApplication.translate("Dialog", u"Task Progress", None));
        ___qtreewidgetitem25.setText(3, QCoreApplication.translate("Dialog", u"Status", None));
        ___qtreewidgetitem25.setText(2, QCoreApplication.translate("Dialog", u"Errors", None));
        ___qtreewidgetitem25.setText(1, QCoreApplication.translate("Dialog", u"User", None));
        ___qtreewidgetitem25.setText(0, QCoreApplication.translate("Dialog", u"Name", None));

        __sortingEnabled3 = self.JobListTree.isSortingEnabled()
        self.JobListTree.setSortingEnabled(False)
        ___qtreewidgetitem26 = self.JobListTree.topLevelItem(0)
        ___qtreewidgetitem26.setText(6, QCoreApplication.translate("Dialog", u"2023/01/16 17:34:24", None));
        ___qtreewidgetitem26.setText(5, QCoreApplication.translate("Dialog", u"1-150", None));
        ___qtreewidgetitem26.setText(3, QCoreApplication.translate("Dialog", u"Done", None));
        ___qtreewidgetitem26.setText(1, QCoreApplication.translate("Dialog", u"User", None));
        ___qtreewidgetitem26.setText(0, QCoreApplication.translate("Dialog", u"ABC_ep01_001_0010", None));
        ___qtreewidgetitem27 = self.JobListTree.topLevelItem(1)
        ___qtreewidgetitem27.setText(6, QCoreApplication.translate("Dialog", u"2023/01/16 15:34:24", None));
        ___qtreewidgetitem27.setText(5, QCoreApplication.translate("Dialog", u"70-150", None));
        ___qtreewidgetitem27.setText(3, QCoreApplication.translate("Dialog", u"Error", None));
        ___qtreewidgetitem27.setText(2, QCoreApplication.translate("Dialog", u"E101", None));
        ___qtreewidgetitem27.setText(1, QCoreApplication.translate("Dialog", u"User_2", None));
        ___qtreewidgetitem27.setText(0, QCoreApplication.translate("Dialog", u"ABC_ep01_001_0020", None));
        ___qtreewidgetitem28 = self.JobListTree.topLevelItem(2)
        ___qtreewidgetitem28.setText(6, QCoreApplication.translate("Dialog", u"2023/01/16 16:34:24", None));
        ___qtreewidgetitem28.setText(5, QCoreApplication.translate("Dialog", u"70-200", None));
        ___qtreewidgetitem28.setText(3, QCoreApplication.translate("Dialog", u"Queued", None));
        ___qtreewidgetitem28.setText(1, QCoreApplication.translate("Dialog", u"User", None));
        ___qtreewidgetitem28.setText(0, QCoreApplication.translate("Dialog", u"ABC_ep01_002_0010", None));
        ___qtreewidgetitem29 = self.JobListTree.topLevelItem(3)
        ___qtreewidgetitem29.setText(6, QCoreApplication.translate("Dialog", u"2023/01/16 17:34:24", None));
        ___qtreewidgetitem29.setText(5, QCoreApplication.translate("Dialog", u"70-150", None));
        ___qtreewidgetitem29.setText(3, QCoreApplication.translate("Dialog", u"Active", None));
        ___qtreewidgetitem29.setText(1, QCoreApplication.translate("Dialog", u"User", None));
        ___qtreewidgetitem29.setText(0, QCoreApplication.translate("Dialog", u"ABC_ep01_002_0050", None));
        self.JobListTree.setSortingEnabled(__sortingEnabled3)

        self.update_B.setText(QCoreApplication.translate("Dialog", u"Update", None))
        self.JobInfoPlay_B.setText(QCoreApplication.translate("Dialog", u"Play", None))
        self.JobInfoPreview.setText(QCoreApplication.translate("Dialog", u"Preview Image", None))
        self.JobNote.setTabText(self.JobNote.indexOf(self.JobInfo),
                                QCoreApplication.translate("Dialog", u"Job Info", None))
        self.JobNote.setTabText(self.JobNote.indexOf(self.JobSetting),
                                QCoreApplication.translate("Dialog", u"Job Setting", None))
        self.JobNote.setTabText(self.JobNote.indexOf(self.JobLog),
                                QCoreApplication.translate("Dialog", u"Job Log", None))
        self.ToolWidget.setTabText(self.ToolWidget.indexOf(self.RenderFarmTap),
                                   QCoreApplication.translate("Dialog", u"Render Farm", None))

        self.ToolWidget.setTabText(self.ToolWidget.indexOf(self.RenderFarmTap), QCoreApplication.translate("MainWindow", u"RenderFarm", None))


        self.actionNew.triggered.connect(self.resetMainWindow)
        self.actionSave.triggered.connect(self.saveFile)
        self.actionLoad.triggered.connect(self.loadFile)
        self.actionClose.triggered.connect(self.closeMainWindow)

        self.MaListTree.clear()




    # retranslateUi

    def updateTabs(self):
        current_tab_count = self.mastTap.count()
        desired_tab_count = self.MaCountV.value()

        if desired_tab_count > current_tab_count:
            for i in range(current_tab_count, desired_tab_count):
                new_tab = QWidget()
                tab_name = "CH_{}".format(i + 1)
                self.mastTap.addTab(new_tab, tab_name)
                self.addContentToTab(new_tab, tab_name)

                MaCHNameV = new_tab.findChild(QLineEdit, "MaCHNameV")
                if MaCHNameV:
                    MaCHNameV.textChanged.connect(lambda text, tab=new_tab: self.updateTabName(text, tab))

        elif desired_tab_count < current_tab_count:
            for i in range(current_tab_count - 1, desired_tab_count - 1, -1):
                self.mastTap.removeTab(i)

    def addInitialTab(self):
        initial_tab = QWidget()
        tab_name = "CH_1"
        self.mastTap.addTab(initial_tab, tab_name)
        self.addContentToTab(initial_tab, tab_name)

        MaCHNameV = initial_tab.findChild(QLineEdit, "MaCHNameV")
        if MaCHNameV:
            MaCHNameV.setText(tab_name)
            MaCHNameV.textChanged.connect(lambda text, tab=initial_tab: self.updateTabName(text, tab))

    def addContentToTab(self, tab, tab_name):
        MaCHNameT = QLabel(tab)
        MaCHNameT.setGeometry(10, 10, 101, 20)
        MaCHNameT.setText("Name")

        MaCHNameV = QLineEdit(tab)
        MaCHNameV.setGeometry(130, 10, 671, 20)
        MaCHNameV.setObjectName("MaCHNameV")
        MaCHNameV.setText(tab_name)

        MaFileT = QLabel(tab)
        MaFileT.setGeometry(10, 50, 101, 20)
        MaFileT.setText("Master File")

        MaFileV = QLineEdit(tab)
        MaFileV.setGeometry(130, 50, 621, 21)
        MaFileV.setObjectName("MaFileV")
        MaFileV.setText("")

        MaPathB = QPushButton(tab)
        MaPathB.setGeometry(760, 50, 41, 21)
        MaPathB.setText("...")

        MaOpenB = QPushButton(tab)
        MaOpenB.setGeometry(810, 50, 41, 23)
        MaOpenB.setText("Open")

        MaVersionT = QLabel(tab)
        MaVersionT.setGeometry(10, 90, 101, 20)
        MaVersionT.setText("Version")

        MaLogT = QPushButton(tab)
        MaLogT.setGeometry(810, 90, 41, 23)
        MaLogT.setText("Log")

        MaVersionV = QLineEdit(tab)
        MaVersionV.setGeometry(130, 90, 671, 20)
        MaVersionV.setObjectName("MaVersionV")
        MaVersionV.setText("")
        MaVersionV.setReadOnly(True)

        MaPathB.clicked.connect(lambda _: self.openFileHou(MaFileV, MaVersionV))
        MaOpenB.clicked.connect(lambda _: self.MaopenFile(MaFileV))
        MaLogT.clicked.connect(lambda: self.open_memo_dialog(tab_name))

    def find_houdini_install_path(self):
        try:
            with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, '.hip') as key:
                program_name = winreg.QueryValue(key, None)

            with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, f'{program_name}\\shell\\open\\command') as key:
                command_path, _ = winreg.QueryValueEx(key, "")
                houdini_bin_path = command_path.split('"')[1]
                houdini_bin_path = '\\'.join(houdini_bin_path.split('\\')[:-1])

                return houdini_bin_path
        except Exception as e:
            print(f"Houdini 실행 파일 경로를 찾는 데 실패했습니다: {e}")
            return None

    def updateTabName(self, new_name, tab):
        index = self.mastTap.indexOf(tab)
        if index >= 0:
            self.mastTap.setTabText(index, new_name)

    def on_ma_start_frame_v_changed(self):
        new_start_frame = self.MaStartFrameV.text()
        self.update_sim_list_tree_start_frames(new_start_frame)

    def update_sim_list_tree_start_frames(self, new_start_frame):
        # SimListTree의 모든 아이템을 순회하며 Start Frame 열을 업데이트
        for i in range(self.SimListTree.topLevelItemCount()):
            item = self.SimListTree.topLevelItem(i)
            line_edit = self.SimListTree.itemWidget(item, 3)  # 3번 열이 Start Frame
            if line_edit:
                line_edit.setText(new_start_frame)

    def openFileHou(self, MaFileV, MaVersionV):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(None, "HIP 파일 선택", "",
                                                  "Houdini Files (*.hip *.hiplc *.hipnc);;All Files (*)",
                                                  options=options)

        fileVersion = module.extract_pattern(filePath)


        if filePath:
            MaFileV.setText(filePath)
            MaVersionV.setText(fileVersion)

    def MaopenFile(self, MaFileV):
        filePath = MaFileV.text()
        if filePath:
            try:
                subprocess.Popen([filePath], shell=True)
            except Exception as e:
                print(f"파일을 열 수 없습니다: {e}")
        else:
            print("파일 경로를 입력하세요.")


    def MarunFile(self, MaFileV):
        file_path = MaFileV.text()
        if file_path:
            # Houdini 설치 디렉토리를 프로그램 실행 파일의 경로로 지정합니다.
            houdini_install_dir = self.find_houdini_install_path()

            # Houdini 실행 파일의 경로를 동적으로 생성합니다.
            if houdini_install_dir:
                houdini_exe = os.path.join(houdini_install_dir, 'houdini.exe')

                try:
                    # Houdini 프로그램으로 .hip 파일 열기
                    subprocess.Popen([houdini_exe, file_path], shell=True)
                except Exception as e:
                    print(f"파일을 열 수 없습니다: {e}")
            else:
                print("Houdini 설치 경로를 찾을 수 없습니다.")
        else:
            print("파일 경로를 입력하세요.")

    def ShotselectDirectory(self):
        dirPath = QFileDialog.getExistingDirectory(None, "폴더 선택")
        if dirPath:  # 사용자가 폴더를 선택했을 경우에만
            self.MaShotPathV.setText(dirPath)
    def CacheselectDirectory(self):
        dirPath = QFileDialog.getExistingDirectory(None, "폴더 선택")
        if dirPath:  # 사용자가 폴더를 선택했을 경우에만
            self.MaCachePathV.setText(dirPath)

    def getAllCharacterNames(self):
        character_names = []
        for i in range(self.mastTap.count()):
            tab = self.mastTap.widget(i)
            MaCHNameV = tab.findChild(QLineEdit, "MaCHNameV")
            if MaCHNameV:
                character_names.append(MaCHNameV.text())
        return character_names

    def get_all_MaFileV_values(self):
        mafilev_values = []
        for i in range(self.mastTap.count()):
            tab = self.mastTap.widget(i)
            MaFileV = tab.findChild(QLineEdit, "MaFileV")
            if MaFileV:
                mafilev_values.append(MaFileV.text())
        return mafilev_values

    def find_highest_version_file(self, folder_path, shot_number, CH_name):
        highest_version = -1
        highest_version_file = None

        # 정규 표현식을 수정하여 캐릭터 이름도 포함하게 합니다.
        pattern = re.compile(rf'{re.escape(shot_number)}_.*CH_{re.escape(CH_name)}.*_v(\d+)\.abc', re.IGNORECASE)

        # 폴더 내 파일 목록 가져오기
        files_in_folder = os.listdir(folder_path)

        for filename in files_in_folder:
            match = pattern.match(filename)
            if match:
                version = int(match.group(1))
                if version > highest_version:
                    highest_version = version
                    highest_version_file = filename

        return highest_version_file

    def find_highest_version_hip_file(self, folder_path, shot_number):
        highest_version = -1
        highest_version_hip_file = None

        pattern = re.compile(rf'{re.escape(shot_number)}_.*_v(\d+)_w(\d+)\.hip', re.IGNORECASE)
        files_in_folder = os.listdir(folder_path)

        for filename in files_in_folder:
            match = pattern.match(filename)
            if match:
                # 주 버전 및 하위 버전 모두 추출
                main_version = int(match.group(1))
                sub_version = int(match.group(2))

                # 비교를 위해 주 버전과 하위 버전을 결합 (예: 3.01)
                combined_version = main_version + sub_version * 0.01

                if combined_version > highest_version:
                    highest_version = combined_version
                    highest_version_hip_file = filename

        return highest_version_hip_file

    def find_highest_hip_version(self, folder_path, shot_number):
        """주어진 폴더와 shot number에 해당하는 최신 버전의 .hip 파일을 찾습니다."""
        pattern = re.compile(rf'{re.escape(shot_number)}.*_cfx_v(\d+)_w\d+\.hip', re.IGNORECASE)
        hip_files_in_folder = [f for f in os.listdir(folder_path) if f.endswith('.hip')]

        matching_files = [f for f in hip_files_in_folder if pattern.match(f)]

        if not matching_files:
            return None

        return max(matching_files, key=lambda x: int(pattern.match(x).group(1)))

    # 폴더 목록을 로드하는 함수
    def load_folder_list(self):
        folder_path = self.MaShotPathV.text()
        self.update_status("Ready")
        CH_names = self.getAllCharacterNames()
        self.hip_file_paths = {}
        if os.path.exists(folder_path):
            self.MaListTree.clear()
            shot_folders = os.listdir(folder_path)

            for folder_name in shot_folders:
                full_path = os.path.join(folder_path, folder_name)

                # 폴더 검사
                if os.path.isdir(full_path):
                    files_in_folder = os.listdir(full_path)
                else:
                    continue

                # 폴더 내 아이템 생성
                shot_number_item = QTreeWidgetItem(self.MaListTree)
                shot_number_item.setText(1, folder_name)
                shot_number_item.setCheckState(0, Qt.Unchecked)

                # Ani 파일 버전 검사
                ani_version_str, version_str, status_str = self.process_ani_version(folder_path, folder_name, CH_names)
                shot_number_item.setText(7, ani_version_str)
                shot_number_item.setText(4, version_str if version_str else "Error")
                shot_number_item.setText(6, status_str)

                # .hip 파일에서 CFX 버전 정보 추출
                hip_version_str = self.process_hip_version(folder_path, folder_name)
                shot_number_item.setText(5, hip_version_str)

                # 샷 넘버별 .hip 파일 경로 저장
                hip_version_str = self.process_hip_version(folder_path, folder_name)
                if hip_version_str and hip_version_str != "Error":
                    self.hip_file_paths[folder_name] = os.path.join(full_path, hip_version_str)





    def process_hip_version(self, folder_path, folder_name):
        # .hip 파일의 전체 경로를 찾습니다.
        highest_hip_file = self.find_highest_version_hip_file(folder_path, folder_name)

        # 최신 버전의 .hip 파일이 있으면 버전 정보를 추출합니다.
        if highest_hip_file:
            hip_version_match = re.search(r'_v(\d+_w\d+)\.hip', highest_hip_file)
            if hip_version_match:
                return "v" + hip_version_match.group(1).zfill(3)
            else:
                return "Error"
        else:
            return ""

    def find_full_path_of_hip_file(self, folder_path, shot_number):
        if not folder_path or not os.path.exists(folder_path):
            return ""

        hip_file = self.find_highest_version_hip_file(folder_path, shot_number)
        if hip_file:
            return os.path.join(folder_path, hip_file)
        return ""

    def process_ani_version(self, folder_path, folder_name, CH_names):
        ch_list_for_this_shot = []
        highest_ani_version_file = None
        for CH_name in CH_names:
            current_highest = self.find_highest_version_file(folder_path, folder_name, CH_name)
            if current_highest:
                ch_list_for_this_shot.append(CH_name)
                highest_ani_version_file = current_highest

        shot_version_str = ', '.join(ch_list_for_this_shot)
        if highest_ani_version_file:
            version = re.search(r'_v(\d+)\.abc', highest_ani_version_file)
            if version:
                return shot_version_str, "v" + version.group(1).zfill(3), "Ready"
            else:
                return shot_version_str, None, "Error"
        else:
            return shot_version_str, None, "Error"

    def get_version_from_hip_file(self, hip_file):
        # .hip 파일명에서 버전 정보 (예: v003)를 추출하는 함수
        version_match = re.search(r'_v(\d+)_w\d+\.hip', hip_file)
        if version_match:
            return "v" + version_match.group(1).zfill(3)
        return None


    def get_ani_version_from_abc_file(self, shot_number):
        # .abc 파일 이름에서 ani 버전을 추출하기 위한 정규 표현식 패턴을 수정합니다.
        search_pattern = f"{shot_number}_CH_.*_ani_v(\d+).abc"
        folder_path = self.MaShotPathV.text()

        if not os.path.exists(folder_path):
            raise ValueError(f"Folder path does not exist: {folder_path}")

        files = os.listdir(folder_path)
        version_files = [file for file in files if re.match(search_pattern, file)]

        if not version_files:
            raise ValueError(f"No .abc file found for shot number: {shot_number}")

        highest_version_file = max(version_files, key=lambda x: int(re.search(r"_ani_v(\d+)", x).group(1)))

        ani_version = re.search(r"_ani_v(\d+)", highest_version_file).group(1)
        return ani_version

    def create_and_run_cmd(self, mread_path, opparm_path, startF_path, mwrite_path, cmd_content_list):

        # 경로에서 'ani' 문자열을 제거합니다.
        mwrite_path = mwrite_path.replace("_ani_", "_")

        # 경로 문자열에서 \를 \\로 변경해줍니다.
        mread_path = mread_path.replace('\\', '\\\\')
        opparm_path = opparm_path.replace('\\', '\\\\')
        startF_path = startF_path.replace('\\', '\\\\')
        mwrite_path = mwrite_path.replace('\\', '\\\\')

        # .cmd 파일 내용을 리스트에 추가
        cmd_content_list.extend([
            f"mread '{mread_path}'",
            f"opparm /obj/CH/Ani fileName '{opparm_path}'",
            f"opparm /obj/Cloth_sim/vellumsolver1 startframe '{startF_path}'",
            f"opparm /obj/Hair_sim/guidesim1 startframe '{startF_path}'",
            f"mwrite '{mwrite_path}'\n"
        ])

    def create_and_run_cmd_for_all_shots(self):
        for index in range(self.MaListTree.topLevelItemCount()):
            item = self.MaListTree.topLevelItem(index)
            item.setCheckState(0, Qt.Checked)
        self.create_and_run_cmd_for_shots()

    def create_and_run_cmd_for_shots(self):

        self.update_status("Processing")

        ready_items = [self.MaListTree.topLevelItem(index) for index in range(self.MaListTree.topLevelItemCount())
                       if self.MaListTree.topLevelItem(index).checkState(0) == Qt.Checked and
                       self.MaListTree.topLevelItem(index).text(6) == "Ready"]

        if not ready_items:
            self.update_status("Done")
            return

        mafilev_values = self.get_all_MaFileV_values()
        if not mafilev_values or all(not value.strip() for value in mafilev_values):
            msg = QMessageBox()
            msg.setStyleSheet("QLabel{min-width: 200px; padding: 10px; text-align: center;}")
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Warning")
            msg.setInformativeText("Master File is Empty!")
            msg.setWindowTitle("Warning")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return

        cmd_content_list = []
        number = 1  # 번호 초기화
        unique_mafilev_values = list(set(mafilev_values))

        for mafilev_value in unique_mafilev_values:
            # mafilev_value에서 캐릭터 이름 추출
            mafilev_char_name = mafilev_value.split('/')[-1].split('_')[1]  # 파일 경로에서 캐릭터 이름을 추출


            for item in ready_items:
                shot_number = item.text(1)
                CH_names = self.getAllCharacterNames()
                CH_names_in_item = item.text(7).split(', ')  # MaListTree의 7번 열에서 캐릭터 이름을 가져옴

                for CH_name in CH_names:

                    # mafilev_char_name과 CH_name이 일치하는 경우에만 처리
                    if CH_name == mafilev_char_name and CH_name in CH_names_in_item:
                        try:
                            # 번호를 cmd_content_list에 추가
                            cmd_content_list.append(f"echo Processing Scene number: {number}")

                            ani_version = self.get_ani_version_from_abc_file(shot_number)
                            available_characters = [CH_name] # 현재 처리 중인 캐릭터만 리스트에 포함

                            mwrite_path = f"G:\\Praxis_Temp\\Praxis_CFX\\To CFX Team\\To Seongil\\Temp\\Batched-simulation_test\\master_test\\Houdini_Pipeline_Master_test\\{shot_number}_{CH_name}_cfx_ani_v{ani_version}_w01.hip"
                            # 파일이 이미 있는지 확인
                            if os.path.exists(mwrite_path):
                                msg = QMessageBox()
                                msg.setText("Already exists. Would you like to overwrite it?")
                                msg.setInformativeText(shot_number)
                                reply = msg.exec_()

                                if reply == QMessageBox.Cancel:
                                    continue

                            opparm_path = f"G:\\Praxis_Temp\\Praxis_CFX\\To CFX Team\\To Seongil\\Temp\\Batched-simulation_test\\master_test\\Houdini_Pipeline_Master_test\\Cache\\{shot_number}_CH_{CH_name}_ani_v{ani_version}.abc"
                            startF_path = self.MaStartFrameV.text()

                            self.create_and_run_cmd(mafilev_value, opparm_path, startF_path, mwrite_path,
                                                    cmd_content_list)

                            number += 1

                            item.setText(6, "Done")
                        except Exception as e:
                            print(f"Error: {e}")
                            continue
                    else:
                        pass
        self.load_folder_list()
        self.update_sim_list_tree()

        #Cmd 파일에 저장
        file_path = os.path.join(os.path.dirname(__file__), 'CreateNewScene.cmd')

        with open(file_path, 'w') as cmd_file:
            cmd_content_list.append("quit")
            cmd_file.write("\n".join(cmd_content_list))

        houdini_path = self.find_houdini_install_path()
        env = os.environ.copy()
        env["PATH"] = f"{houdini_path};{env['PATH']}"
        number -= 1

        self.worker = HSceneMaker(file_path, houdini_path, number, self)
        self.worker.Scene_progress_message.connect(self.statusbar.showMessage)
        self.worker.start()

        self.update_status("Done")
        self.update_MaListR()

    def SimList_save_data(self):
        self.existing_data.clear()  # Clear existing data before saving
        for i in range(self.SimListTree.topLevelItemCount()):
            item = self.SimListTree.topLevelItem(i)
            shot_number = item.text(0)
            self.existing_data[shot_number] = {
                "checked": item.checkState(0) == Qt.Checked,
                "statement": self.SimListTree.itemWidget(item, 2).currentText() if self.SimListTree.itemWidget(item,
                                                                                                               2) else "",
                "start_frame": self.SimListTree.itemWidget(item, 3).text() if self.SimListTree.itemWidget(item,
                                                                                                          3) else "",
                "end_frame": self.SimListTree.itemWidget(item, 4).text() if self.SimListTree.itemWidget(item,
                                                                                                        4) else "",
                "viewport_checked": self.SimListTree.itemWidget(item, 6).findChild(
                    QCheckBox).isChecked() if self.SimListTree.itemWidget(item, 6) else False
            }

    def addLineEditToColumn(self, item, column, text="", width=None):
        # QLineEdit 위젯 생성 및 설정
        line_edit = QLineEdit()
        line_edit.setText(text)
        if width is not None:
            line_edit.setFixedWidth(width)  # 고정된 너비 설정
        if column == 3:  # Simulation Start Frame
            line_edit.textChanged.connect(lambda text, item=item: self.on_line_edit_changed(item, text, "start"))
        elif column == 4:  # End Frame
            line_edit.textChanged.connect(lambda text, item=item: self.on_line_edit_changed(item, text, "end"))

        self.SimListTree.setItemWidget(item, column, line_edit)
        return line_edit

    def on_line_edit_changed(self, item, text, frame_type):
        shot_number = item.text(0)  # Shot Number 추출
        if frame_type == "start":
            self.update_shot_tab_start_frame(shot_number, text)
        elif frame_type == "end":
            self.update_shot_tab_end_frame(shot_number, text)

    # ShotTab의 Start Frame 및 End Frame 업데이트
    def update_shot_tab_start_frame(self, shot_number, new_start_frame):
        shot_tab_module = modules.get("shot_tab")
        ShotTab = shot_tab_module.ShotTab
        for i in range(self.ToolWidget.count()):
            tab = self.ToolWidget.widget(i)
            if isinstance(tab, ShotTab) and tab.shot_number == shot_number:
                tab.RangeV1.setText(new_start_frame)  # RangeV1 업데이트

    def update_shot_tab_end_frame(self, shot_number, new_end_frame):
        shot_tab_module = modules.get("shot_tab")
        ShotTab = shot_tab_module.ShotTab
        for i in range(self.ToolWidget.count()):
            tab = self.ToolWidget.widget(i)
            if isinstance(tab, ShotTab) and tab.shot_number == shot_number:
                tab.RangeV2.setText(new_end_frame)  # RangeV2 업데이트


    def update_sim_list_tree_start_frame(self, shot_number, new_start_frame):
        # SimListTree의 아이템을 순회하며 해당 샷 번호의 Start Frame을 업데이트
        for i in range(self.SimListTree.topLevelItemCount()):
            item = self.SimListTree.topLevelItem(i)
            if item.text(0) == shot_number:
                line_edit = self.SimListTree.itemWidget(item, 3)  # 3번 열이 Start Frame
                if line_edit:
                    line_edit.setText(new_start_frame)

    def update_sim_list_tree_end_frame(self, shot_number, new_end_frame):
        # SimListTree의 아이템을 순회하며 해당 샷 번호의 End Frame을 업데이트
        for i in range(self.SimListTree.topLevelItemCount()):
            item = self.SimListTree.topLevelItem(i)
            if item.text(0) == shot_number:
                line_edit = self.SimListTree.itemWidget(item, 4)  # 4번 열이 End Frame
                if line_edit:
                    line_edit.setText(new_end_frame)

    def update_sim_list_tree(self):
        self.SimList_save_data()  # Update the method call
        self.SimListTree.clear()

        # MaListTree의 모든 topLevelItem을 가져와 처리합니다.
        for i in range(self.MaListTree.topLevelItemCount()):
            ma_item = self.MaListTree.topLevelItem(i)
            shot_number = ma_item.text(1)
            cfx_version = ma_item.text(5)
            characters = ma_item.text(7)

            ch_list = characters.split(',') if characters else []

            default_start_frame = self.MaStartFrameV.text()  # MaStartFrameV의 기본값 가져오기

            # CFX Version 데이터가 있는지 확인합니다.
            if cfx_version.strip():  # 공백을 제거하고 내용이 있는지 확인
                # SimListTree에 새로운 아이템을 추가합니다.
                new_item = QTreeWidgetItem(self.SimListTree)
                new_item.setCheckState(0, Qt.Unchecked)  # 체크박스 상태를 Unchecked로 설정합니다.
                new_item.setText(0, shot_number)  # Shot Number 컬럼
                new_item.setText(1, cfx_version)  # CFX Version 컬럼

                # QLineEdit 추가 (기본값 및 너비 설정)
                start_frame_edit = self.addLineEditToColumn(new_item, 3, default_start_frame, width=130)
                end_frame_edit = self.addLineEditToColumn(new_item, 4, width=100)

                self.SimListTree.itemChanged.connect(self.on_item_changed)

                # QComboBox 추가
                combo_box = QComboBox()
                combo_box.setStyleSheet("QComboBox { background-color: white; }")

                status_list = ["Ready", "WIP", "Send to Sup", "SupRT", "SupOK", "Send to Client", "ClientRT",
                               "ClientOK", "Hold", "Delete"]
                combo_box.addItems(status_list)
                self.SimListTree.setItemWidget(new_item, 2, combo_box)
                # QComboBox 변경 시그널 연결
                combo_box.currentTextChanged.connect(lambda text, item=new_item: self.on_combo_box_changed(item, text))

                # Progress bar 생성
                progress_container = QWidget()
                layout_progrss = QHBoxLayout()  # 가로로 배치될 수 있도록 QHBoxLayout 사용
                progressBar = QProgressBar()

                progressBar.setTextVisible(False)

                # 배경색을 블랙과 화이트의 농도로 설정
                black_intensity = 242  # 블랙의 농도 (0부터 255까지)
                white_intensity = 255  # 화이트의 농도 (0부터 255까지)
                style = f"""
                    QProgressBar {{
                        border: none;
                        background-color: rgba({black_intensity}, {black_intensity}, {black_intensity}, 255);
                    }}

                    QProgressBar::chunk {{
                        background-color: rgb(36, 145, 255);   
                    }}
                """
                progressBar.setStyleSheet(style)
                layout_progrss.setContentsMargins(2, 3, 5, 2)  # 여백 설정
                # ProgressBar의 크기를 조절합니다.
                progressBar.setMinimumSize(36, 14)  # 최소 가로 너비와 세로 높이 설정
                progressBar.setMaximumSize(36, 14)  # 최대 가로 너비와 세로 높이 설정
                layout_progrss.addWidget(progressBar)  # QProgressBar를 컨테이너 위젯에 추가
                progress_container.setLayout(layout_progrss)

                self.SimListTree.setItemWidget(new_item, 7, progress_container)

                # Shot Number가 있는 항목에만 체크박스와 버튼 추가
                if shot_number:
                    # QWidget와 QHBoxLayout 생성
                    widget = QWidget()
                    layout = QHBoxLayout(widget)
                    layout.setContentsMargins(0, 0, 0, 0)  # 마진 제거

                    # 체크박스 추가
                    checkbox = QCheckBox()
                    layout.addWidget(checkbox)

                    # 버튼 추가
                    preview_button = QPushButton("")
                    icon_path = os.path.join(icon_directory, 'play_video.png')
                    preview_button.setIcon(QIcon(icon_path))
                    preview_button.setMinimumSize(100, 20)  # 버튼의 최소 크기 설정

                    layout.addWidget(preview_button)

                    # 위젯을 SimListTree의 항목에 추가
                    self.SimListTree.setItemWidget(new_item, 6, widget)  # 6번 열에 추가
                    viewport_file_path = self.check_viewport_preview_exists(shot_number, cfx_version)

                    #viewport 동작 추가
                    if viewport_file_path:
                            icon_on_path = os.path.join(icon_directory, 'play_video_on.png')
                            preview_button.setIcon(QIcon(icon_on_path))
                            # 클릭 이벤트 연결
                            preview_button.clicked.connect(partial(self.play_video, viewport_file_path))


                if shot_number:
                    sequence_preview_button = QPushButton("")
                    icon_path = os.path.join(icon_directory, 'play_video.png')
                    sequence_preview_button.setIcon(QIcon(icon_path))
                    self.SimListTree.setItemWidget(new_item, 5, sequence_preview_button)

                    file_path = self.check_preview_exists(shot_number, cfx_version)

                    if file_path:
                        icon_on_path = os.path.join(icon_directory, 'play_video_on.png')
                        sequence_preview_button.setIcon(QIcon(icon_on_path))
                        # 클릭 이벤트 연결
                        sequence_preview_button.clicked.connect(partial(self.play_video, file_path))

                if file_path:
                    icon_on_path = os.path.join(icon_directory, 'play_video_on.png')
                    sequence_preview_button.setIcon(QIcon(icon_on_path))
                    sequence_preview_button.clicked.connect(lambda fp=file_path: self.play_video(fp))

                # 새로운 항목에 저장된 데이터 적용
                if shot_number in self.existing_data:
                    new_item.setCheckState(0,
                                           Qt.Checked if self.existing_data[shot_number]["checked"] else Qt.Unchecked)
                    combo_box.setCurrentText(self.existing_data[shot_number]["statement"])
                    start_frame_edit.setText(self.existing_data[shot_number]["start_frame"])
                    end_frame_edit.setText(self.existing_data[shot_number]["end_frame"])
                    checkbox.setChecked(self.existing_data[shot_number]["viewport_checked"])

                # 캐릭터 이름들을 하위 항목으로 추가합니다.
                if characters:
                    for character_name in characters.split(','):
                        # 각 캐릭터 이름에 대한 하위 항목 생성
                        character_item = QTreeWidgetItem(new_item)
                        character_item.setCheckState(0, Qt.Unchecked)
                        character_item.setText(0, character_name.strip())  # 캐릭터 이름 설정

        # SimListTree의 순서대로 탭 재정렬을 위한 함수
        def reorder_tabs(self, shot_numbers_in_order):
            reserved_tabs = ["Master", "Simulation", "RenderFarm"]  # 건너뛸 탭 이름 지정
            start_index = len(reserved_tabs)  # 재정렬을 시작할 인덱스 설정

            for shot_number in shot_numbers_in_order:
                for index in range(start_index, self.ToolWidget.count()):
                    if self.ToolWidget.tabText(index) == shot_number:
                        target_index = start_index + shot_numbers_in_order.index(shot_number)
                        self.ToolWidget.tabBar().moveTab(index, target_index)
                        break

        # SimListTree의 Shot Number를 가져옵니다.
        shot_numbers_in_order = []
        for i in range(self.SimListTree.topLevelItemCount()):
            item = self.SimListTree.topLevelItem(i)
            shot_number = item.text(0)  # SimListTree에서 Shot Number가 있는 컬럼
            if shot_number and shot_number not in shot_numbers_in_order:
                shot_numbers_in_order.append(shot_number)

        # 체크된 항목에 대한 작업
        for i in range(self.SimListTree.topLevelItemCount()):
            item = self.SimListTree.topLevelItem(i)
            if item.checkState(0) == Qt.Checked:  # 첫 번째 컬럼이 체크 상태인지 확인
                shot_number = item.text(0)
                # 체크된 항목에 대한 작업 수행
                # 예: 진행 상태 업데이트, Houdini 명령 실행 등
                self.perform_task_for_checked_item(shot_number)


        # 기존 탭 제거
        existing_tabs_to_remove = []
        for i in range(self.ToolWidget.count()):
            tab_text = self.ToolWidget.tabText(i)
            if tab_text not in ["Master", "Simulation", "RenderFarm"] and tab_text not in shot_numbers_in_order:
                existing_tabs_to_remove.append(tab_text)

        for tab_text in existing_tabs_to_remove:
            index = self.ToolWidget.indexOf(self.ToolWidget.findChild(QWidget, f"{tab_text}_Tab"))
            if index != -1:
                self.ToolWidget.removeTab(index)

        # 새 탭 추가
        for shot_number in shot_numbers_in_order:
            tab_name = f"{shot_number}_Tab"
            tab_exists = False

            # 탭이 이미 존재하는지 확인
            for index in range(self.ToolWidget.count()):
                if self.ToolWidget.tabText(index) == shot_number:
                    tab_exists = True
                    break

            # 탭이 존재하지 않으면 새 탭 추가
            if not tab_exists:
                cfx_version = ""
                ch_list = []
                hip_path = ""
                # SimListTree에서 해당 shot_number의 CFX Version, 캐릭터 목록 및 hip_path 찾기
                for i in range(self.SimListTree.topLevelItemCount()):
                    sim_item = self.SimListTree.topLevelItem(i)
                    if sim_item.text(0) == shot_number:
                        cfx_version = sim_item.text(1)
                        folder_path = self.MaShotPathV.text()
                        hip_path = self.find_full_path_of_hip_file(folder_path, shot_number)
                        # 하위 항목에서 캐릭터 목록 추출
                        for j in range(sim_item.childCount()):
                            child_item = sim_item.child(j)
                            ch_list.append(child_item.text(0))  # 캐릭터 이름 추출
                        break

                # ShotTab 모듈을 동적으로 불러옵니다.
                shot_tab_module = modules.get("shot_tab")
                if shot_tab_module:
                    new_tab = shot_tab_module.ShotTab(shot_number=shot_number, cfx_version=cfx_version, ch_list=ch_list, hip_path=hip_path, main_window=self)
                    # 새 탭에 대한 시그널 연결
                    self.connect_shot_tab_signals(new_tab)
                    new_tab.setObjectName(tab_name)  # 탭 객체에 이름 설정
                    self.ToolWidget.addTab(new_tab, shot_number)  # 탭에 텍스트 설정
                else:
                    print("ShotTab module not found.")



        # 탭 순서 재정렬
        reorder_tabs(self, shot_numbers_in_order)

        # 최종 탭 상태 확인
        final_tabs = [self.ToolWidget.tabText(i) for i in range(self.ToolWidget.count())]

        # 탭의 변경이 완료된 후 사이드바 업데이트
        self.updateSidebarWithTabs()

    # ShotTab 시그널 연결 함수
    def connect_shot_tab_signals(self, shot_tab):
        shot_tab.statementChanged.connect(self.on_shot_tab_statement_changed)

    # 새 ShotTab 인스턴스 생성 및 연결 함수
    def add_new_shot_tab(self, shot_number, cfx_version, ch_list, hip_path):
        new_tab = ShotTab(shot_number, cfx_version, ch_list, hip_path, self)
        self.connect_shot_tab_signals(new_tab)

    # ShotTab에서 Statement 변경 감지 시 호출되는 함수
    def on_shot_tab_statement_changed(self, shot_number, new_statement):
        # SimListTree 업데이트
        for i in range(self.SimListTree.topLevelItemCount()):
            item = self.SimListTree.topLevelItem(i)
            if item.text(0) == shot_number:
                combo_box = self.SimListTree.itemWidget(item, 2)
                combo_box.setCurrentText(new_statement)
                break

    # ShotTab의 Statement를 업데이트하는 함수
    def update_shot_tab_statement(self, shot_number, new_statement):
        for i in range(self.ToolWidget.count()):
            tab = self.ToolWidget.widget(i)
            if isinstance(tab, ShotTab) and tab.shot_number == shot_number:
                tab.ShotStateV.setCurrentText(new_statement)
                break

    # SimListTree 아이템이 변경될 때 호출되는 함수
    def on_sim_list_tree_item_changed(self, item, column):
        if column == 2:  # 2번 열이 Statement 열인지 확인
            shot_number = item.text(0)
            new_statement = self.SimListTree.itemWidget(item, column).currentText()
            self.update_shot_tab_statement(shot_number, new_statement)

    # ShotTab의 Statement를 업데이트하는 함수
    def update_shot_tab_statement(self, shot_number, new_statement):
        # ShotTab 클래스를 shot_tab_module에서 참조
        shot_tab_module = modules.get("shot_tab")
        ShotTab = shot_tab_module.ShotTab

        for i in range(self.ToolWidget.count()):
            tab = self.ToolWidget.widget(i)
            # tab이 ShotTab 인스턴스인지 확인
            if isinstance(tab, ShotTab) and tab.shot_number == shot_number:
                tab.ShotStateV.setCurrentText(new_statement)
                break
    def on_combo_box_changed(self, item, text):
        # SimListTree의 아이템과 연결된 QComboBox의 텍스트가 변경될 때 호출
        shot_number = item.text(0)
        self.update_shot_tab_statement(shot_number, text)

    def get_end_frame_from_sim_list_tree(self, shot):
        # SimListTree에서 주어진 End Frame 불러옴.
        for i in range(self.SimListTree.topLevelItemCount()):
            item = self.SimListTree.topLevelItem(i)
            if item.text(0) == shot:  # 샷 넘버와 일치하는 항목을 찾음
                end_frame_widget = self.SimListTree.itemWidget(item, 4)  # "End Frame" 열의 QLineEdit
                if end_frame_widget:
                    return end_frame_widget.text()

    def get_start_frame_from_sim_list_tree(self, shot):
        # SimListTree에서 주어진 start Frame 불러옴.
        for i in range(self.SimListTree.topLevelItemCount()):
            item = self.SimListTree.topLevelItem(i)
            if item.text(0) == shot:  # 샷 넘버와 일치하는 항목을 찾음
                Start_frame_widget = self.SimListTree.itemWidget(item, 3)  # "Start Frame" 열의 QLineEdit
                if Start_frame_widget:
                    return Start_frame_widget.text()

    def find_item_in_sim_list_tree(self, shot_number):
        # SimListTree에서 주어진 Shot Number를 검색합니다.
        for i in range(self.SimListTree.topLevelItemCount()):
            if self.SimListTree.topLevelItem(i).text(0) == shot_number:
                return True  # Shot Number가 이미 존재합니다.
        return False  # Shot Number가 존재하지 않습니다.

    def select_all_sim_items(self):
        # SimListTree의 모든 최상위 항목을 순회합니다.
        for i in range(self.SimListTree.topLevelItemCount()):
            top_item = self.SimListTree.topLevelItem(i)
            top_item.setCheckState(0, Qt.Checked)  # 최상위 항목을 선택됨으로 설정합니다.

            # 모든 자식 항목을 순회하며 선택됨으로 설정합니다.
            for j in range(top_item.childCount()):
                child_item = top_item.child(j)
                child_item.setCheckState(0, Qt.Checked)

    def deselect_all_sim_items(self):
        # SimListTree의 모든 최상위 항목을 순회합니다.
        for i in range(self.SimListTree.topLevelItemCount()):
            top_item = self.SimListTree.topLevelItem(i)
            top_item.setCheckState(0, Qt.Unchecked)  # 최상위 항목을 선택 해제됨으로 설정합니다.

            # 모든 자식 항목을 순회하며 선택 해제됨으로 설정합니다.
            for j in range(top_item.childCount()):
                child_item = top_item.child(j)
                child_item.setCheckState(0, Qt.Unchecked)

    def update_MaListR(self):
        # 'Done' 상태의 항목 수를 확인
        done_count = sum(1 for index in range(self.MaListTree.topLevelItemCount())
                         if self.MaListTree.topLevelItem(index).text(6) == "Done")


    def on_item_changed(self, item, column):
        if column == 0 and item.parent() is None:  # 첫 번째 열의 체크박스 상태 변경 감지 및 상위 항목 확인
            self.update_child_items(item, item.checkState(column))

    def update_child_items(self, parent_item, state):
        for i in range(parent_item.childCount()):
            child_item = parent_item.child(i)
            child_item.setCheckState(0, state)  # 하위 항목의 체크 상태를 부모와 동일하게 설정

    def check_preview_exists(self, shot_number, cfx_version):
        # MaShotPathV에 render\images 경로를 추가하여 탐색
        preview_path = self.MaShotPathV.text()
        suffix = r'render\images'
        preview_path = os.path.join(preview_path, suffix)

        # 정규 표현식 패턴 설정
        pattern = re.compile(rf"{shot_number}.*{cfx_version}\.mp4")

        try:
            for filename in os.listdir(preview_path):
                if pattern.match(filename):
                    full_path = os.path.normpath(os.path.join(preview_path, filename))
                    return full_path
        except Exception as e:
            pass

        return None

    def check_viewport_preview_exists(self, shot_number, cfx_version):
        # Viewport Preview 파일 경로 생성
        preview_path = self.MaShotPathV.text()
        suffix = r'render\images'
        preview_path = os.path.join(preview_path, suffix)
        # 정규 표현식 패턴 설정
        pattern = re.compile(rf"{shot_number}.*{cfx_version}\_following.mp4")
        try:
            for filename in os.listdir(preview_path):
                if pattern.match(filename):
                    full_path = os.path.normpath(os.path.join(preview_path, filename))
                    return full_path
        except Exception as e:
            pass

    def play_video(self, file_path):
        if file_path:
            print(f"Attempting to play video: {file_path}")
            try:
                # 파일 경로를 따옴표로 묶음
                cmd = f'cmd /c start "" "{file_path}"'
                subprocess.run(cmd, shell=True, check=True)
            except Exception as e:
                print(f"Error playing video: {e}")

    def update_simlist_progress(self, shot_name, progress):
        for i in range(self.SimListTree.topLevelItemCount()):
            item = self.SimListTree.topLevelItem(i)
            if item.text(0) == shot_name:  # 샷 이름과 일치하는 항목 찾기
                progress_container = self.SimListTree.itemWidget(item, 7)  # 진행률 컨테이너
                if progress_container:
                    for j in range(progress_container.layout().count()):
                        widget = progress_container.layout().itemAt(j).widget()
                        if isinstance(widget, QProgressBar):
                            widget.setValue(int(progress))  # 진행률 업데이트
                            break

    def perform_task_for_checked_item(self, shot_number, progress=None):
        # progress가 제공되지 않았을 경우 기본값 설정
        if progress is None:
            progress = 0.0  # 또는 적절한 기본값 사용

        for i in range(self.SimListTree.topLevelItemCount()):
            item = self.SimListTree.topLevelItem(i)
            if item.text(0) == shot_number:
                progress_container = self.SimListTree.itemWidget(item, 7)
                if progress_container:
                    for j in range(progress_container.layout().count()):
                        widget = progress_container.layout().itemAt(j).widget()
                        if isinstance(widget, QProgressBar):
                            widget.setValue(progress)
                            break

    def update_render_cmd(self):
        selected_shots = self.get_checked_shots()
        render_cmd_path = os.path.join(os.path.dirname(__file__), 'render.cmd')

        folder_path = self.MaShotPathV.text()  # .hip 파일이 위치한 폴더 경로
        error_occurred = False  # 오류 발생 여부를 추적하는 플래그

        frames_info = []  # 각 샷의 프레임 범위를 저장할 리스트

        # 모든 샷에 대한 "End Frame" 값이 있는지 확인
        for shot in selected_shots:
            self.perform_task_for_checked_item(shot, 0)
            end_frame = self.get_end_frame_from_sim_list_tree(shot)
            start_frame = self.get_start_frame_from_sim_list_tree(shot)
            StartFrameSeq = self.SimStartFrameV.text()  # 클래스 속성을 사용하는 경우

            if not end_frame.strip():  # "End Frame" 값이 비어있는 경우
                self.show_warning_message("Please check the end frame and try again")
                error_occurred = True  # 오류 발생

            if not StartFrameSeq.strip():  # "Start Frame" 값이 비어있는 경우
                self.show_warning_message("Please check the start frame and try again")
                error_occurred = True  # 오류 발생

            # frames_info에 프레임 범위 추가
            frames_info.append((int(StartFrameSeq), int(end_frame)))

        if error_occurred:
            return  # 오류가 발생했으므로 함수 실행 중단


        with open(render_cmd_path, 'w') as file:
            for i, (shot, (start_frame, end_frame)) in enumerate(zip(selected_shots, frames_info)):
                hip_path = self.find_full_path_of_hip_file(folder_path, shot)
                hip_path = hip_path.replace("\\", "\\\\")
                hip_path = hip_path.replace("/", "\\\\")  # 경로 구분자 통일

                Seqstart_frame = self.SimStartFrameV.text()
                start_frame = self.get_start_frame_from_sim_list_tree(shot)
                end_frame = self.get_end_frame_from_sim_list_tree(shot)

                # Viewport Preview 체크 상태 확인
                is_viewport_preview_checked = self.is_viewport_preview_checked(shot)

                if hip_path:
                    file.write(f'echo shot:"{shot} number:{i+1}"\n')
                    file.write(f'mread "{hip_path}"\n')
                    file.write(f'opparm /obj/Preview/Preview_Exporter range1 {Seqstart_frame}  range2  {end_frame}\n')
                    file.write(f'opparm /obj/Cloth_sim/vellumsolver1 startframe {start_frame}\nopparm /obj/Hair_sim/guidesim1 startframe {start_frame}\n')
                    file.write('render -V /obj/Preview/Preview_Exporter/ropnet1/Export\n')

                    if is_viewport_preview_checked:
                        # Viewport Preview가 체크된 경우 추가 명령을 포함
                        file.write(f'opparm /obj/Preview/Preview_Exporter cam /obj/following_cam\n')
                        file.write(f'opparm /obj/Preview/Preview_Exporter range1 {start_frame} range2 {end_frame}\n')
                        file.write('render -V /obj/Preview/Preview_Exporter/ropnet1/Export\n')

            file.write('quit\n')

        # HBatchWorker 인스턴스 생성
        houdini_path = self.find_houdini_install_path()
        env = os.environ.copy()
        env["PATH"] = f"{houdini_path};{env['PATH']}"

        self.worker = HBatchWorker(render_cmd_path, houdini_path, frames_info, self)
        self.worker.progress_message.connect(self.statusbar.showMessage)
        self.worker.progress_updated.connect(self.SimBar.setValue)
        self.worker.update_request.connect(self.update_sim_list_tree)
        self.worker.start()

    def is_viewport_preview_checked(self, shot_number):
        for i in range(self.SimListTree.topLevelItemCount()):
            item = self.SimListTree.topLevelItem(i)
            if item.text(0) == shot_number:  # Shot Number 컬럼이 일치하는지 확인
                container_widget = self.SimListTree.itemWidget(item, 6)  # QWidget 컨테이너
                if container_widget:
                    layout = container_widget.layout()  # QHBoxLayout
                    if layout:
                        checkbox_widget = layout.itemAt(0).widget()  # 첫 번째 위젯이 QCheckBox
                        if isinstance(checkbox_widget, QCheckBox):
                            return checkbox_widget.isChecked()
        return False

    def show_warning_message(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Warning")
        msg.setInformativeText(text)
        msg.setWindowTitle("Warning")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setStyleSheet("QLabel{min-width: 250px; padding: 10px; text-align: center;}"
                          "QMessageBoxWarningIcon { margin-right: 10px; align: center; }"
                          )
        msg.exec_()

    def get_checked_shots(self):
        checked_shots = []
        for i in range(self.SimListTree.topLevelItemCount()):
            item = self.SimListTree.topLevelItem(i)
            if item.checkState(0) == Qt.Checked:
                shot_number = item.text(0)  # 체크된 샷 넘버 가져오기
                checked_shots.append(shot_number)
        return checked_shots

    def Reload_shot_tab(self):
        shot_tab_module = modules.get("shot_tab")

        if shot_tab_module:
            # SimListTree의 모든 아이템을 순회합니다.
            for i in range(self.SimListTree.topLevelItemCount()):
                item = self.SimListTree.topLevelItem(i)
                shot_number = item.text(0)  # 0열에 있는 샷 번호
                cfx_version = item.text(1)  # 1열에 있는 CFX 버전 정보
                folder_path = self.MaShotPathV.text()
                hip_path = self.find_full_path_of_hip_file(folder_path, shot_number)  # hip_path 조회

                # 하위 항목에서 캐릭터 목록 추출
                ch_list = []
                for j in range(item.childCount()):
                    child_item = item.child(j)
                    ch_list.append(child_item.text(0))  # 캐릭터 이름 추출

                # ShotTab 인스턴스 생성
                shot_tab_instance = shot_tab_module.ShotTab(shot_number, cfx_version, ch_list, hip_path, self)

                # process_cfx_version 메서드 호출
                shot_tab_instance.process_cfx_version()
        else:
            print("ShotTab module not found.")

    def open_memo_dialog(self, tab_name=None):
        # 메모 다이얼로그 창 생성
        memo_dialog = QDialog()
        memo_dialog.setWindowTitle(f"{tab_name if tab_name else '전체 리스트'} - 메모")

        # 메모 작성을 위한 QTextEdit 위젯 생성
        memo_text_edit = QTextEdit(memo_dialog)

        # 전달된 tab_name이 None이면 전체 리스트의 메모를 불러오고, 그렇지 않으면 특정 탭의 메모를 불러옴
        if tab_name:
            # 특정 탭의 메모 불러오기
            memo_text_edit.setPlainText(self.tab_memos.get(tab_name, ""))
        else:
            # 전체 리스트의 메모 불러오기
            memo_text_edit.setPlainText(self.saved_memo_content)

        # 'Cancel'과 'Save' 버튼 생성
        cancel_button = QPushButton("Cancel")
        save_button = QPushButton("Save")

        # 'Cancel' 버튼 클릭 시 다이얼로그 닫기 연결
        cancel_button.clicked.connect(memo_dialog.close)

        # 'Save' 버튼 클릭 시 호출될 함수
        def save_memo():
            if tab_name:
                # 특정 탭의 메모 저장
                self.tab_memos[tab_name] = memo_text_edit.toPlainText()
            else:
                # 전체 리스트의 메모 저장
                self.saved_memo_content = memo_text_edit.toPlainText()

            # 저장 후 다이얼로그 닫기
            memo_dialog.close()

        # 'Save' 버튼을 save_memo 함수에 연결
        save_button.clicked.connect(save_memo)

        # 다이얼로그 레이아웃 설정
        button_layout = QHBoxLayout()
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(save_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(memo_text_edit)
        main_layout.addLayout(button_layout)
        memo_dialog.setLayout(main_layout)

        # 다이얼로그 표시
        memo_dialog.exec()

        # 슬롯 함수 정의
    def on_off_sidebar(self):
        # 사이드바의 표시 상태를 변경
        new_visibility = not self.sideBarDockWidget.isVisible()
        self.sideBarDockWidget.setVisible(new_visibility)

        # 메뉴 항목의 체크 상태를 업데이트
        self.actionSidebarControler.setChecked(new_visibility)

    def on_sidebar_visibility_changed(self, visible):
        # 사이드바 가시성에 따라 메뉴 항목 체크 상태 업데이트
        self.actionSidebarControler.setChecked(visible)

    # 탭 전환을 위한 범용 함수
    def switch_to_tab(self, tab_name):
        index = self.find_tab_index(tab_name)
        if index != -1:
            self.ToolWidget.setCurrentIndex(index)

    # 탭 이름으로 인덱스 찾는 함수
    def find_tab_index(self, tab_name):
        for i in range(self.ToolWidget.count()):
            if self.ToolWidget.tabText(i) == tab_name:
                return i
        return -1

    # Help 웹사이트로 이동하는 함수
    # OpenAI Chat 웹사이트로 이동하는 함수
    def open_help(self):
        url = QUrl("https://chat.openai.com/")
        QDesktopServices.openUrl(url)

    def open_about(self):
        msg = QMessageBox()

        # Scripts 폴더에서 build_time.txt 파일 읽기
        build_time_file_path = os.path.join(module_directory, "build_time.txt")
        print(build_time_file_path)
        try:
            with open(build_time_file_path, "r") as file:
                build_time = file.read().strip()
        except FileNotFoundError:
            build_time = "Unknown"

        # 텍스트 설정
        informative_text = f"Build 0.3.0-alpha.1, built on {build_time}\n\n" \
                           "Powered by Houdini\n" \
                           "Copyright © 2023 SEONGIL LEE"
        msg.setText("CFX for Houdini 2024.0.0")

        # 굵은 글꼴 설정
        font = QFont()
        font.setBold(True)
        msg.setFont(font)

        msg.setInformativeText(informative_text)
        msg.setWindowTitle("About")
        msg.setStandardButtons(QMessageBox.Close)
        msg.exec()

    def resetMainWindow(self):
        global MainWindow
        MainWindow.close()
        MainWindow = QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.setWindowTitle('CFX For HOUDINI')
        MainWindow.show()


    def closeMainWindow(self):
        # MainWindow를 닫음
        MainWindow.close()

    def saveFile(self):
        file_path, _ = QFileDialog.getSaveFileName(MainWindow, "Save Configuration", "", "CFX HOUDINI (*.cfx)")
        if file_path:
            file_name = file_path.split("/")[-1]
            MainWindow.setWindowTitle(f"{file_name} - CFX For HOUDINI")
            if not file_path.endswith('.cfx'):
                file_path += '.cfx'
            settings = QSettings(file_path, QSettings.IniFormat)
            settings.setValue("MaProjectV", self.MaProjectV.text())
            settings.setValue("MaCountV", self.MaCountV.value())
            # Save values from dynamically added tabs
            for i in range(self.mastTap.count()):
                tab = self.mastTap.widget(i)
                MaCHNameV = tab.findChild(QLineEdit, "MaCHNameV")
                MaFileV = tab.findChild(QLineEdit, "MaFileV")
                MaVersionV = tab.findChild(QLineEdit, "MaVersionV")
                if MaCHNameV:
                    key = f"Tab_{i}_MaCHNameV"
                    settings.setValue(key, MaCHNameV.text())
                if MaFileV:
                    key = f"Tab_{i}_MaFileV"
                    settings.setValue(key, MaFileV.text())
                if MaVersionV:
                    key = f"Tab_{i}_MaVersionV"
                    settings.setValue(key, MaVersionV.text())
                # Save memo content for each tab
                tab_name = self.mastTap.tabText(i)  # Get the name of the tab
                memo_key = f"Tab_{i}_Memo"  # Create a unique key for the memo content
                memo_content = self.tab_memos.get(tab_name, "")  # Get the memo content from the dictionary
                settings.setValue(memo_key, memo_content)  # Save the memo content in the settings

            settings.setValue("MaStartFrameV", self.MaStartFrameV.text())
            settings.setValue("MaShotPathV", self.MaShotPathV.text())
            settings.setValue("MaCachePathV", self.MaCachePathV.text())

            tree_items = []
            for index in range(self.MaListTree.topLevelItemCount()):
                item = self.MaListTree.topLevelItem(index)
                tree_items.append({
                    'checked': item.checkState(0) == Qt.Checked,
                    'texts': [item.text(i) for i in range(item.columnCount())]
                })
            settings.setValue("MaListTreeItems", tree_items)

            # 메모 내용 저장
            settings.setValue("MemoContent", self.saved_memo_content)

            #Simulation Tap_Save
            settings.setValue("SimFrameRateV", self.SimFrameRateV.text())
            settings.setValue("SimStartFrameV", self.SimStartFrameV.text())
            settings.setValue("SimResV_X", self.SimResV_X.text())
            settings.setValue("SimResV_Y", self.SimResV_Y.text())
            settings.setValue("SimResB", self.SimResB.currentIndex())

            # SimListTree 항목 저장
            sim_list_items = []
            for index in range(self.SimListTree.topLevelItemCount()):
                item = self.SimListTree.topLevelItem(index)
                # 체크박스 상태 저장
                checked = item.checkState(0) == Qt.Checked
                start_frame_edit = self.SimListTree.itemWidget(item, 3)  # QLineEdit
                end_frame_edit = self.SimListTree.itemWidget(item, 4)  # QLineEdit

                item_data = {
                    'checked': checked,
                    'shot_number': item.text(0),
                    'cfx_version': item.text(1),
                    'status': self.SimListTree.itemWidget(item, 2).currentText(),  # QComboBox의 현재 텍스트
                    'start_frame': start_frame_edit.text() if start_frame_edit else "",
                    'end_frame': end_frame_edit.text() if end_frame_edit else "",
                    # Sequence Preview와 Viewport Preview 상태 저장
                    'sequence_preview_exists': self.check_preview_exists(item.text(0), item.text(1)),
                    'viewport_preview_exists': self.check_viewport_preview_exists(item.text(0), item.text(1)),
                    'viewport_checked': self.SimListTree.itemWidget(item, 6).findChild(QCheckBox).isChecked(),
                    # 하위 항목들의 상태 저장
                    'children': [{
                        'checked': child.checkState(0) == Qt.Checked,
                        'text': child.text(0)
                    } for child in [item.child(i) for i in range(item.childCount())]],
                }
                sim_list_items.append(item_data)

            settings.setValue("SimListTreeItems", sim_list_items)

            # TODO: 다른 UI 위젯의 상태 및 값을 저장하는 코드를 추가하세요.


    def loadFile(self):
        global MainWindow

        file_path, _ = QFileDialog.getOpenFileName(MainWindow, "Load CFX HOUDINI", "", "CFX HOUDINI (*.cfx)")
        if file_path:
            self.update_sim_list_tree()
            self.load_folder_list()
            self.Reload_shot_tab()
            file_name = file_path.split("/")[-1]
            MainWindow.setWindowTitle(f"{file_name} - CFX For HOUDINI")
            settings = QSettings(file_path, QSettings.IniFormat)
            value = settings.value("MaProjectV", "")
            self.MaProjectV.setText(value)
            self.MaCountV.setValue(int(settings.value("MaCountV", 0)))
            for i in range(self.mastTap.count()):
                tab = self.mastTap.widget(i)
                MaCHNameV = tab.findChild(QLineEdit, "MaCHNameV")
                MaFileV = tab.findChild(QLineEdit, "MaFileV")
                MaVersionV = tab.findChild(QLineEdit, "MaVersionV")
                if MaCHNameV:
                    key = f"Tab_{i}_MaCHNameV"
                    value = settings.value(key, "")
                    MaCHNameV.setText(value)
                if MaFileV:
                    key = f"Tab_{i}_MaFileV"
                    value = settings.value(key, "")
                    MaFileV.setText(value)
                if MaVersionV:
                    key = f"Tab_{i}_MaVersionV"
                    value = settings.value(key, "")
                    MaVersionV.setText(value)

                # Load memo content for each tab
                memo_key = f"Tab_{i}_Memo"
                memo_content = settings.value(memo_key, "")
                tab_name = self.mastTap.tabText(i)  # Get the name of the tab
                self.tab_memos[tab_name] = memo_content  # Store the memo content in the dictionary

            self.MaStartFrameV.setText(settings.value("MaStartFrameV", ""))
            self.MaShotPathV.setText(settings.value("MaShotPathV", ""))
            self.MaCachePathV.setText(settings.value("MaCachePathV", ""))

            tree_items = settings.value("MaListTreeItems", [])
            for item_data in tree_items:
                item = QTreeWidgetItem(self.MaListTree)
                item.setCheckState(0, Qt.Checked if item_data['checked'] else Qt.Unchecked)
                for i, text in enumerate(item_data['texts']):
                    item.setText(i, text)

            # 메모 내용 불러오기
            self.saved_memo_content = settings.value("MemoContent", "")

            #Simulation Tap_Load
            self.SimFrameRateV.setText(settings.value("SimFrameRateV", ""))
            self.SimStartFrameV.setText(settings.value("SimStartFrameV", ""))
            # Load the saved value for SimResB
            sim_resb_index = settings.value("SimResB", defaultValue=0, type=int)
            self.SimResB.setCurrentIndex(sim_resb_index)
            self.SimResV_X.setText(settings.value("SimResV_X", ""))
            self.SimResV_Y.setText(settings.value("SimResV_Y", ""))

            # SimListTree 항목 불러오기
            sim_list_items = settings.value("SimListTreeItems", [])
            if sim_list_items is None:
                sim_list_items = []  # sim_list_items가 None인 경우 빈 리스트 할당
            self.SimListTree.clear()
            for item_data in sim_list_items:
                new_item = QTreeWidgetItem(self.SimListTree)
                new_item.setCheckState(0, Qt.Checked if item_data['checked'] else Qt.Unchecked)
                new_item.setText(0, item_data['shot_number'])
                new_item.setText(1, item_data['cfx_version'])

                # QComboBox 설정
                combo_box = QComboBox()
                combo_box.setStyleSheet("QComboBox { background-color: white; }")
                combo_box.addItems(["Ready", "WIP", "Send to Sup", "SupRT", "SupOK", "Send to Client", "ClientRT",
                                    "ClientOK", "Hold", "Delete"])
                combo_box.setCurrentText(item_data['status'])
                self.SimListTree.setItemWidget(new_item, 2, combo_box)

                # QLineEdit 설정
                self.addLineEditToColumn(new_item, 3, item_data['start_frame'], width=130)
                self.addLineEditToColumn(new_item, 4, item_data['end_frame'], width=100)

                # Sequence Preview 버튼 설정
                sequence_preview_button = QPushButton("")
                icon_path = os.path.join(icon_directory, 'play_video.png')
                sequence_preview_button.setIcon(QIcon(icon_path))
                self.SimListTree.setItemWidget(new_item, 5, sequence_preview_button)
                if item_data['sequence_preview_exists']:
                    icon_on_path = os.path.join(icon_directory, 'play_video_on.png')
                    sequence_preview_button.setIcon(QIcon(icon_on_path))
                    # 클릭 이벤트 연결...

                # Viewport Preview 버튼 및 체크박스 설정
                if item_data['shot_number']:
                    # QWidget와 QHBoxLayout 생성
                    widget = QWidget()
                    layout = QHBoxLayout(widget)
                    layout.setContentsMargins(0, 0, 0, 0)

                    # 체크박스 추가
                    checkbox = QCheckBox()
                    checkbox.setChecked(item_data['viewport_checked'])
                    layout.addWidget(checkbox)

                    # 버튼 추가
                    preview_button = QPushButton("")
                    icon_path = os.path.join(icon_directory, 'play_video.png')
                    preview_button.setIcon(QIcon(icon_path))
                    preview_button.setMinimumSize(100, 20)

                    # 버튼 상태 설정
                    if item_data['viewport_preview_exists']:
                        icon_on_path = os.path.join(icon_directory, 'play_video_on.png')
                        preview_button.setIcon(QIcon(icon_on_path))
                        # 클릭 이벤트 연결: 예를 들어, play_video 함수 연결
                        file_path = self.check_viewport_preview_exists(item_data['shot_number'],
                                                                       item_data['cfx_version'])
                        preview_button.clicked.connect(partial(self.play_video, file_path))

                    layout.addWidget(preview_button)

                    # 위젯을 SimListTree의 항목에 추가
                    self.SimListTree.setItemWidget(new_item, 6, widget)

                # 하위 항목들 복원
                for child_data in item_data.get('children', []):
                    child = QTreeWidgetItem(new_item)
                    child.setText(0, child_data['text'])
                    child.setCheckState(0, Qt.Checked if child_data['checked'] else Qt.Unchecked)
        else:
            self.resetMainWindow()


    # TODO: 다른 UI 위젯의 상태 및 값을 불러오는 코드를 추가하세요.
    def adjustSidebarWidth(self):
        max_width = 0
        font_metrics = QFontMetrics(self.sideBarListWidget.font())

        # 모든 항목의 텍스트 너비를 확인
        for index in range(self.sideBarListWidget.count()):
            item = self.sideBarListWidget.item(index)
            text_width = font_metrics.boundingRect(item.text()).width()
            max_width = max(max_width, text_width)

        # 여백 추가
        padding = 20
        new_width = max_width + padding

        # 사이드바의 너비를 조절
        self.sideBarDockWidget.setFixedWidth(new_width)

    def onSidebarItemClicked(self, item):
        # 클릭된 항목의 텍스트를 가져옴
        tab_name = item.text()

        # 해당 이름을 가진 탭을 찾아서 전환
        for index in range(self.ToolWidget.count()):
            if self.ToolWidget.tabText(index) == tab_name:
                self.ToolWidget.setCurrentIndex(index)
                break
    def updateSidebarWithTabs(self):
        # ToolWidget의 존재 여부를 확인
        if hasattr(self, 'ToolWidget'):
            self.sideBarListWidget.clear()  # 리스트를 클리어하고 새로운 탭 목록으로 업데이트

            for index in range(self.ToolWidget.count()):
                tab_name = self.ToolWidget.tabText(index)
                self.sideBarListWidget.addItem(tab_name)

        # 사이드바 너비 재조정
        self.adjustSidebarWidth()

    def update_status(self, message):
        self.statusbar.showMessage(message)

    def Redo_Undo(self, text):
        old_text = self.sender().previous_text  # 이전 텍스트 저장 방식에 따라 달라질 수 있음
        new_text = text
        edit_command = EditCommand(self.sender(), old_text, new_text)
        self.undoStack.push(edit_command)
class HSceneMaker(QThread):
    Scene_progress_message = Signal(str)

    def __init__(self, file_path, houdini_path, number, ui_main_window):
        super().__init__()
        self.file_path = file_path
        self.houdini_path = houdini_path
        self.number = number
        self.ui_main_window = ui_main_window

    def run(self):
        env = os.environ.copy()
        env["PATH"] = f"{self.houdini_path};{env['PATH']}"
        progress_message_signal = self.Scene_progress_message
        progress_message_signal.emit("Starting...")

        process = subprocess.Popen(f'hbatch "{self.file_path}"', shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT, env=env)

        total_scenes = self.number  # 전체 샷의 수

        while True:
            output = process.stdout.readline()
            if output == b'' and process.poll() is not None:
                break
            if output:
                output_decoded = output.decode('utf-8', 'ignore')
                print(output_decoded.strip())

                # 샷 번호와 이름 업데이트
                number_match = re.search(r"Processing Scene number: (\d+)", output_decoded.strip())
                if number_match:
                    number_name = number_match.group(1)  # 샷 이름 추출
                    progress_message_signal.emit(
                        f"Processing... ({number_name} of {total_scenes})")

        progress_message_signal.emit("Done")

class HBatchWorker(QThread):
    progress_message = Signal(str)
    progress_updated = Signal(int)
    update_request = Signal()

    def __init__(self, command_path, houdini_path, frames_info, ui_main_window):
        super().__init__()
        self.command_path = command_path
        self.houdini_path = houdini_path
        self.frames_info = frames_info
        self.ui_main_window = ui_main_window  # Ui_MainWindow 인스턴스 저장

    def run(self):
        env = os.environ.copy()
        env["PATH"] = f"{self.houdini_path};{env['PATH']}"
        progress_message_signal = self.progress_message
        progress_message_signal.emit("Starting...")

        process = subprocess.Popen(f'hbatch "{self.command_path}"', shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT, env=env)

        for i, (start_frame, end_frame) in enumerate(self.frames_info):

            total_frames = end_frame - start_frame + 1
            progress_signal = self.progress_updated
            progress_signal.emit(1) # 실행시 초기값 1

            current_shot_number = 1  # 현재 샷 번호 초기화
            total_shots = len(self.frames_info)  # 전체 샷의 수
            shot_name = ""
            # run 메서드 내에서
            while True:
                output = process.stdout.readline()
                if output == b'' and process.poll() is not None:
                    break
                if output:
                    output_decoded = output.decode('utf-8', 'ignore')
                    print(output_decoded.strip())

                    # 샷 번호와 이름 업데이트
                    shot_match = re.search(r"shot:(.+) number:(\d+)", output_decoded.strip())
                    if shot_match:
                        shot_name = shot_match.group(1)  # 샷 이름 추출
                        print(f"shot_name{shot_name}")

                        current_shot_number = int(shot_match.group(2))  # 샷 번호 추출

                        progress_message_signal.emit(
                            f"Processing... {shot_name} ({current_shot_number} of {total_shots})")

                    # 진행률 형식 감지
                    progress_match = re.search(r"Progress:\s*([\d.]+)%", output_decoded.strip())
                    if progress_match:
                        progress_percentage = float(progress_match.group(1))

                        # Ui_MainWindow 인스턴스를 통해 update_simlist_progress 호출
                        self.ui_main_window.update_simlist_progress(shot_name, progress_percentage)
                        progress_signal.emit(progress_percentage)

            # 작업 완료 시 진행률 100%로 설정
            progress_signal.emit(100.0)
            progress_message_signal.emit("Done")
            self.update_request.emit()  # GUI 업데이트 요청

# 사용자의 특정 액션을 나타내는 QUndoCommand 서브클래스
class EditCommand(QUndoCommand):
    def __init__(self, line_edit, old_text, new_text):
        super().__init__()
        self.line_edit = line_edit
        self.old_text = old_text
        self.new_text = new_text

    def undo(self):
        ui.lastEditedLineEdit = self.line_edit  # 여기서 ui는 Ui_MainWindow 인스턴스
        self.line_edit.setText(self.old_text)

    def redo(self):
        ui.lastEditedLineEdit = self.line_edit  # 여기서 ui는 Ui_MainWindow 인스턴스
        self.line_edit.setText(self.new_text)


class CustomLineEdit(QLineEdit):
    def __init__(self, undo_stack, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.undo_stack = undo_stack

    def focusInEvent(self, event):
        super().focusInEvent(event)
        QApplication.instance().setActiveUndoStack(self.undo_stack)

class ServerApp(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.start_server()

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('192.168.35.15', 8080))
        self.server_socket.listen()
        threading.Thread(target=self.accept_connections, daemon=True).start()

    def accept_connections(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            server_worker = ServerThread(client_socket)
            server_thread = QThread()
            server_worker.moveToThread(server_thread)
            server_worker.update_signal.connect(self.update_status)
            server_thread.started.connect(server_worker.run)
            server_thread.start()

    @Slot(str)
    def update_status(self, status):
        self.ui.Statement_1_E.setText(status)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.statusbar.showMessage('Ready')
    MainWindow.setWindowTitle('CFX For HOUDINI')
    ui.loadFile()
    MainWindow.show()
    sys.exit(app.exec())
