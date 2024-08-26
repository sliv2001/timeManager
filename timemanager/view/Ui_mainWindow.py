# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainWindowoBecYq.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialogButtonBox, QGridLayout,
    QGroupBox, QLabel, QListView, QMainWindow,
    QMenuBar, QPlainTextEdit, QSizePolicy, QStatusBar,
    QTabWidget, QTextEdit, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setLocale(QLocale(QLocale.Russian, QLocale.Russia))
        MainWindow.setUnifiedTitleAndToolBarOnMac(True)
        self.removeItem = QAction(MainWindow)
        self.removeItem.setObjectName(u"removeItem")
        self.removeItem.setCheckable(False)
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditDelete))
        self.removeItem.setIcon(icon)
        self.removeItem.setMenuRole(QAction.MenuRole.NoRole)
        self.addItem = QAction(MainWindow)
        self.addItem.setObjectName(u"addItem")
        self.addItem.setCheckable(False)
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentNew))
        self.addItem.setIcon(icon1)
        self.addItem.setMenuRole(QAction.MenuRole.NoRole)
        self.verboseItem = QAction(MainWindow)
        self.verboseItem.setObjectName(u"verboseItem")
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentProperties))
        self.verboseItem.setIcon(icon2)
        self.verboseItem.setMenuRole(QAction.MenuRole.NoRole)
        self.closeVerboseItem = QAction(MainWindow)
        self.closeVerboseItem.setObjectName(u"closeVerboseItem")
        icon3 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditClear))
        self.closeVerboseItem.setIcon(icon3)
        self.closeVerboseItem.setMenuRole(QAction.MenuRole.NoRole)
        self.checkItem = QAction(MainWindow)
        self.checkItem.setObjectName(u"checkItem")
        self.checkItem.setCheckable(True)
        self.checkItem.setMenuRole(QAction.MenuRole.NoRole)
        self.upItem = QAction(MainWindow)
        self.upItem.setObjectName(u"upItem")
        icon4 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoUp))
        self.upItem.setIcon(icon4)
        self.upItem.setMenuRole(QAction.MenuRole.NoRole)
        self.downItem = QAction(MainWindow)
        self.downItem.setObjectName(u"downItem")
        icon5 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoDown))
        self.downItem.setIcon(icon5)
        self.downItem.setMenuRole(QAction.MenuRole.NoRole)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.buttonBox = QDialogButtonBox(self.centralwidget)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setLocale(QLocale(QLocale.Russian, QLocale.Russia))
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.NoButton)

        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 1)

        self.itemVerboseGroupBox = QGroupBox(self.centralwidget)
        self.itemVerboseGroupBox.setObjectName(u"itemVerboseGroupBox")
        self.verticalLayout = QVBoxLayout(self.itemVerboseGroupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(self.itemVerboseGroupBox)
        self.tabWidget.setObjectName(u"tabWidget")
        self.markdown = QWidget()
        self.markdown.setObjectName(u"markdown")
        self.verticalLayout_2 = QVBoxLayout(self.markdown)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.itemVerboseTextEdit = QPlainTextEdit(self.markdown)
        self.itemVerboseTextEdit.setObjectName(u"itemVerboseTextEdit")

        self.verticalLayout_2.addWidget(self.itemVerboseTextEdit)

        self.tabWidget.addTab(self.markdown, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.markdown), u"Markdown")
        self.text = QWidget()
        self.text.setObjectName(u"text")
        self.verticalLayout_3 = QVBoxLayout(self.text)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.itemVerboseTextView = QTextEdit(self.text)
        self.itemVerboseTextView.setObjectName(u"itemVerboseTextView")

        self.verticalLayout_3.addWidget(self.itemVerboseTextView)

        self.tabWidget.addTab(self.text, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.itemVerboseButtonBox = QDialogButtonBox(self.itemVerboseGroupBox)
        self.itemVerboseButtonBox.setObjectName(u"itemVerboseButtonBox")
        self.itemVerboseButtonBox.setLocale(QLocale(QLocale.Russian, QLocale.Russia))
        self.itemVerboseButtonBox.setStandardButtons(QDialogButtonBox.StandardButton.Apply|QDialogButtonBox.StandardButton.Close)

        self.verticalLayout.addWidget(self.itemVerboseButtonBox)


        self.gridLayout.addWidget(self.itemVerboseGroupBox, 2, 0, 1, 1)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.listView = QListView(self.centralwidget)
        self.listView.setObjectName(u"listView")

        self.gridLayout.addWidget(self.listView, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 36))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.itemVerboseButtonBox.rejected.connect(self.closeVerboseItem.trigger)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.removeItem.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c", None))
