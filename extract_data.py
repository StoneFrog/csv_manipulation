# -*- coding: utf-8 -*-

import sys
from rera_5 import ImportFile, DataConversion, ListDivision, Main
from PyQt4 import QtGui, QtCore

class Example(QtGui.QWidget):

	def __init__(self):
		super(Example, self).__init__()
		self.import_file = ImportFile()
		self.data_conversion = DataConversion()
		self.list_division = ListDivision()
		self.main = Main('/home')

		self.initUI()


	def initUI(self):

		import_file = ImportFile()


		#part below responsible for drawing listbox and selecting be default
		#some checkboxes
		self.listbox = QtGui.QListWidget(self)

		name_dict = import_file.export_dict()
		name_list_sorted = sorted(list(name_dict.keys()))
		checklist = ['id', 'time', 'cellnumber', 'voc', 'isc', 'fillfactor', 'eta']

		for name in name_list_sorted:
			name_item = QtGui.QListWidgetItem(name)
			if name in checklist:
				name_item.setCheckState(QtCore.Qt.Checked)
			else:
				name_item.setCheckState(QtCore.Qt.Unchecked)
			self.listbox.addItem(name_item)


		#part below creates rest of components (buttons, lines, labels)and connect them
		#to choose file/directory to save file
		lbl = QtGui.QLabel('Choose file', self)

		lbl2 = QtGui.QLabel('Choose directory to save the file', self)

		self.btn = QtGui.QPushButton('Browse', self)
		self.btn.clicked.connect(self.showDialog)

		self.btn2 = QtGui.QPushButton('Browse', self)
		self.btn2.clicked.connect(self.showDialog)

		self.btn3 = QtGui.QPushButton('Start extraction', self)
		self.btn3.clicked.connect(self.extract_data)

		self.le = QtGui.QLineEdit('/home', self)
		self.le2 = QtGui.QLineEdit('/home', self)


		#Layout
		hbox = QtGui.QHBoxLayout()
		hbox.addWidget(self.btn)
		hbox.addWidget(self.le)

		vbox = QtGui.QVBoxLayout()
		vbox.addWidget(lbl)
		vbox.addLayout(hbox)


		hbox2 = QtGui.QHBoxLayout()
		hbox2.addWidget(self.btn2)
		hbox2.addWidget(self.le2)

		vbox2 = QtGui.QVBoxLayout()
		vbox2.addWidget(lbl2)
		vbox2.addLayout(hbox2)

		vbox3 = QtGui.QVBoxLayout()
		vbox3.addLayout(vbox)
		vbox3.addLayout(vbox2)
		vbox3.addWidget(self.btn3)
		vbox3.addStretch(1)

		hbox3 = QtGui.QHBoxLayout()
		hbox3.addWidget(self.listbox)
		hbox3.addLayout(vbox3)

		self.setLayout(hbox3) 

		#main window
		self.setGeometry(30, 30, 700, 1000)
		self.setWindowTitle('test')
		self.show()

	def showDialog(self): #choose file directory

		if self.sender() == self.btn:
			fname = QtGui.QFileDialog.getOpenFileName(self, 'Choose file')
			self.le.setText(str(fname))
		elif self.sender() == self.btn2:
			fname = QtGui.QFileDialog.getExistingDirectory(self, 'Choose directory')
			self.le2.setText(str(fname))

	def extract_data(self):
		import_file = ImportFile()

		name_dict = import_file.export_dict()
		extraction_list = ['id', 'time', 'cellnumber']
		chose_column = []

		for number in range(0,len(self.listbox)):
			element = QtGui.QListWidgetItem(self.listbox.item(number))
			if element.checkState() == 2:
				if (self.listbox.item(number).text() in extraction_list) != True:
					extraction_list.append(str(self.listbox.item(number).text()))

		runner = Main(str(self.le.text()))
		runner.save_data(extraction_list, str(self.le2.text()))



def main():

	app = QtGui.QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
