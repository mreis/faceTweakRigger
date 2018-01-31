
#############################
#############################
#
#	-	FaceTwkRig - v2
#	by:	Mendel Reis
#	at:	mendelreis@gmail.com 
#
#############################

from PySide2.QtWidgets import *
from PySide2.QtGui import  *
from PySide2.QtCore import *
from pymel.core import * 
from functools import partial
import maya.OpenMayaUI as mui
import shiboken2
#import cPickle
#import time
import os

# Get Maya Window
def getMayaWindow():
	mayaWindowPointer = mui.MQtUtil.mainWindow()
	return shiboken2.wrapInstance(long(mayaWindowPointer), QWidget)

class mainUI():

	def __init__(self):
		# Ui window
		if window("faceTweakRiggerUi", query = True, exists = True):
			deleteUI("faceTweakRiggerUi", wnd = True)

		# Main Ui
		self.ui = QMainWindow(getMayaWindow())
		self.ui.setFixedSize(500, 500)
		#self.ui.setMinimumWidth(500)
		#self.ui.setMaximumWidth(500)
		self.ui.setObjectName('faceTweakRiggerUi')
		self.ui.setWindowTitle('Face Tweak Rigger Ui - v 2.0') 
		self.ui.setWindowFlags(self.ui.windowFlags() & ~Qt.WindowMinMaxButtonsHint)


		#model 
		self.grpModel = Model()
		self.vtxModel = vtxModel([])

		# Central Widget & Layout
		centralWidget = QWidget()
		self.centralLayout = QVBoxLayout()
		centralWidget.setLayout(self.centralLayout)
		self.ui.setCentralWidget(centralWidget)

		# Menu Bar
		self.menuBar = MenuBar()
		self.centralLayout.addWidget(self.menuBar)

		# first group: select geomtry and head controller
		self.selectionGrp = QGroupBox()
		self.selectionGrp.setMaximumHeight(100)
		self.selectionGrp.setTitle('Select model geometry and head controller. ') 
		self.selectionGrpLayout = QHBoxLayout()
		self.selectionGrp.setLayout(self.selectionGrpLayout)
		self.centralLayout.addWidget(self.selectionGrp)
		self.selectionGrpWidget = selectionGrp()
		self.selectionGrpLayout.addWidget(self.selectionGrpWidget)

		# separator 1
		separatorLine = QFrame()
		separatorLine.setFrameShape(QFrame.HLine)
		separatorLine.setFrameShadow(QFrame.Sunken)	
		self.centralLayout.addWidget(separatorLine)	

		# Table Views Group
		self.tvGrp = QGroupBox('Face tweak groups and vertices.')
		tablesLayout = QVBoxLayout()
		self.tvGrp.setLayout(tablesLayout)
		self.centralLayout.addWidget(self.tvGrp)

		# Table Views
		tableViewsWidgets = QWidget()
		tvwLayout = QHBoxLayout()
		tvwLayout.setContentsMargins(0,0,0,0)
		tablesLayout.addWidget(tableViewsWidgets)
		tableViewsWidgets.setLayout(tvwLayout)
		
		#left side
		leftTableWidget = QWidget()
		leftTableWidget.setMaximumHeight(250)
		leftLayout = QVBoxLayout()
		leftLayout.setContentsMargins(0,0,0,0)
		leftTableWidget.setLayout(leftLayout)
		#right Side
		rightTableWidget = QWidget()
		rightTableWidget.setMaximumHeight(250)
		rightLayout = QVBoxLayout()
		rightLayout.setContentsMargins(0,0,0,0)
		rightTableWidget.setLayout(rightLayout)
		#addto layout
		tvwLayout.addWidget(leftTableWidget)
		tvwLayout.addWidget(rightTableWidget)

		# left side table view: Groups
		self.grpTable = Table()
		self.newGrpInut = QLineEdit()
		self.newGrpInut.setMinimumHeight(25)
		grpBtnsWidgets = QWidget()
		leftBtnLayout = QHBoxLayout()
		leftBtnLayout.setContentsMargins(0,0,0,0)
		grpBtnsWidgets.setLayout(leftBtnLayout)
		self.newGrpBtn = NewGrpBtn(self.newGrpInut, self.grpModel)
		self.delGrpBtn = DelGrpBtn(self.grpTable,self.grpModel)
		leftBtnLayout.addWidget(self.newGrpBtn)
		leftBtnLayout.addWidget(self.delGrpBtn)
		leftLayout.addWidget(self.grpTable)
		leftLayout.addWidget(self.newGrpInut)
		leftLayout.addWidget(grpBtnsWidgets)

		# right side table view: Vertices
		self.vtxTable = listView()
		self.vtxTable.setModel(self.vtxModel)
		vtxBtnsWidgets = QWidget()
		rightBtnLayout = QHBoxLayout()
		rightBtnLayout.setContentsMargins(0,0,0,0)
		vtxBtnsWidgets.setLayout(rightBtnLayout)
		self.addVtxBtn = getVtxBtn()
		self.delVtxBtn = QPushButton("Del Vertices")
		self.queryVtxBtn = QPushButton("Query")
		rightBtnLayout.addWidget(self.addVtxBtn)
		rightBtnLayout.addWidget(self.delVtxBtn)
		rightBtnLayout.addWidget(self.queryVtxBtn)

		rightLayout.addWidget(self.vtxTable)
		rightLayout.addWidget(vtxBtnsWidgets)

		# separator 2
		separatorLine = QFrame()
		separatorLine.setFrameShape(QFrame.HLine)
		separatorLine.setFrameShadow(QFrame.Sunken)	
		self.centralLayout.addWidget(separatorLine)

		# create facial rig area and adjust controls

		lastWidget = QWidget()
		lastLayout = QHBoxLayout()
		lastLayout.setContentsMargins(0,0,0,0)
		lastWidget.setLayout(lastLayout)

		self.rigBtn = QPushButton("Create face tweak rig")
		self.rigBtn.setMinimumHeight(35)
		self.rigBtn.setMinimumWidth(350)

		self.adjBtn = QPushButton("Adjust controls")
		self.adjBtn.setMinimumHeight(35)

		lastLayout.addWidget(self.rigBtn)
		lastLayout.addWidget(self.adjBtn)
		self.centralLayout.addWidget(lastWidget)

		self.grpTable.setModel(self.grpModel)
		self.selection = self.grpTable.selectionModel()
		self.selection.selectionChanged.connect(partial(self.handleSelectionChanged))
		self.grpTable.resizeColumnsToContents()
		self.header = self.grpTable.horizontalHeader()
		self.header.setSectionResizeMode(1, QHeaderView.Stretch)


		# show ui
		self.ui.show()

	def handleSelectionChanged(self, selected, deselected):

		for index in self.grpTable.selectionModel().selectedRows():
			print 'Row %d is selected' % index.row()

			vtx = self.grpModel.groups[index.row()][3]

			self.vtxModel = vtxModel(vtx)
			self.vtxTable.setModel(self.vtxModel)