#if QT_CONFIG(tooltip)
        self.removeItem.setToolTip(QCoreApplication.translate("MainWindow", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u0442\u0435\u043a\u0443\u0449\u0438\u0439 \u044d\u043b\u0435\u043c\u0435\u043d\u0442", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.removeItem.setShortcut(QCoreApplication.translate("MainWindow", u"Del", None))
#endif // QT_CONFIG(shortcut)
        self.addItem.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c", None))
#if QT_CONFIG(tooltip)
        self.addItem.setToolTip(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u043d\u043e\u0432\u044b\u0439 \u044d\u043b\u0435\u043c\u0435\u043d\u0442", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.addItem.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+N", None))
#endif // QT_CONFIG(shortcut)
        self.verboseItem.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0434\u0440\u043e\u0431\u043d\u043e", None))
#if QT_CONFIG(tooltip)
        self.verboseItem.setToolTip(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u043b\u0443\u0447\u0438\u0442\u044c \u043f\u043e\u0434\u0440\u043e\u0431\u043d\u0443\u044e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0438\u044e \u043e\u0431 \u044d\u043b\u0435\u043c\u0435\u043d\u0442\u0435 \u0438 \u0438\u0437\u043c\u0435\u043d\u0438\u0442\u044c \u0441\u0432\u043e\u0439\u0441\u0442\u0432\u0430", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.verboseItem.setShortcut(QCoreApplication.translate("MainWindow", u"Return", None))
#endif // QT_CONFIG(shortcut)
        self.closeVerboseItem.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043a\u0440\u044b\u0442\u044c \u043f\u043e\u0434\u0440\u043e\u0431\u043d\u043e\u0441\u0442\u0438", None))
#if QT_CONFIG(tooltip)
        self.closeVerboseItem.setToolTip(QCoreApplication.translate("MainWindow", u"\u0421\u043a\u0440\u044b\u0442\u044c \u043f\u043e\u0434\u0440\u043e\u0431\u043d\u043e\u0441\u0442\u0438 \u043e\u0431 \u044d\u043b\u0435\u043c\u0435\u043d\u0442\u0435", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.closeVerboseItem.setShortcut(QCoreApplication.translate("MainWindow", u"Esc", None))
#endif // QT_CONFIG(shortcut)
        self.checkItem.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043c\u0435\u0442\u0438\u0442\u044c \u043a\u0430\u043a \u0432\u044b\u043f\u043e\u043b\u043d\u0435\u043d\u043d\u043e\u0435", None))
#if QT_CONFIG(tooltip)
        self.checkItem.setToolTip(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043c\u0435\u0442\u0438\u0442\u044c \u0434\u0430\u043d\u043d\u044b\u0439 \u044d\u043b\u0435\u043c\u0435\u043d\u0442 \u043a\u0430\u043a \u0432\u044b\u043f\u043e\u043b\u043d\u0435\u043d\u043d\u044b\u0439", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.checkItem.setShortcut(QCoreApplication.translate("MainWindow", u"Space", None))
#endif // QT_CONFIG(shortcut)
        self.upItem.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0434\u043d\u044f\u0442\u044c \u0432\u0432\u0435\u0440\u0445", None))
#if QT_CONFIG(tooltip)
        self.upItem.setToolTip(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0434\u043d\u044f\u0442\u044c \u044d\u043b\u0435\u043c\u0435\u043d\u0442 \u0432\u0432\u0435\u0440\u0445 \u043f\u043e \u043f\u0440\u0438\u043e\u0440\u0438\u0442\u0435\u0442\u0443", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.upItem.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+Num+Up", None))
#endif // QT_CONFIG(shortcut)
        self.downItem.setText(QCoreApplication.translate("MainWindow", u"\u041e\u043f\u0443\u0441\u0442\u0438\u0442\u044c \u0432\u043d\u0438\u0437", None))
#if QT_CONFIG(tooltip)
        self.downItem.setToolTip(QCoreApplication.translate("MainWindow", u"\u041e\u043f\u0443\u0441\u0442\u0438\u0442\u044c \u044d\u043b\u0435\u043c\u0435\u043d\u0442 \u0432\u043d\u0438\u0437", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.downItem.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+Num+Down", None))
#endif // QT_CONFIG(shortcut)
        self.itemVerboseGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"GroupBox", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.text), QCoreApplication.translate("MainWindow", u"\u0424\u043e\u0440\u043c\u0430\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u044b\u0439 \u0442\u0435\u043a\u0441\u0442", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u042d\u0442\u043e \u0441\u043f\u0438\u0441\u043e\u043a \u0434\u0435\u043b, \u043a\u043e\u0442\u043e\u0440\u044b\u0435 \u043d\u0443\u0436\u043d\u043e \u0432\u044b\u043f\u043e\u043b\u043d\u0438\u0442\u044c \u0432 \u0442\u0435\u0447\u0435\u043d\u0438\u0435 \u0434\u043d\u044f:", None))
    # retranslateUi

