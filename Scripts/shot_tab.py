import sys
import os
import re
import json
import importlib.util
import subprocess
import glob
import winreg
from functools import partial
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, QThread, Signal, QSettings, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontMetrics, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient, QDesktopServices,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox, QHeaderView,
    QLabel, QLineEdit, QMainWindow, QDockWidget, QMenu, QCheckBox,
    QMenuBar, QProgressBar, QListWidget, QPushButton, QSizePolicy,
    QSpinBox, QStatusBar, QTabWidget, QTextEdit,
    QToolButton, QDialog, QHBoxLayout, QVBoxLayout, QTreeWidget, QFileDialog, QTreeWidgetItem, QMessageBox, QWidget)

# 현재 파일의 절대 경로를 구합니다.
current_directory = os.path.dirname(os.path.abspath(__file__))

# 'Scripts' 폴더의 경로를 구합니다.
module_directory = os.path.join(current_directory, 'Scripts')

# 현재 디렉토리의 상위 디렉토리를 구합니다.
parent_directory = os.path.dirname(current_directory)

# 상위 디렉토리를 sys.path에 추가합니다.
if parent_directory not in sys.path:
    sys.path.insert(0, parent_directory)

# 상위 디렉토리에 있는 'Houdini_Pipeline.py'를 임포트합니다.
from Houdini_Pipeline import HBatchWorker


