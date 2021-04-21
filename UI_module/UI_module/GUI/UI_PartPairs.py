# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file '03_PartPairs.ui'
##
## Created by: Qt User Interface Compiler version 5.15.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide2.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QIcon,
    QKeySequence,
    QLinearGradient,
    QPalette,
    QPainter,
    QPixmap,
    QRadialGradient,
)
from PySide2.QtWidgets import *


class Ui_PartPairForm(object):
    def setupUi(self, PartPairForm):
        if not PartPairForm.objectName():
            PartPairForm.setObjectName(u"PartPairForm")
        PartPairForm.resize(1000, 750)
        sizePolicy = QSizePolicy(
            QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PartPairForm.sizePolicy().hasHeightForWidth())
        PartPairForm.setSizePolicy(sizePolicy)
        PartPairForm.setMinimumSize(QSize(1000, 750))
        self.gridLayout = QGridLayout(PartPairForm)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setSizeConstraint(QLayout.SetMinimumSize)
        self.verticalLayout_2.setContentsMargins(0, -1, -1, -1)
        self.partPairs_tableView = QTableView(PartPairForm)
        self.partPairs_tableView.setObjectName(u"partPairs_tableView")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(
            self.partPairs_tableView.sizePolicy().hasHeightForWidth()
        )
        self.partPairs_tableView.setSizePolicy(sizePolicy1)
        self.partPairs_tableView.setMinimumSize(QSize(690, 640))
        self.partPairs_tableView.setFrameShape(QFrame.Box)
        self.partPairs_tableView.setFrameShadow(QFrame.Sunken)
        self.partPairs_tableView.setSizeAdjustPolicy(
            QAbstractScrollArea.AdjustToContents
        )
        self.partPairs_tableView.setDragDropMode(QAbstractItemView.DragDrop)
        self.partPairs_tableView.setShowGrid(False)
        self.partPairs_tableView.setWordWrap(False)
        self.partPairs_tableView.setCornerButtonEnabled(False)
        self.partPairs_tableView.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout_2.addWidget(self.partPairs_tableView)

        self.gridFrame = QFrame(PartPairForm)
        self.gridFrame.setObjectName(u"gridFrame")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.gridFrame.sizePolicy().hasHeightForWidth())
        self.gridFrame.setSizePolicy(sizePolicy2)
        self.gridFrame.setMinimumSize(QSize(0, 100))
        self.horizontalLayout_2 = QHBoxLayout(self.gridFrame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 9, 0, 0)
        self.horizontalSpacer = QSpacerItem(
            300, 20, QSizePolicy.Fixed, QSizePolicy.Minimum
        )

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.groupBox = QGroupBox(self.gridFrame)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy3)
        self.groupBox.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.groupBox.setFlat(False)
        self.groupBox.setCheckable(False)
        self.gridLayout_2 = QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.pushButton_geometricSimilarity = QPushButton(self.groupBox)
        self.pushButton_geometricSimilarity.setObjectName(
            u"pushButton_geometricSimilarity"
        )
        self.pushButton_geometricSimilarity.setMinimumSize(QSize(110, 0))

        self.gridLayout_2.addWidget(self.pushButton_geometricSimilarity, 2, 0, 1, 1)

        self.pushButton_featureSimilarity = QPushButton(self.groupBox)
        self.pushButton_featureSimilarity.setObjectName(u"pushButton_featureSimilarity")
        sizePolicy4 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(
            self.pushButton_featureSimilarity.sizePolicy().hasHeightForWidth()
        )
        self.pushButton_featureSimilarity.setSizePolicy(sizePolicy4)
        self.pushButton_featureSimilarity.setMinimumSize(QSize(110, 0))

        self.gridLayout_2.addWidget(self.pushButton_featureSimilarity, 1, 0, 1, 1)

        self.horizontalLayout_2.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.gridFrame)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_3 = QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(-1, -1, 9, -1)
        self.pushButton_positioning = QPushButton(self.groupBox_2)
        self.pushButton_positioning.setObjectName(u"pushButton_positioning")

        self.gridLayout_3.addWidget(self.pushButton_positioning, 2, 2, 1, 1)

        self.pushButton_deleteAll = QPushButton(self.groupBox_2)
        self.pushButton_deleteAll.setObjectName(u"pushButton_deleteAll")

        self.gridLayout_3.addWidget(self.pushButton_deleteAll, 2, 4, 1, 1)

        self.pushButton_load = QPushButton(self.groupBox_2)
        self.pushButton_load.setObjectName(u"pushButton_load")
        sizePolicy4.setHeightForWidth(
            self.pushButton_load.sizePolicy().hasHeightForWidth()
        )
        self.pushButton_load.setSizePolicy(sizePolicy4)
        self.pushButton_load.setMinimumSize(QSize(0, 53))

        self.gridLayout_3.addWidget(self.pushButton_load, 1, 0, 2, 1)

        self.pushButton_save = QPushButton(self.groupBox_2)
        self.pushButton_save.setObjectName(u"pushButton_save")
        sizePolicy4.setHeightForWidth(
            self.pushButton_save.sizePolicy().hasHeightForWidth()
        )
        self.pushButton_save.setSizePolicy(sizePolicy4)

        self.gridLayout_3.addWidget(self.pushButton_save, 1, 2, 1, 1)

        self.pushButton_reset = QPushButton(self.groupBox_2)
        self.pushButton_reset.setObjectName(u"pushButton_reset")

        self.gridLayout_3.addWidget(self.pushButton_reset, 1, 4, 1, 1)

        self.horizontalLayout_2.addWidget(self.groupBox_2)

        self.verticalLayout_2.addWidget(self.gridFrame)

        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.verticalLayout.setContentsMargins(-1, -1, -1, 6)
        self.groupBox_3 = QGroupBox(PartPairForm)
        self.groupBox_3.setObjectName(u"groupBox_3")
        sizePolicy5 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy5)
        self.groupBox_3.setMinimumSize(QSize(200, 200))
        self.gridLayout_4 = QGridLayout(self.groupBox_3)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_BodyA = QLabel(self.groupBox_3)
        self.label_BodyA.setObjectName(u"label_BodyA")
        sizePolicy4.setHeightForWidth(self.label_BodyA.sizePolicy().hasHeightForWidth())
        self.label_BodyA.setSizePolicy(sizePolicy4)
        self.label_BodyA.setMinimumSize(QSize(170, 170))
        self.label_BodyA.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(
            self.label_BodyA, 0, 0, 1, 1, Qt.AlignHCenter | Qt.AlignVCenter
        )

        self.verticalLayout.addWidget(self.groupBox_3)

        self.groupBox_4 = QGroupBox(PartPairForm)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setMinimumSize(QSize(200, 200))
        self.gridLayout_5 = QGridLayout(self.groupBox_4)
        self.gridLayout_5.setSpacing(0)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.label_BodyB = QLabel(self.groupBox_4)
        self.label_BodyB.setObjectName(u"label_BodyB")
        sizePolicy4.setHeightForWidth(self.label_BodyB.sizePolicy().hasHeightForWidth())
        self.label_BodyB.setSizePolicy(sizePolicy4)
        self.label_BodyB.setMinimumSize(QSize(170, 170))
        self.label_BodyB.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(
            self.label_BodyB, 0, 0, 1, 1, Qt.AlignHCenter | Qt.AlignVCenter
        )

        self.verticalLayout.addWidget(self.groupBox_4)

        self.pairProperties_tableView = QTableView(PartPairForm)
        self.pairProperties_tableView.setObjectName(u"pairProperties_tableView")
        sizePolicy6 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(
            self.pairProperties_tableView.sizePolicy().hasHeightForWidth()
        )
        self.pairProperties_tableView.setSizePolicy(sizePolicy6)
        self.pairProperties_tableView.setMinimumSize(QSize(300, 0))
        self.pairProperties_tableView.setFrameShape(QFrame.Box)
        self.pairProperties_tableView.horizontalHeader().setProperty(
            "showSortIndicator", True
        )

        self.verticalLayout.addWidget(self.pairProperties_tableView)

        self.pushButton_Overlay = QPushButton(PartPairForm)
        self.pushButton_Overlay.setObjectName(u"pushButton_Overlay")
        sizePolicy4.setHeightForWidth(
            self.pushButton_Overlay.sizePolicy().hasHeightForWidth()
        )
        self.pushButton_Overlay.setSizePolicy(sizePolicy4)
        self.pushButton_Overlay.setMinimumSize(QSize(200, 0))
        self.pushButton_Overlay.setMaximumSize(QSize(200, 16777215))

        self.verticalLayout.addWidget(
            self.pushButton_Overlay, 0, Qt.AlignHCenter | Qt.AlignVCenter
        )

        self.horizontalLayout.addLayout(self.verticalLayout)

        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.retranslateUi(PartPairForm)

        QMetaObject.connectSlotsByName(PartPairForm)

    # setupUi

    def retranslateUi(self, PartPairForm):
        PartPairForm.setWindowTitle(
            QCoreApplication.translate("PartPairForm", u"Form", None)
        )
        self.groupBox.setTitle(
            QCoreApplication.translate("PartPairForm", u"Preference Calculation ", None)
        )
        self.pushButton_geometricSimilarity.setText(
            QCoreApplication.translate("PartPairForm", u"Geometric Similarity", None)
        )
        self.pushButton_featureSimilarity.setText(
            QCoreApplication.translate("PartPairForm", u"Feature Similarity", None)
        )
        self.groupBox_2.setTitle(
            QCoreApplication.translate("PartPairForm", u"Data Management", None)
        )
        self.pushButton_positioning.setText(
            QCoreApplication.translate("PartPairForm", u"Positioning", None)
        )
        self.pushButton_deleteAll.setText(
            QCoreApplication.translate("PartPairForm", u"Delete all", None)
        )
        self.pushButton_load.setText(
            QCoreApplication.translate("PartPairForm", u"Load\n" "Parts", None)
        )
        self.pushButton_save.setText(
            QCoreApplication.translate("PartPairForm", u"Save", None)
        )
        self.pushButton_reset.setText(
            QCoreApplication.translate("PartPairForm", u"Reset", None)
        )
        self.groupBox_3.setTitle(
            QCoreApplication.translate("PartPairForm", u"Body A", None)
        )
        self.label_BodyA.setText(
            QCoreApplication.translate("PartPairForm", u"TextLabel", None)
        )
        self.groupBox_4.setTitle(
            QCoreApplication.translate("PartPairForm", u"Body B", None)
        )
        self.label_BodyB.setText(
            QCoreApplication.translate("PartPairForm", u"TextLabel", None)
        )
        self.pushButton_Overlay.setText(
            QCoreApplication.translate("PartPairForm", u"Build Overlay", None)
        )

    # retranslateUi