class MenuBar(QMenuBar):

	def __init__(self ):
		super(MenuBar, self).__init__() 

		self.help = QMenu('Help')
		self.addMenu(self.help)

		self.info = QMenu('Info')
		self.addMenu(self.info)

class selectionGrp(QWidget):

	def __init__(self):
		super(selectionGrp, self).__init__() 

		layout = QVBoxLayout()
		layout.setContentsMargins(0,0,0,0)
		self.setLayout(layout)

		modelSelection = QWidget()
		modelLayout = QHBoxLayout()
		modelLayout.setContentsMargins(0,0,0,0)
		modelSelection.setLayout(modelLayout)
		getModelBtn = QPushButton("Get model")
		getModelBtn.setFixedSize(100, 25)
		getModelBtn.clicked.connect(partial(self.getModel))
		self.modelDisplay = QLineEdit()
		self.modelDisplay.setEnabled(False)
		self.modelDisplay.setMinimumHeight(25)
		modelLayout.addWidget(self.modelDisplay)
		modelLayout.addWidget(getModelBtn)

		headSelection = QWidget()
		headLayout = QHBoxLayout()
		headLayout.setContentsMargins(0,0,0,0)
		headSelection.setLayout(headLayout)
		getHeadBtn = QPushButton("Get Head Ctrl")
		getHeadBtn.setFixedSize(100, 25)
		getHeadBtn.clicked.connect(partial(self.getCtrl))
		self.headDisplay = QLineEdit()
		self.headDisplay.setEnabled(False)
		self.headDisplay.setMinimumHeight(25)
		headLayout.addWidget(self.headDisplay)
		headLayout.addWidget(getHeadBtn)

		layout.addWidget(modelSelection)
		layout.addWidget(headSelection)


	def getModel(self, *args):

		obj = selected()

		if len(obj) > 1 or len(obj) == 0:
			warning("Must have ONE single object selected")
			return False
		else:
			self.modelDisplay.setText(obj[0].name())

	def getCtrl(self, *args):

		obj = selected()

		if len(obj) > 1 or len(obj) == 0:
			warning("Must have ONE single object selected")
			return False
		else:
			self.headDisplay.setText(obj[0].name())