class ShotTab(QWidget):
    # Statement 변경 시그널
    statementChanged = Signal(str, str)  # shot_number, new_statement

    def __init__(self, shot_number, cfx_version, ch_list, hip_path, main_window, parent=None):
        super(ShotTab, self).__init__(parent)
        self.shot_number = shot_number
        self.cfx_version = cfx_version
        self.ch_list = ch_list
        self.hip_path = hip_path
        self.main_window = main_window
        self.setupUi()


    def setupUi(self):
        layout = QVBoxLayout(self)  # QVBoxLayout을 이용하여 레이아웃 설정
        layout.setContentsMargins(0, 0, 10, 10)  # 여백 설정
        layout.setSpacing(0)  # 간격 설정

        self.ShotTap = QWidget(self)
        self.ShotTap.setObjectName(f"{self.shot_number}__Tab")
        layout.addWidget(self.ShotTap)

        self.ClothGrp = QGroupBox(self.ShotTap)
        self.ClothGrp.setObjectName(f"{self.shot_number}_ClothGrp")
        self.ClothGrp.setGeometry(QRect(10, 80, 431, 491))
        self.ClothTap = QTabWidget(self.ClothGrp)
        self.ClothTap.setObjectName(f"{self.shot_number}_ClothTap")
        self.ClothTap.setGeometry(QRect(10, 20, 411, 461))
        self.ClothTap_1 = QWidget()
        self.ClothTap_1.setObjectName(f"{self.shot_number}_ClothTap_1")
        self.ClothPPV = QTreeWidget(self.ClothTap_1)
        font = QFont()
        font1 = QFont()
        font1.setStrikeOut(False)
        font1.setKerning(True)
        font1.setStyleStrategy(QFont.PreferDefault)
        self.ClothPPV.headerItem().setText(0, "")
        __qtreewidgetitem16 = QTreeWidgetItem()
        __qtreewidgetitem16.setFont(0, font1);
        self.ClothPPV.setHeaderItem(__qtreewidgetitem16)
        __qtreewidgetitem17 = QTreeWidgetItem(self.ClothPPV)
        __qtreewidgetitem17.setFont(2, font);
        __qtreewidgetitem17.setTextAlignment(1, Qt.AlignLeading | Qt.AlignVCenter);
        QTreeWidgetItem(self.ClothPPV)
        QTreeWidgetItem(self.ClothPPV)
        QTreeWidgetItem(self.ClothPPV)
        QTreeWidgetItem(self.ClothPPV)
        QTreeWidgetItem(self.ClothPPV)
        QTreeWidgetItem(self.ClothPPV)
        QTreeWidgetItem(self.ClothPPV)
        QTreeWidgetItem(self.ClothPPV)
        QTreeWidgetItem(self.ClothPPV)
        QTreeWidgetItem(self.ClothPPV)
        QTreeWidgetItem(self.ClothPPV)
        QTreeWidgetItem(self.ClothPPV)
        self.ClothPPV.setObjectName(f"{self.shot_number}_ClothPPV")
        self.ClothPPV.setGeometry(QRect(10, 40, 381, 251))
        self.ClothPresetV = QComboBox(self.ClothTap_1)
        self.ClothPresetV.addItem("")
        self.ClothPresetV.addItem("")
        self.ClothPresetV.addItem("")
        self.ClothPresetV.setObjectName(f"{self.shot_number}_ClothPresetV")
        self.ClothPresetV.setGeometry(QRect(10, 10, 191, 22))
        self.ClothPresetNewB = QPushButton(self.ClothTap_1)
        self.ClothPresetNewB.setObjectName(f"{self.shot_number}_ClothPresetNewB")
        self.ClothPresetNewB.setGeometry(QRect(220, 10, 51, 23))
        self.ClothPresetSaveB = QPushButton(self.ClothTap_1)
        self.ClothPresetSaveB.setObjectName(f"{self.shot_number}_ClothPresetSaveB")
        self.ClothPresetSaveB.setGeometry(QRect(280, 10, 51, 23))
        self.ClothPresetLoadB = QPushButton(self.ClothTap_1)
        self.ClothPresetLoadB.setObjectName(f"{self.shot_number}_ClothPresetLoadB")
        self.ClothPresetLoadB.setGeometry(QRect(340, 10, 51, 23))
        self.AttPGrp = QGroupBox(self.ClothTap_1)
        self.AttPGrp.setObjectName(f"{self.shot_number}_AttPGrp")
        self.AttPGrp.setGeometry(QRect(10, 310, 381, 121))
        self.AttPPPV = QTreeWidget(self.AttPGrp)
        self.AttPPPV.headerItem().setText(0, "")
        QTreeWidgetItem(self.AttPPPV)
        QTreeWidgetItem(self.AttPPPV)
        self.AttPPPV.setObjectName(f"{self.shot_number}_AttPPPV")
        self.AttPPPV.setGeometry(QRect(10, 20, 361, 91))
        self.ClothTap.addTab(self.ClothTap_1, "")
        self.ClothTap_2 = QWidget()
        self.ClothTap_2.setObjectName(f"{self.shot_number}_ClothTap_2")
        self.ClothTap.addTab(self.ClothTap_2, "")
        self.ClothTap_3 = QWidget()
        self.ClothTap_3.setObjectName(f"{self.shot_number}_ClothTap_3")
        self.ClothTap.addTab(self.ClothTap_3, "")
        self.HairGrp = QGroupBox(self.ShotTap)
        self.HairGrp.setObjectName(f"{self.shot_number}_HairGrp")
        self.HairGrp.setGeometry(QRect(450, 80, 431, 491))
        self.HairTap = QTabWidget(self.HairGrp)
        self.HairTap.setObjectName(f"{self.shot_number}_HairTap")
        self.HairTap.setGeometry(QRect(10, 20, 411, 461))
        self.HairTap_1 = QWidget()
        self.HairTap_1.setObjectName(f"{self.shot_number}_HairTap_1")
        self.hairPresetV = QComboBox(self.HairTap_1)
        self.hairPresetV.addItem("")
        self.hairPresetV.addItem("")
        self.hairPresetV.setObjectName(f"{self.shot_number}_hairPresetV")
        self.hairPresetV.setGeometry(QRect(10, 10, 191, 22))
        self.HairPPV = QTreeWidget(self.HairTap_1)
        self.HairPPV.headerItem().setText(0, "")
        __qtreewidgetitem18 = QTreeWidgetItem()
        __qtreewidgetitem18.setFont(0, font1);
        self.HairPPV.setHeaderItem(__qtreewidgetitem18)
        __qtreewidgetitem19 = QTreeWidgetItem(self.HairPPV)
        __qtreewidgetitem19.setFont(2, font);
        __qtreewidgetitem19.setTextAlignment(1, Qt.AlignLeading | Qt.AlignVCenter);
        QTreeWidgetItem(self.HairPPV)
        QTreeWidgetItem(self.HairPPV)
        QTreeWidgetItem(self.HairPPV)
        QTreeWidgetItem(self.HairPPV)
        QTreeWidgetItem(self.HairPPV)
        QTreeWidgetItem(self.HairPPV)
        QTreeWidgetItem(self.HairPPV)
        QTreeWidgetItem(self.HairPPV)
        QTreeWidgetItem(self.HairPPV)
        QTreeWidgetItem(self.HairPPV)
        QTreeWidgetItem(self.HairPPV)
        QTreeWidgetItem(self.HairPPV)
        self.HairPPV.setObjectName(f"{self.shot_number}_HairPPV")
        self.HairPPV.setGeometry(QRect(10, 40, 381, 251))
        self.CAGrp = QGroupBox(self.HairTap_1)
        self.CAGrp.setObjectName(f"{self.shot_number}_CAGrp")
        self.CAGrp.setGeometry(QRect(10, 310, 381, 121))
        self.CAPPV = QTreeWidget(self.CAGrp)
        self.CAPPV.headerItem().setText(0, "")
        __qtreewidgetitem20 = QTreeWidgetItem()
        __qtreewidgetitem20.setFont(0, font1);
        self.CAPPV.setHeaderItem(__qtreewidgetitem20)
        __qtreewidgetitem21 = QTreeWidgetItem(self.CAPPV)
        __qtreewidgetitem21.setFont(2, font);
        __qtreewidgetitem21.setTextAlignment(1, Qt.AlignLeading | Qt.AlignVCenter);
        QTreeWidgetItem(self.CAPPV)
        QTreeWidgetItem(self.CAPPV)
        self.CAPPV.setObjectName(f"{self.shot_number}_CAPPV")
        self.CAPPV.setGeometry(QRect(10, 20, 361, 91))
        self.hairPresetNewB = QPushButton(self.HairTap_1)
        self.hairPresetNewB.setObjectName(f"{self.shot_number}_hairPresetNewB")
        self.hairPresetNewB.setGeometry(QRect(220, 10, 51, 23))
        self.HairPresetSaveB = QPushButton(self.HairTap_1)
        self.HairPresetSaveB.setObjectName(f"{self.shot_number}_HairPresetSaveB")
        self.HairPresetSaveB.setGeometry(QRect(280, 10, 51, 23))
        self.HairPresetLoadB = QPushButton(self.HairTap_1)
        self.HairPresetLoadB.setObjectName(f"{self.shot_number}_HairPresetLoadB")
        self.HairPresetLoadB.setGeometry(QRect(340, 10, 51, 23))
        self.HairTap.addTab(self.HairTap_1, "")
        self.HairTap_2 = QWidget()
        self.HairTap_2.setObjectName(f"{self.shot_number}_HairTap_2")
        self.HairTap.addTab(self.HairTap_2, "")
        self.HairTap_3 = QWidget()
        self.HairTap_3.setObjectName(f"{self.shot_number}_HairTap_3")
        self.HairTap.addTab(self.HairTap_3, "")
        self.ChV = QComboBox(self.ShotTap)
        self.ChV.setObjectName(f"{self.shot_number}_V")
        self.ChV.setGeometry(QRect(10, 10, 381, 22))
        self.AniVersionT = QLabel(self.ShotTap)
        self.AniVersionT.setObjectName(f"{self.shot_number}_AniVersionT")
        self.AniVersionT.setGeometry(QRect(10, 50, 111, 20))
        self.AniVersionV = QLineEdit(self.ShotTap)
        self.AniVersionV.setObjectName(f"{self.shot_number}_AniVersionV")
        self.AniVersionV.setGeometry(QRect(120, 50, 101, 20))
        self.AniVersionV.setReadOnly(True)
        self.RunB = QPushButton(self.ShotTap)
        self.RunB.setObjectName(f"{self.shot_number}_RunB")
        self.RunB.setGeometry(QRect(670, 10, 101, 23))
        self.OpenB = QPushButton(self.ShotTap)
        self.OpenB.setObjectName(f"{self.shot_number}_OpenB")
        self.OpenB.setGeometry(QRect(780, 10, 101, 23))
        self.CFXVersionT = QLabel(self.ShotTap)
        self.CFXVersionT.setObjectName(f"{self.shot_number}_CFXVersionT")
        self.CFXVersionT.setGeometry(QRect(240, 50, 111, 20))
        self.CFXVersionV = QLineEdit(self.ShotTap)
        self.CFXVersionV.setObjectName(f"{self.shot_number}_CFXVersionV")
        self.CFXVersionV.setGeometry(QRect(340, 50, 101, 20))
        self.CFXVersionV.setReadOnly(True)
        self.WindGrp = QGroupBox(self.ShotTap)
        self.WindGrp.setObjectName(f"{self.shot_number}_WindGrp")
        self.WindGrp.setGeometry(QRect(890, 80, 431, 491))
        self.WindTap = QTabWidget(self.WindGrp)
        self.WindTap.setObjectName(f"{self.shot_number}_WindTap")
        self.WindTap.setGeometry(QRect(10, 20, 411, 461))
        self.WindTap_1 = QWidget()
        self.WindTap_1.setObjectName(f"{self.shot_number}_WindTap_1")
        self.WindPresetV = QComboBox(self.WindTap_1)
        self.WindPresetV.addItem("")
        self.WindPresetV.addItem("")
        self.WindPresetV.setObjectName(f"{self.shot_number}_WindPresetV")
        self.WindPresetV.setGeometry(QRect(10, 10, 191, 22))
        self.WindPPV = QTreeWidget(self.WindTap_1)
        self.WindPPV.headerItem().setText(0, "")
        __qtreewidgetitem22 = QTreeWidgetItem()
        __qtreewidgetitem22.setFont(0, font1);
        self.WindPPV.setHeaderItem(__qtreewidgetitem22)
        __qtreewidgetitem23 = QTreeWidgetItem(self.WindPPV)
        __qtreewidgetitem23.setFont(2, font);
        __qtreewidgetitem23.setTextAlignment(1, Qt.AlignLeading | Qt.AlignVCenter);
        QTreeWidgetItem(self.WindPPV)
        QTreeWidgetItem(self.WindPPV)
        QTreeWidgetItem(self.WindPPV)
        QTreeWidgetItem(self.WindPPV)
        QTreeWidgetItem(self.WindPPV)
        QTreeWidgetItem(self.WindPPV)
        QTreeWidgetItem(self.WindPPV)
        self.WindPPV.setObjectName(f"{self.shot_number}_WindPPV")
        self.WindPPV.setGeometry(QRect(10, 40, 381, 251))
        self.WindDGrp = QGroupBox(self.WindTap_1)
        self.WindDGrp.setObjectName(f"{self.shot_number}_WindDGrp")
        self.WindDGrp.setGeometry(QRect(10, 310, 381, 121))
        self.WindPresetNewB = QPushButton(self.WindTap_1)
        self.WindPresetNewB.setObjectName(f"{self.shot_number}_WindPresetNewB")
        self.WindPresetNewB.setGeometry(QRect(220, 10, 51, 23))
        self.WindPresetSaveB = QPushButton(self.WindTap_1)
        self.WindPresetSaveB.setObjectName(f"{self.shot_number}_WindPresetSaveB")
        self.WindPresetSaveB.setGeometry(QRect(280, 10, 51, 23))
        self.WindPresetLoadB = QPushButton(self.WindTap_1)
        self.WindPresetLoadB.setObjectName(f"{self.shot_number}_WindPresetLoadB")
        self.WindPresetLoadB.setGeometry(QRect(340, 10, 51, 23))
        self.WindTap.addTab(self.WindTap_1, "")
        self.WindTap_2 = QWidget()
        self.WindTap_2.setObjectName(f"{self.shot_number}_WindTap_2")
        self.WindTap.addTab(self.WindTap_2, "")
        self.WindTap_3 = QWidget()
        self.WindTap_3.setObjectName(f"{self.shot_number}_WindTap_3")
        self.WindTap.addTab(self.WindTap_3, "")
        self.ConstraintsGrp = QGroupBox(self.ShotTap)
        self.ConstraintsGrp.setObjectName(f"{self.shot_number}_ConstraintsGrp")
        self.ConstraintsGrp.setGeometry(QRect(450, 580, 431, 181))
        self.ConstraintsTap = QTabWidget(self.ConstraintsGrp)
        self.ConstraintsTap.setObjectName(f"{self.shot_number}_ConstraintsTap")
        self.ConstraintsTap.setGeometry(QRect(20, 20, 411, 151))
        self.ConstraintsTap_1 = QWidget()
        self.ConstraintsTap_1.setObjectName(f"{self.shot_number}_ConstraintsTap_1")
        self.ConsPPV = QTreeWidget(self.ConstraintsTap_1)
        self.ConsPPV.headerItem().setText(0, "")
        __qtreewidgetitem24 = QTreeWidgetItem()
        __qtreewidgetitem24.setFont(0, font1);
        self.ConsPPV.setHeaderItem(__qtreewidgetitem24)
        __qtreewidgetitem25 = QTreeWidgetItem(self.ConsPPV)
        __qtreewidgetitem25.setFont(2, font);
        __qtreewidgetitem25.setTextAlignment(1, Qt.AlignLeading | Qt.AlignVCenter);
        QTreeWidgetItem(self.ConsPPV)
        self.ConsPPV.setObjectName(f"{self.shot_number}_ConsPPV")
        self.ConsPPV.setGeometry(QRect(10, 40, 381, 71))
        self.ConsPresetV = QComboBox(self.ConstraintsTap_1)
        self.ConsPresetV.addItem("")
        self.ConsPresetV.setObjectName(f"{self.shot_number}_ConsPresetV")
        self.ConsPresetV.setGeometry(QRect(10, 10, 191, 22))
        self.ConsPresetNewB = QPushButton(self.ConstraintsTap_1)
        self.ConsPresetNewB.setObjectName(f"{self.shot_number}_ConsPresetNewB")
        self.ConsPresetNewB.setGeometry(QRect(220, 10, 51, 23))
        self.ConsPresetSaveB = QPushButton(self.ConstraintsTap_1)
        self.ConsPresetSaveB.setObjectName(f"{self.shot_number}_ConsPresetSaveB")
        self.ConsPresetSaveB.setGeometry(QRect(280, 10, 51, 23))
        self.ConsPresetLoadB = QPushButton(self.ConstraintsTap_1)
        self.ConsPresetLoadB.setObjectName(f"{self.shot_number}_ConsPresetLoadB")
        self.ConsPresetLoadB.setGeometry(QRect(340, 10, 51, 23))
        self.ConstraintsTap.addTab(self.ConstraintsTap_1, "")
        self.ConstraintsTap_2 = QWidget()
        self.ConstraintsTap_2.setObjectName(f"{self.shot_number}_ConstraintsTap_2")
        self.ConstraintsTap.addTab(self.ConstraintsTap_2, "")
        self.ConstraintsTap_3 = QWidget()
        self.ConstraintsTap_3.setObjectName(f"{self.shot_number}_ConstraintsTap_3")
        self.ConstraintsTap.addTab(self.ConstraintsTap_3, "")
        self.CollidersGrp = QGroupBox(self.ShotTap)
        self.CollidersGrp.setObjectName(f"{self.shot_number}_CollidersGrp")
        self.CollidersGrp.setGeometry(QRect(890, 580, 431, 181))
        self.CollidersTap = QTabWidget(self.CollidersGrp)
        self.CollidersTap.setObjectName(f"{self.shot_number}_CollidersTap")
        self.CollidersTap.setGeometry(QRect(20, 20, 401, 151))
        self.CollidersTap_1 = QWidget()
        self.CollidersTap_1.setObjectName(f"{self.shot_number}_CollidersTap_1")
        self.ColliPPV = QTreeWidget(self.CollidersTap_1)
        self.ColliPPV.headerItem().setText(0, "")
        __qtreewidgetitem26 = QTreeWidgetItem()
        __qtreewidgetitem26.setFont(0, font1);
        self.ColliPPV.setHeaderItem(__qtreewidgetitem26)
        __qtreewidgetitem27 = QTreeWidgetItem(self.ColliPPV)
        __qtreewidgetitem27.setFont(2, font);
        __qtreewidgetitem27.setTextAlignment(1, Qt.AlignLeading | Qt.AlignVCenter);
        QTreeWidgetItem(self.ColliPPV)
        self.ColliPPV.setObjectName(f"{self.shot_number}_ColliPPV")
        self.ColliPPV.setGeometry(QRect(10, 40, 371, 71))
        self.ColliPresetV = QComboBox(self.CollidersTap_1)
        self.ColliPresetV.addItem("")
        self.ColliPresetV.setObjectName(f"{self.shot_number}_ColliPresetV")
        self.ColliPresetV.setGeometry(QRect(10, 10, 191, 22))
        self.ColliPresetLoadB = QPushButton(self.CollidersTap_1)
        self.ColliPresetLoadB.setObjectName(f"{self.shot_number}_ColliPresetLoadB")
        self.ColliPresetLoadB.setGeometry(QRect(330, 10, 51, 23))
        self.ColliPresetSaveB = QPushButton(self.CollidersTap_1)
        self.ColliPresetSaveB.setObjectName(f"{self.shot_number}_ColliPresetSaveB")
        self.ColliPresetSaveB.setGeometry(QRect(270, 10, 51, 23))
        self.ColliPresetNewB = QPushButton(self.CollidersTap_1)
        self.ColliPresetNewB.setObjectName(f"{self.shot_number}_ColliPresetNewB")
        self.ColliPresetNewB.setGeometry(QRect(210, 10, 51, 23))
        self.CollidersTap.addTab(self.CollidersTap_1, "")
        self.CollidersTap_2 = QWidget()
        self.CollidersTap_2.setObjectName(f"{self.shot_number}_CollidersTap_2")
        self.CollidersTap.addTab(self.CollidersTap_2, "")
        self.CollidersTap_3 = QWidget()
        self.CollidersTap_3.setObjectName(f"{self.shot_number}_CollidersTap_3")
        self.CollidersTap.addTab(self.CollidersTap_3, "")
        self.ResetB = QPushButton(self.ShotTap)
        self.ResetB.setObjectName(f"{self.shot_number}_ResetB")
        self.ResetB.setGeometry(QRect(560, 10, 101, 23))
        self.LogB = QPushButton(self.ShotTap)
        self.LogB.setObjectName(f"{self.shot_number}_LogB")
        self.LogB.setGeometry(QRect(400, 10, 41, 21))
        self.ShotStateT = QLabel(self.ShotTap)
        self.ShotStateT.setObjectName(f"{self.shot_number}_ShotStateT")
        self.ShotStateT.setGeometry(QRect(450, 50, 111, 20))
        self.RangeT = QLabel(self.ShotTap)
        self.RangeT.setObjectName(f"{self.shot_number}_RangeT")
        self.RangeT.setGeometry(QRect(670, 50, 111, 20))
        self.RangeV1 = QLineEdit(self.ShotTap)
        self.RangeV1.setObjectName(f"{self.shot_number}_RangeV1")
        self.RangeV1.setGeometry(QRect(730, 50, 71, 20))
        self.RangeV2 = QLineEdit(self.ShotTap)
        self.RangeV2.setObjectName(f"{self.shot_number}_RangeV2")
        self.RangeV2.setGeometry(QRect(810, 50, 71, 20))
        self.SolverGrp = QGroupBox(self.ShotTap)
        self.SolverGrp.setObjectName(f"{self.shot_number}_SolverGrp")
        self.SolverGrp.setGeometry(QRect(10, 580, 431, 181))
        self.SolverPPV = QTreeWidget(self.SolverGrp)
        self.SolverPPV.headerItem().setText(0, "")
        __qtreewidgetitem28 = QTreeWidgetItem()
        __qtreewidgetitem28.setFont(0, font1);
        self.SolverPPV.setHeaderItem(__qtreewidgetitem28)
        __qtreewidgetitem29 = QTreeWidgetItem(self.SolverPPV)
        __qtreewidgetitem29.setFont(2, font);
        __qtreewidgetitem29.setTextAlignment(1, Qt.AlignLeading | Qt.AlignVCenter);
        QTreeWidgetItem(self.SolverPPV)
        QTreeWidgetItem(self.SolverPPV)
        QTreeWidgetItem(self.SolverPPV)
        QTreeWidgetItem(self.SolverPPV)
        self.SolverPPV.setObjectName(f"{self.shot_number}_SolverPPV")
        self.SolverPPV.setGeometry(QRect(20, 50, 381, 121))
        self.SolverPresetV = QComboBox(self.SolverGrp)
        self.SolverPresetV.addItem("")
        self.SolverPresetV.setObjectName(f"{self.shot_number}_SolverPresetV")
        self.SolverPresetV.setGeometry(QRect(20, 20, 191, 22))
        self.SolverPresetNewB = QPushButton(self.SolverGrp)
        self.SolverPresetNewB.setObjectName(f"{self.shot_number}_SolverPresetNewB")
        self.SolverPresetNewB.setGeometry(QRect(230, 20, 51, 23))
        self.SolverPresetSaveB = QPushButton(self.SolverGrp)
        self.SolverPresetSaveB.setObjectName(f"{self.shot_number}_SolverPresetSaveB")
        self.SolverPresetSaveB.setGeometry(QRect(290, 20, 51, 23))
        self.SolverPresetLoadB = QPushButton(self.SolverGrp)
        self.SolverPresetLoadB.setObjectName(f"{self.shot_number}_SolverPresetLoadB")
        self.SolverPresetLoadB.setGeometry(QRect(350, 20, 51, 23))
        self.ExportB = QPushButton(self.ShotTap)
        self.ExportB.setObjectName(f"{self.shot_number}_ExportB")
        self.ExportB.setGeometry(QRect(890, 10, 101, 23))
        self.ShotStateV = QComboBox(self.ShotTap)
        self.ShotStateV.setObjectName(f"{self.shot_number}_ShotStateV")
        self.ShotStateV.setGeometry(QRect(560, 50, 101, 22))
        self.Bar = QProgressBar(self.ShotTap)
        self.Bar.setObjectName(f"{self.shot_number}_Bar")
        self.Bar.setGeometry(QRect(890, 53, 101, 15))
        self.Bar.setTextVisible(False)

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
        self.Bar.setStyleSheet(style)
        self.SaveB = QPushButton(self.ShotTap)
        self.SaveB.setObjectName(f"{self.shot_number}_SaveB")
        self.SaveB.setGeometry(QRect(1200, 10, 101, 23))
        self.LoadB = QPushButton(self.ShotTap)
        self.LoadB.setObjectName(f"{self.shot_number}_LoadB")
        self.LoadB.setGeometry(QRect(1200, 40, 101, 23))
        self.PresetV = QComboBox(self.ShotTap)
        self.PresetV.addItem("")
        self.PresetV.setObjectName(f"{self.shot_number}_PresetV")
        self.PresetV.setGeometry(QRect(1060, 10, 131, 22))

        self.ClothTap.setCurrentIndex(0)
        self.HairTap.setCurrentIndex(0)
        self.WindTap.setCurrentIndex(0)
        self.ConstraintsTap.setCurrentIndex(0)
        self.CollidersTap.setCurrentIndex(0)

        self.ClothGrp.setTitle(QCoreApplication.translate("MainWindow", u"Cloth", None))
        ___qtreewidgetitem21 = self.ClothPPV.headerItem()
        ___qtreewidgetitem21.setText(2, QCoreApplication.translate("MainWindow", u"Values", None));
        ___qtreewidgetitem21.setText(1, QCoreApplication.translate("MainWindow", u"Properties", None));
        ___qtreewidgetitem21.setText(0, QCoreApplication.translate("MainWindow", u"", None));

        __sortingEnabled2 = self.ClothPPV.isSortingEnabled()
        self.ClothPPV.setSortingEnabled(False)
        ___qtreewidgetitem22 = self.ClothPPV.topLevelItem(0)
        ___qtreewidgetitem22.setText(2, QCoreApplication.translate("MainWindow", u"1.0", None));
        ___qtreewidgetitem22.setText(1, QCoreApplication.translate("MainWindow", u"Length Scale", None));
        ___qtreewidgetitem23 = self.ClothPPV.topLevelItem(1)
        ___qtreewidgetitem23.setText(2, QCoreApplication.translate("MainWindow", u"1.0", None));
        ___qtreewidgetitem23.setText(1, QCoreApplication.translate("MainWindow", u"Density", None));
        ___qtreewidgetitem24 = self.ClothPPV.topLevelItem(2)
        ___qtreewidgetitem24.setText(2, QCoreApplication.translate("MainWindow", u"1.0", None));
        ___qtreewidgetitem24.setText(1, QCoreApplication.translate("MainWindow", u"Stretch Resistance", None));
        ___qtreewidgetitem25 = self.ClothPPV.topLevelItem(3)
        ___qtreewidgetitem25.setText(2, QCoreApplication.translate("MainWindow", u"1.0", None));
        ___qtreewidgetitem25.setText(1, QCoreApplication.translate("MainWindow", u"Stretch Damp", None));
        ___qtreewidgetitem26 = self.ClothPPV.topLevelItem(4)
        ___qtreewidgetitem26.setText(2, QCoreApplication.translate("MainWindow", u"1.0", None));
        ___qtreewidgetitem26.setText(1, QCoreApplication.translate("MainWindow", u"Shear Resistance", None));
        ___qtreewidgetitem27 = self.ClothPPV.topLevelItem(5)
        ___qtreewidgetitem27.setText(2, QCoreApplication.translate("MainWindow", u"1.0", None));
        ___qtreewidgetitem27.setText(1, QCoreApplication.translate("MainWindow", u"Bend Resistance", None));
        ___qtreewidgetitem28 = self.ClothPPV.topLevelItem(6)
        ___qtreewidgetitem28.setText(2, QCoreApplication.translate("MainWindow", u"1.0", None));
        ___qtreewidgetitem28.setText(1, QCoreApplication.translate("MainWindow", u"Bend Damp", None));
        ___qtreewidgetitem29 = self.ClothPPV.topLevelItem(7)
        ___qtreewidgetitem29.setText(2, QCoreApplication.translate("MainWindow", u"1.0", None));
        ___qtreewidgetitem29.setText(1, QCoreApplication.translate("MainWindow", u"Air Drag", None));
        ___qtreewidgetitem30 = self.ClothPPV.topLevelItem(8)
        ___qtreewidgetitem30.setText(2, QCoreApplication.translate("MainWindow", u"1.0", None));
        ___qtreewidgetitem30.setText(1, QCoreApplication.translate("MainWindow", u"Thickness", None));
        ___qtreewidgetitem31 = self.ClothPPV.topLevelItem(9)
        ___qtreewidgetitem31.setText(2, QCoreApplication.translate("MainWindow", u"1.0", None));
        ___qtreewidgetitem31.setText(1, QCoreApplication.translate("MainWindow", u"Fricton", None));
        ___qtreewidgetitem32 = self.ClothPPV.topLevelItem(10)
        ___qtreewidgetitem32.setText(2, QCoreApplication.translate("MainWindow", u"0.0", None));
        ___qtreewidgetitem32.setText(1, QCoreApplication.translate("MainWindow", u"Pressure", None));
        ___qtreewidgetitem33 = self.ClothPPV.topLevelItem(11)
        ___qtreewidgetitem33.setText(2, QCoreApplication.translate("MainWindow", u"On", None));
        ___qtreewidgetitem33.setText(1, QCoreApplication.translate("MainWindow", u"Self Collision", None));
        ___qtreewidgetitem34 = self.ClothPPV.topLevelItem(12)
        ___qtreewidgetitem34.setText(2, QCoreApplication.translate("MainWindow", u"Off", None));
        ___qtreewidgetitem34.setText(1, QCoreApplication.translate("MainWindow", u"Local Space", None));
        self.ClothPPV.setSortingEnabled(__sortingEnabled2)
        self.ClothPPV.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.ClothPPV.header().setSectionResizeMode(1, QHeaderView.ResizeToContents)

        self.ClothPresetV.setItemText(0, QCoreApplication.translate("MainWindow", u"Fabric 1", None))
        self.ClothPresetV.setItemText(1, QCoreApplication.translate("MainWindow", u"Fabric 2", None))
        self.ClothPresetV.setItemText(2, QCoreApplication.translate("MainWindow", u"Fabric 3", None))

        self.ClothPresetNewB.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.ClothPresetSaveB.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.ClothPresetLoadB.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.AttPGrp.setTitle(QCoreApplication.translate("MainWindow", u"Attribute Paint", None))
        ___qtreewidgetitem35 = self.AttPPPV.headerItem()
        ___qtreewidgetitem35.setText(2, QCoreApplication.translate("MainWindow", u"Values", None));
        ___qtreewidgetitem35.setText(1, QCoreApplication.translate("MainWindow", u"Properties", None));

        __sortingEnabled3 = self.AttPPPV.isSortingEnabled()
        self.AttPPPV.setSortingEnabled(False)
        ___qtreewidgetitem36 = self.AttPPPV.topLevelItem(0)
        ___qtreewidgetitem36.setText(2, QCoreApplication.translate("MainWindow", u"Off", None));
        ___qtreewidgetitem36.setText(1, QCoreApplication.translate("MainWindow", u"Density", None));
        ___qtreewidgetitem37 = self.AttPPPV.topLevelItem(1)
        ___qtreewidgetitem37.setText(2, QCoreApplication.translate("MainWindow", u"On", None));
        ___qtreewidgetitem37.setText(1, QCoreApplication.translate("MainWindow", u"Soft Constraint", None));
        self.AttPPPV.setSortingEnabled(__sortingEnabled3)

        self.ClothTap.setTabText(self.ClothTap.indexOf(self.ClothTap_1), QCoreApplication.translate("MainWindow", u"Cape", None))
        self.ClothTap.setTabText(self.ClothTap.indexOf(self.ClothTap_2), QCoreApplication.translate("MainWindow", u"Back", None))
        self.ClothTap.setTabText(self.ClothTap.indexOf(self.ClothTap_3), QCoreApplication.translate("MainWindow", u"Front", None))
        self.HairGrp.setTitle(QCoreApplication.translate("MainWindow", u"Hair", None))
        self.hairPresetV.setItemText(0, QCoreApplication.translate("MainWindow", u"Soft", None))
        self.hairPresetV.setItemText(1, QCoreApplication.translate("MainWindow", u"Hard", None))

        ___qtreewidgetitem38 = self.HairPPV.headerItem()
        ___qtreewidgetitem38.setText(2, QCoreApplication.translate("MainWindow", u"Values", None));
        ___qtreewidgetitem38.setText(1, QCoreApplication.translate("MainWindow", u"Properties", None));
        ___qtreewidgetitem38.setText(0, QCoreApplication.translate("MainWindow", u"", None));

        __sortingEnabled4 = self.HairPPV.isSortingEnabled()
        self.HairPPV.setSortingEnabled(False)
        ___qtreewidgetitem39 = self.HairPPV.topLevelItem(0)
        ___qtreewidgetitem39.setText(2, QCoreApplication.translate("MainWindow", u"1.0", None));
        ___qtreewidgetitem39.setText(1, QCoreApplication.translate("MainWindow", u"Self Collide", None));
        ___qtreewidgetitem40 = self.HairPPV.topLevelItem(1)
        ___qtreewidgetitem40.setText(2, QCoreApplication.translate("MainWindow", u"1.0", None));
        ___qtreewidgetitem40.setText(1, QCoreApplication.translate("MainWindow", u"Friction", None));
        ___qtreewidgetitem41 = self.HairPPV.topLevelItem(2)
        ___qtreewidgetitem41.setText(2, QCoreApplication.translate("MainWindow", u"1.0", None));
        ___qtreewidgetitem41.setText(1, QCoreApplication.translate("MainWindow", u"Stretch Resistance", None));
        ___qtreewidgetitem42 = self.HairPPV.topLevelItem(3)
        ___qtreewidgetitem42.setText(2, QCoreApplication.translate("MainWindow", u"1.0", None));
        ___qtreewidgetitem42.setText(1, QCoreApplication.translate("MainWindow", u"Stretch Damp", None));
        ___qtreewidgetitem43 = self.HairPPV.topLevelItem(4)
        ___qtreewidgetitem43.setText(2, QCoreApplication.translate("MainWindow", u"1.0", None));
        ___qtreewidgetitem43.setText(1, QCoreApplication.translate("MainWindow", u"Bend Resistance", None));
        ___qtreewidgetitem44 = self.HairPPV.topLevelItem(5)
        ___qtreewidgetitem44.setText(2, QCoreApplication.translate("MainWindow", u"1.0", None));
        ___qtreewidgetitem44.setText(1, QCoreApplication.translate("MainWindow", u"Bend Damp", None));
        ___qtreewidgetitem45 = self.HairPPV.topLevelItem(6)
        ___qtreewidgetitem45.setText(2, QCoreApplication.translate("MainWindow", u"1.0", None));
        ___qtreewidgetitem45.setText(1, QCoreApplication.translate("MainWindow", u"Twist Resistance", None));
        ___qtreewidgetitem46 = self.HairPPV.topLevelItem(7)
        ___qtreewidgetitem46.setText(2, QCoreApplication.translate("MainWindow", u"1.0", None));
        ___qtreewidgetitem46.setText(1, QCoreApplication.translate("MainWindow", u"Mass", None));
        ___qtreewidgetitem47 = self.HairPPV.topLevelItem(8)
        ___qtreewidgetitem47.setText(2, QCoreApplication.translate("MainWindow", u"1.0", None));
        ___qtreewidgetitem47.setText(1, QCoreApplication.translate("MainWindow", u"Drag", None));
        ___qtreewidgetitem48 = self.HairPPV.topLevelItem(9)
        ___qtreewidgetitem48.setText(2, QCoreApplication.translate("MainWindow", u"1.0", None));
        ___qtreewidgetitem48.setText(1, QCoreApplication.translate("MainWindow", u"Tangential Drag", None));
        ___qtreewidgetitem49 = self.HairPPV.topLevelItem(10)
        ___qtreewidgetitem49.setText(2, QCoreApplication.translate("MainWindow", u"1.0", None));
        ___qtreewidgetitem49.setText(1, QCoreApplication.translate("MainWindow", u"Mtion Drag", None));
        ___qtreewidgetitem50 = self.HairPPV.topLevelItem(11)
        ___qtreewidgetitem50.setText(2, QCoreApplication.translate("MainWindow", u"1.0", None));
        ___qtreewidgetitem50.setText(1, QCoreApplication.translate("MainWindow", u"Damp", None));
        ___qtreewidgetitem51 = self.HairPPV.topLevelItem(12)
        ___qtreewidgetitem51.setText(2, QCoreApplication.translate("MainWindow", u"Off", None));
        ___qtreewidgetitem51.setText(1, QCoreApplication.translate("MainWindow", u"Local Space", None));
        self.HairPPV.setSortingEnabled(__sortingEnabled4)

        self.HairPPV.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.HairPPV.header().setSectionResizeMode(1, QHeaderView.ResizeToContents)

        self.CAGrp.setTitle(QCoreApplication.translate("MainWindow", u"Curve Attract", None))
        ___qtreewidgetitem52 = self.CAPPV.headerItem()
        ___qtreewidgetitem52.setText(2, QCoreApplication.translate("MainWindow", u"Values", None));
        ___qtreewidgetitem52.setText(1, QCoreApplication.translate("MainWindow", u"Properties", None));
        ___qtreewidgetitem52.setText(0, QCoreApplication.translate("MainWindow", u"", None));

        __sortingEnabled5 = self.CAPPV.isSortingEnabled()
        self.CAPPV.setSortingEnabled(False)
        ___qtreewidgetitem53 = self.CAPPV.topLevelItem(0)
        ___qtreewidgetitem53.setText(2, QCoreApplication.translate("MainWindow", u"1.0", None));
        ___qtreewidgetitem53.setText(1, QCoreApplication.translate("MainWindow", u"Root", None));
        ___qtreewidgetitem54 = self.CAPPV.topLevelItem(1)
        ___qtreewidgetitem54.setText(2, QCoreApplication.translate("MainWindow", u"0.5", None));
        ___qtreewidgetitem54.setText(1, QCoreApplication.translate("MainWindow", u"Mid", None));
        ___qtreewidgetitem55 = self.CAPPV.topLevelItem(2)
        ___qtreewidgetitem55.setText(2, QCoreApplication.translate("MainWindow", u"0.0", None));
        ___qtreewidgetitem55.setText(1, QCoreApplication.translate("MainWindow", u"Tip", None));
        self.CAPPV.setSortingEnabled(__sortingEnabled5)

        self.CAPPV.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.CAPPV.header().setSectionResizeMode(1, QHeaderView.ResizeToContents)

        self.hairPresetNewB.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.HairPresetSaveB.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.HairPresetLoadB.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.HairTap.setTabText(self.HairTap.indexOf(self.HairTap_1), QCoreApplication.translate("MainWindow", u"Front", None))
        self.HairTap.setTabText(self.HairTap.indexOf(self.HairTap_2), QCoreApplication.translate("MainWindow", u"Hair", None))
        self.HairTap.setTabText(self.HairTap.indexOf(self.HairTap_3), QCoreApplication.translate("MainWindow", u"Beard", None))



        self.AniVersionT.setText(QCoreApplication.translate("MainWindow", u"Ani Cache Version", None))
        self.AniVersionV.setText(QCoreApplication.translate("MainWindow", u"v02", None))
        self.RunB.setText(QCoreApplication.translate("MainWindow", u"Run", None))
        self.OpenB.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.CFXVersionT.setText(QCoreApplication.translate("MainWindow", u"CFX Version", None))
        self.CFXVersionV.setText(QCoreApplication.translate("MainWindow", u"w01", None))
        self.WindGrp.setTitle(QCoreApplication.translate("MainWindow", u"Wind", None))
        self.WindPresetV.setItemText(0, QCoreApplication.translate("MainWindow", u"Gentle Rustling", None))
        self.WindPresetV.setItemText(1, QCoreApplication.translate("MainWindow", u"Strongly", None))

        ___qtreewidgetitem56 = self.WindPPV.headerItem()
        ___qtreewidgetitem56.setText(2, QCoreApplication.translate("MainWindow", u"Values", None));
        ___qtreewidgetitem56.setText(1, QCoreApplication.translate("MainWindow", u"Properties", None));
        ___qtreewidgetitem56.setText(0, QCoreApplication.translate("MainWindow", u"", None));

        __sortingEnabled6 = self.WindPPV.isSortingEnabled()
        self.WindPPV.setSortingEnabled(False)
        ___qtreewidgetitem57 = self.WindPPV.topLevelItem(0)
        ___qtreewidgetitem57.setText(2, QCoreApplication.translate("MainWindow", u"0.8", None));
        ___qtreewidgetitem57.setText(1, QCoreApplication.translate("MainWindow", u"Time Scale", None));
        ___qtreewidgetitem58 = self.WindPPV.topLevelItem(1)
        ___qtreewidgetitem58.setText(2, QCoreApplication.translate("MainWindow", u"5.0", None));
        ___qtreewidgetitem58.setText(1, QCoreApplication.translate("MainWindow", u"Magnitude", None));
        ___qtreewidgetitem59 = self.WindPPV.topLevelItem(2)
        ___qtreewidgetitem59.setText(2, QCoreApplication.translate("MainWindow", u"1.0", None));
        ___qtreewidgetitem59.setText(1, QCoreApplication.translate("MainWindow", u"Away From Center", None));
        ___qtreewidgetitem60 = self.WindPPV.topLevelItem(3)
        ___qtreewidgetitem60.setText(2, QCoreApplication.translate("MainWindow", u"1.0", None));
        ___qtreewidgetitem60.setText(1, QCoreApplication.translate("MainWindow", u"Direction Speed", None));
        ___qtreewidgetitem61 = self.WindPPV.topLevelItem(4)
        ___qtreewidgetitem61.setText(2, QCoreApplication.translate("MainWindow", u"1.0", None));
        ___qtreewidgetitem61.setText(1, QCoreApplication.translate("MainWindow", u"Turbulence", None));
        ___qtreewidgetitem62 = self.WindPPV.topLevelItem(5)
        ___qtreewidgetitem62.setText(2, QCoreApplication.translate("MainWindow", u"1.0", None));
        ___qtreewidgetitem62.setText(1, QCoreApplication.translate("MainWindow", u"Turbulence Speed", None));
        ___qtreewidgetitem63 = self.WindPPV.topLevelItem(6)
        ___qtreewidgetitem63.setText(2, QCoreApplication.translate("MainWindow", u"1.0", None));
        ___qtreewidgetitem63.setText(1, QCoreApplication.translate("MainWindow", u"Turbulence Freq", None));
        ___qtreewidgetitem64 = self.WindPPV.topLevelItem(7)
        ___qtreewidgetitem64.setText(2, QCoreApplication.translate("MainWindow", u"1.0", None));
        ___qtreewidgetitem64.setText(1, QCoreApplication.translate("MainWindow", u"Detail Turbulence", None));
        self.WindPPV.setSortingEnabled(__sortingEnabled6)

        self.WindPPV.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.WindPPV.header().setSectionResizeMode(1, QHeaderView.ResizeToContents)

        self.WindDGrp.setTitle(QCoreApplication.translate("MainWindow", u"Direction", None))
        self.WindPresetNewB.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.WindPresetSaveB.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.WindPresetLoadB.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.WindTap.setTabText(self.WindTap.indexOf(self.WindTap_1), QCoreApplication.translate("MainWindow", u"World", None))
        self.WindTap.setTabText(self.WindTap.indexOf(self.WindTap_2), QCoreApplication.translate("MainWindow", u"Wind 1", None))
        self.WindTap.setTabText(self.WindTap.indexOf(self.WindTap_3), QCoreApplication.translate("MainWindow", u"Wind 2", None))
        self.ConstraintsGrp.setTitle(QCoreApplication.translate("MainWindow", u"Constraints", None))
        ___qtreewidgetitem65 = self.ConsPPV.headerItem()
        ___qtreewidgetitem65.setText(2, QCoreApplication.translate("MainWindow", u"Values", None));
        ___qtreewidgetitem65.setText(1, QCoreApplication.translate("MainWindow", u"Properties", None));
        ___qtreewidgetitem65.setText(0, QCoreApplication.translate("MainWindow", u"", None));

        __sortingEnabled7 = self.ConsPPV.isSortingEnabled()
        self.ConsPPV.setSortingEnabled(False)
        ___qtreewidgetitem66 = self.ConsPPV.topLevelItem(0)
        ___qtreewidgetitem66.setText(2, QCoreApplication.translate("MainWindow", u"1.0", None));
        ___qtreewidgetitem66.setText(1, QCoreApplication.translate("MainWindow", u"Stiffness", None));
        ___qtreewidgetitem67 = self.ConsPPV.topLevelItem(1)
        ___qtreewidgetitem67.setText(2, QCoreApplication.translate("MainWindow", u"1.0", None));
        ___qtreewidgetitem67.setText(1, QCoreApplication.translate("MainWindow", u"Damping", None));
        self.ConsPPV.setSortingEnabled(__sortingEnabled7)

        self.ConsPPV.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.ConsPPV.header().setSectionResizeMode(1, QHeaderView.ResizeToContents)

        self.ConsPresetV.setItemText(0, QCoreApplication.translate("MainWindow", u"Constraint 1", None))

        self.ConsPresetNewB.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.ConsPresetSaveB.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.ConsPresetLoadB.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.ConstraintsTap.setTabText(self.ConstraintsTap.indexOf(self.ConstraintsTap_1), QCoreApplication.translate("MainWindow", u"Cape", None))
        self.ConstraintsTap.setTabText(self.ConstraintsTap.indexOf(self.ConstraintsTap_2), QCoreApplication.translate("MainWindow", u"Back", None))
        self.ConstraintsTap.setTabText(self.ConstraintsTap.indexOf(self.ConstraintsTap_3), QCoreApplication.translate("MainWindow", u"Front", None))
        self.CollidersGrp.setTitle(QCoreApplication.translate("MainWindow", u"Colliders", None))
        ___qtreewidgetitem68 = self.ColliPPV.headerItem()
        ___qtreewidgetitem68.setText(2, QCoreApplication.translate("MainWindow", u"Values", None));
        ___qtreewidgetitem68.setText(1, QCoreApplication.translate("MainWindow", u"Properties", None));
        ___qtreewidgetitem68.setText(0, QCoreApplication.translate("MainWindow", u"", None));

        __sortingEnabled8 = self.ColliPPV.isSortingEnabled()
        self.ColliPPV.setSortingEnabled(False)
        ___qtreewidgetitem69 = self.ColliPPV.topLevelItem(0)
        ___qtreewidgetitem69.setText(2, QCoreApplication.translate("MainWindow", u"1.0", None));
        ___qtreewidgetitem69.setText(1, QCoreApplication.translate("MainWindow", u"Offset", None));
        ___qtreewidgetitem70 = self.ColliPPV.topLevelItem(1)
        ___qtreewidgetitem70.setText(2, QCoreApplication.translate("MainWindow", u"0.0", None));
        ___qtreewidgetitem70.setText(1, QCoreApplication.translate("MainWindow", u"Friction", None));
        self.ColliPPV.setSortingEnabled(__sortingEnabled8)

        self.ColliPPV.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.ColliPPV.header().setSectionResizeMode(1, QHeaderView.ResizeToContents)

        self.ColliPresetV.setItemText(0, QCoreApplication.translate("MainWindow", u"Collision 1", None))

        self.ColliPresetLoadB.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.ColliPresetSaveB.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.ColliPresetNewB.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.CollidersTap.setTabText(self.CollidersTap.indexOf(self.CollidersTap_1), QCoreApplication.translate("MainWindow", u"Cape", None))
        self.CollidersTap.setTabText(self.CollidersTap.indexOf(self.CollidersTap_2), QCoreApplication.translate("MainWindow", u"Back", None))
        self.CollidersTap.setTabText(self.CollidersTap.indexOf(self.CollidersTap_3), QCoreApplication.translate("MainWindow", u"Front", None))
        self.ResetB.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
        self.LogB.setText(QCoreApplication.translate("MainWindow", u"Log", None))
        self.ShotStateT.setText(QCoreApplication.translate("MainWindow", u"Shot Statement", None))
        self.RangeT.setText(QCoreApplication.translate("MainWindow", u"Ranges", None))
        self.RangeV1.setText(QCoreApplication.translate("MainWindow", u"", None))
        self.RangeV2.setText(QCoreApplication.translate("MainWindow", u"", None))
        self.SolverGrp.setTitle(QCoreApplication.translate("MainWindow", u"Solver", None))
        ___qtreewidgetitem71 = self.SolverPPV.headerItem()
        ___qtreewidgetitem71.setText(2, QCoreApplication.translate("MainWindow", u"Values", None));
        ___qtreewidgetitem71.setText(1, QCoreApplication.translate("MainWindow", u"Properties", None));
        ___qtreewidgetitem71.setText(0, QCoreApplication.translate("MainWindow", u"", None));

        __sortingEnabled9 = self.SolverPPV.isSortingEnabled()
        self.SolverPPV.setSortingEnabled(False)
        ___qtreewidgetitem72 = self.SolverPPV.topLevelItem(0)
        ___qtreewidgetitem72.setText(2, QCoreApplication.translate("MainWindow", u"70", None));
        ___qtreewidgetitem72.setText(1, QCoreApplication.translate("MainWindow", u"Start Time", None));
        ___qtreewidgetitem73 = self.SolverPPV.topLevelItem(1)
        ___qtreewidgetitem73.setText(2, QCoreApplication.translate("MainWindow", u"3.0", None));
        ___qtreewidgetitem73.setText(1, QCoreApplication.translate("MainWindow", u"Frame Samples", None));
        ___qtreewidgetitem74 = self.SolverPPV.topLevelItem(2)
        ___qtreewidgetitem74.setText(2, QCoreApplication.translate("MainWindow", u"1.0", None));
        ___qtreewidgetitem74.setText(1, QCoreApplication.translate("MainWindow", u"Time Scale", None));
        ___qtreewidgetitem75 = self.SolverPPV.topLevelItem(3)
        ___qtreewidgetitem75.setText(2, QCoreApplication.translate("MainWindow", u"1.0", None));
        ___qtreewidgetitem75.setText(1, QCoreApplication.translate("MainWindow", u"Length Scale", None));
        ___qtreewidgetitem76 = self.SolverPPV.topLevelItem(4)
        ___qtreewidgetitem76.setText(2, QCoreApplication.translate("MainWindow", u"Off", None));
        ___qtreewidgetitem76.setText(1, QCoreApplication.translate("MainWindow", u"Local Space", None));
        self.SolverPPV.setSortingEnabled(__sortingEnabled9)

        self.SolverPPV.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.SolverPPV.header().setSectionResizeMode(1, QHeaderView.ResizeToContents)

        self.SolverPresetV.setItemText(0, QCoreApplication.translate("MainWindow", u"Solver 1", None))

        self.SolverPresetNewB.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.SolverPresetSaveB.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.SolverPresetLoadB.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.ExportB.setText(QCoreApplication.translate("MainWindow", u"Export", None))

        # ch_list에 있는 각 항목을 QComboBox에 추가
        for index, ch_name in enumerate(self.ch_list):
            self.ChV.addItem("")  # 새 항목 추가
            self.ChV.setItemText(index, QCoreApplication.translate("MainWindow", ch_name, None))

        status_list = ["Ready", "WIP", "Send to Sup", "SupRT", "SupOK", "Send to Client", "ClientRT",
                       "ClientOK", "Hold", "Delete"]
        # status_list에 있는 모든 상태를 QComboBox에 추가합니다.
        for index, status in enumerate(status_list):
            self.ShotStateV.addItem("")  # 새 항목 추가
            self.ShotStateV.setItemText(index, QCoreApplication.translate("MainWindow", status, None))
        self.SaveB.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.LoadB.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.PresetV.setItemText(0, QCoreApplication.translate("Dialog", u"Default", None))

        # Range변경에 대한 연결 설정
        self.RangeV1.textChanged.connect(lambda: self.on_range_v1_changed())
        self.RangeV2.textChanged.connect(lambda: self.on_range_v2_changed())

        # Statement 변경에 대한 연결 설정
        self.ShotStateV.currentTextChanged.connect(self.on_statement_changed)

        # cfx_version 처리 및 설정
        self.process_cfx_version()

        # Open 버튼 클릭 이벤트 연결
        self.OpenB.clicked.connect(lambda: self.open_hip(self.shot_number))

        # Run 버튼 클릭 이벤트 연결
        self.RunB.clicked.connect(self.render_cmd)

    def open_hip(self, shot_number):

        filePath = self.hip_path
        if filePath:
            try:
                subprocess.Popen([filePath], shell=True)
            except Exception as e:
                print(f"파일을 열 수 없습니다: {e}")
        else:
            pass

    def process_cfx_version(self):
        # cfx_version을 '_' 기준으로 분리
        parts = self.cfx_version.split('_')
        if len(parts) == 2:
            ani_version, cfx_version = parts
            self.AniVersionV.setText(ani_version)
            self.CFXVersionV.setText(cfx_version)

    def on_statement_changed(self, new_statement):
        # SimListTree에서 해당 샷 번호의 Statement를 업데이트
        self.update_sim_list_tree_statement(self.shot_number, new_statement)

    def update_sim_list_tree_statement(self, shot_number, new_statement):
        # 이제 main_window 참조를 사용하여 SimListTree에 접근
        for i in range(self.main_window.SimListTree.topLevelItemCount()):
            item = self.main_window.SimListTree.topLevelItem(i)
            if item.text(0) == shot_number:
                combo_box = self.main_window.SimListTree.itemWidget(item, 2)
                combo_box.setCurrentText(new_statement)
                break
    def on_statement_changed(self, new_statement):
        # SimListTree에서 해당 샷 번호의 Statement를 업데이트
        self.statementChanged.emit(self.shot_number, new_statement)

    def connect_shot_tab_signals(self, shot_tab):
        shot_tab.statementChanged.connect(self.on_shot_tab_statement_changed)

    def on_statement_changed(self):
        new_statement = self.ShotStateV.currentText()
        self.statementChanged.emit(self.shot_number, new_statement)

    def on_range_v1_changed(self):
        new_start_frame = self.RangeV1.text()
        self.main_window.update_sim_list_tree_start_frame(self.shot_number, new_start_frame)

    def on_range_v2_changed(self):
        new_end_frame = self.RangeV2.text()
        self.main_window.update_sim_list_tree_end_frame(self.shot_number, new_end_frame)

    def render_cmd(self):
        # start_frame과 end_frame 값을 ShotTab의 속성에서 가져옴
        start_frame = self.RangeV1.text()  # 예시: self.RangeV1는 시작 프레임을 나타냄
        end_frame = self.RangeV2.text()  # 예시: self.RangeV2는 종료 프레임을 나타냄


        # StartFrameSeq는 main_window 객체를 통해 가져옴
        StartFrameSeq = self.main_window.SimStartFrameV.text()

        # 오류 체크
        if not end_frame.strip():
            self.main_window.show_warning_message("Please check the end frame and try again")
            return  # 오류 발생 시 함수 종료

        if not StartFrameSeq.strip():
            self.main_window.show_warning_message("Please check the start frame and try again")
            return  # 오류 발생 시 함수 종료

        render_cmd_path = os.path.join(os.path.dirname(__file__), 'render.cmd')
        render_cmd_path = os.path.join(parent_directory, 'render.cmd')

        with open(render_cmd_path, 'w') as file:
            # 파일에 명령어 작성
            file.write(f'echo shot:"{self.shot_number} number:1"\n')
            file.write(f'mread "{self.hip_path}"\n')
            file.write(f'opparm /obj/Preview/Preview_Exporter range1 {StartFrameSeq} range2 {end_frame}\n')
            file.write('render -V /obj/Preview/Preview_Exporter/ropnet1/Export\n')
            file.write('quit\n')

        # HBatchWorker 인스턴스 생성 및 작업 시작
        houdini_path = self.main_window.find_houdini_install_path()
        env = os.environ.copy()
        env["PATH"] = f"{houdini_path};{env['PATH']}"

        frames_info = [(int(start_frame), int(end_frame))]  # 프레임 정보

        self.worker = HBatchWorker(render_cmd_path, houdini_path, frames_info, self.main_window)
        self.worker.progress_message.connect(self.main_window.statusbar.showMessage)
        self.worker.progress_updated.connect(self.Bar.setValue)
        self.worker.update_request.connect(self.main_window.update_sim_list_tree)
        self.worker.start()