class NewGrpBtn(QPushButton):

	def __init__(self, input, model):
		super(NewGrpBtn, self).__init__()

		self.setText('Create group')
		self.model = model
		self.input = input
		self.clicked.connect(partial(self.getGrpName))
		

	def getGrpName(self, *args):

		t = self.input.text()
		values = ["X", t, 'not', []]

		self.model.insertRows(0, 1, values = values)

class DelGrpBtn(QPushButton):
	
	def __init__(self, tableView, model):
		super(DelGrpBtn, self).__init__()

		self.setText('Delete group')
		self.tableView = tableView
		self.model = model
		self.clicked.connect(partial(self.delGrpName))
		
	def delGrpName(self, *args):

		index_list = [] 

		for model_index in self.tableView.selectionModel().selectedRows():       
		    index = QPersistentModelIndex(model_index)         
		    index_list.append(index)     

		for index in index_list:                                    
			self.model.removeRow(index.row()) 

class getVtxBtn(QPushButton):
	def __init__(self):
		super(getVtxBtn, self).__init__()

		self.setText("Add vertices")
		self.clicked.connect(partial(self.getVtxs))

	def getVtxs(self, *args):

		vtxs = selected()
		vtxs = filterExpand(vtxs, selectionMask = 31)
		print ''

		for vtx in vtxs:
			print vtx





class Table(QTableView):

	def __init__(self,  *args, **kwargs):
		QTableView.__init__(self, *args, **kwargs)

		self.setSortingEnabled(True)
		hHeader = self.horizontalHeader()
		hHeader.setSectionResizeMode(QHeaderView.Fixed);
		self.setSelectionBehavior(QAbstractItemView.SelectRows)
		vHeader = self.verticalHeader()
		vHeader.hide()

class Model(QAbstractTableModel):

	def __init__(self, parent = None):
		QAbstractTableModel.__init__(self, parent)

		#data
		self.groups = [['X','test','done',[1,2,3,4,5,6,7]],['X','test2','done',['A', 'B','C']]]
		#header
		self.header_labels = ['', 'Group', 'Status']

	def rowCount(self, parent):
		return len(self.groups)

	def columnCount(self, parent):
		return 3

	def flags(self, index):

		if index.column() < 2:
			fl = Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable
		else:
			fl = Qt.ItemIsSelectable | Qt.ItemIsEnabled

		return fl

	
	def headerData(self, section, orientation, role):
		if role == Qt.DisplayRole and orientation == Qt.Horizontal:
			return self.header_labels[section]

	def removeRow(self, row, parent = QModelIndex()):
		self.beginRemoveRows(parent, row, row)
		self.groups.remove(self.groups[row])
		self.endRemoveRows()

	def insertRows(self, position, row, values = [] , parent = QModelIndex()):

		lastposition = self.rowCount(0)
		self.beginInsertRows(parent, lastposition, lastposition)
		self.groups.insert(lastposition, values)
		self.endInsertRows()
	
	def setData(self, index, value, role = Qt.EditRole):

		setIt = False
		value = value
		row = index.row()
		column = index.column()

		if role == Qt.EditRole:
			setIt = True

		if setIt:
			self.groups[row][column] = value
			self.dataChanged.emit(row, column)

		print self.groups
		return False

	def data(self, index, role):
		if not index.isValid():
			return 

		row = index.row()
		column = index.column()

		if role == Qt.DisplayRole:
			value = self.groups[row][column]
			return value

		elif role == Qt.TextAlignmentRole:
			return Qt.AlignCenter;

		elif role == Qt.EditRole: 
			index = index 
			return index.data()     	

class listView(QListView):
	def __init__(self, headers = [], parent = None):
		QListView.__init__(self, parent)


class vtxModel(QAbstractListModel):

	def __init__(self, vtxs, parent = None):
		QAbstractListModel.__init__(self, parent)
      
      	#data
		self.vtxs = vtxs

        #header
		self.header_labels = ['Vertices']

	def rowCount(self, parent):
		return len(self.vtxs)


	def flags(self, index):

		fl = Qt.ItemIsSelectable | Qt.ItemIsEnabled
		return fl

	def headerData(self, section, orientation, role):
		if role == Qt.DisplayRole and orientation == Qt.Horizontal:
			return self.header_labels[section]

	def data(self, index, role):
		if not index.isValid():
			return 

		row = index.row()
		column = index.column()

		if role == Qt.DisplayRole:
			value = self.vtxs[row]
			return value

		elif role == Qt.TextAlignmentRole:
			return Qt.AlignLeft;

	def insertRow(row, count, value = [], parent = QModelIndex()):
		lastposition = self.rowCount(0)
		self.beginInsertRows(parent, lastposition, lastposition + count)
		self.vtx.insert(lastposition, values)
		self.endInsertRows()

a = mainUI()