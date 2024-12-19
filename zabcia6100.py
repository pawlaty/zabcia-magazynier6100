'''
Copyright by pawlaty@2024JeleniaGora
Wszelkie prawa zastrzeżone
All rigth reserved
'''

from PyQt5 import QtCore, QtGui, QtWidgets
import os
import sys
import datetime
import pandas
import pprint
from sqllite3 import SqlCon as coon
#from inator import InatorZliczator as Inator
#from raport import Raport

class Ui_TestQFileDialog(object):

    def __init__(self):
        print('hello zabcia')
        self.new_sql = coon()


    #Fill SelectBox POWIATY-Country i ... co?
    def fillSelectCountry(self,records=[]):
        self.choiceContry.setInsertPolicy(QtWidgets.QComboBox.InsertAlphabetically)
        list_select = list(set(records))

        for b in range(len(list_select)):
            self.choiceContry.addItem(list_select[b])        
        self.choiceContry.setEditable(True)

    def _open_file_dialog(self):        
        try:
            fileName = QtWidgets.QFileDialog.getOpenFileName(TestQFileDialog,"Select Excel file to import","", "Excel *.xls *.xlsx")
            self.dir = str(fileName[0])
            self.lineEdit.setText(self.dir)
            self.infoLabel.setText(self.dir)
            self.infoLabel.setText("Wybierz powiat do raportu.")
            
            self.data = pandas.read_excel(self.dir)
            self.fillSelectCountry(self.data['Podział 2'].values)

            #self.records_from_country = data[data['Podział 2']=="jeleniogórski"].values
            self.records_from_country = self.data[self.data['Podział 2']==self.choiceContry.currentText()].values

    		#nowa instancja INATORA- Zliczatora:-)))
            self.badania = Inator(self.records_from_country)
            
            self.choiceContry.activated.connect(self.changeSelect)
        except Exception as err:
            self.infoLabel.setText("Nie wybrano pliku")
            print(err)
    
    def makeRaport(self):
        self.records_from_country = self.data[self.data['Podział 2']==self.choiceContry.currentText()].values
        self.badania.ChangeBadania(self.records_from_country)
        self.badania.Refresh()
        self._raport = self.raport.MakeRaport(self.badania.CountPCRinPinkAreas(),self.badania.CountPCRinBlueAreas(),self.badania.CountElisa(),self.badania.CountBonesData(),self.choiceContry.currentText() + "ego")
        return self._raport

    def changeSelect(self):
        self.infoLabel.setText(self.makeRaport())

    def about(self):
        self.info_author.show()

    def setupUi(self, TestQFileDialog):
        TestQFileDialog.setObjectName("TestQFileDialog")
        #TestQFileDialog.resize(500, 500)
        TestQFileDialog.setFixedSize(500,420)
        
        #info author
        self.info_author = QtWidgets.QMessageBox(TestQFileDialog)
        
        self.info_author.setIcon(QtWidgets.QMessageBox.Information)
        self.info_author.setText("Copyright by Paweł Czajkowski\r\nJelenia GÓRA 2024\r\nWszystkie prawa zastrzeżone.\r\nKopiowanie, użytkowanie, udostępnianie\r\nbez zezwolenia zabronione.\r\nKontakt:pawlaty@gmail.com")
        self.info_author.setWindowTitle("o autorze...")
        self.info_author.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.info_author.hide()

        self.selecLabel = QtWidgets.QLabel(TestQFileDialog)
        self.selecLabel.setText('Wskaż plik exela')
        self.selecLabel.setGeometry(QtCore.QRect(345, 60, 800, 25))

        self.toolButtonOpenDialog = QtWidgets.QToolButton(TestQFileDialog)
        self.toolButtonOpenDialog.setGeometry(QtCore.QRect(440, 30, 50, 50))
        self.toolButtonOpenDialog.setObjectName("toolButtonOpenDialog")
        self.toolButtonOpenDialog.clicked.connect(self._open_file_dialog)
        
        #wazne: jakp argument musi TestQFileDialog
        #Label disabled file name to write 
        self.lineEdit = QtWidgets.QLineEdit(TestQFileDialog)
        self.lineEdit.setEnabled(False)
        self.lineEdit.setGeometry(QtCore.QRect(10, 30, 410, 35))
        self.lineEdit.setObjectName("lineEdit")

        # X--SelectBox Powiaty--------------------------------------
        self.choiceContry = QtWidgets.QComboBox(TestQFileDialog)
        self.choiceContry.setInsertPolicy(QtWidgets.QComboBox.InsertAlphabetically)
        self.choiceContry.setGeometry(QtCore.QRect(10, 90, 195, 25))
        self.choiceContry.setObjectName('choiceContry')
        self.choiceContry.setEditable(False)
        
        # Y--Label "Wybierz powiat"
        self.nameLabel = QtWidgets.QLabel(TestQFileDialog)
        self.nameLabel.setText('Wybierz powiat do raportu:')
        self.nameLabel.setGeometry(QtCore.QRect(225, 90, 150, 25))
        #-----------------------------------------------------------

        # A--Label "Nazwa pliku do exportu"-------------------------
        self.nameLabel = QtWidgets.QLabel(TestQFileDialog)
        self.nameLabel.setText('Nazwa pliku do exportu:')
        self.nameLabel.setGeometry(QtCore.QRect(10, 110, 250, 25))
        #self.nameLabel.setObjectName("nameLabel")

        # B--text input file_name
        self.line = QtWidgets.QLineEdit(TestQFileDialog)
        self.line.setGeometry(QtCore.QRect(10, 130, 195, 30))
        self.line.setObjectName("line")
        #self.line.move(80, 20)
        
        # C--butt export to txt
        self.button = QtWidgets.QPushButton(TestQFileDialog)
        self.button.setGeometry(225,130,100,30)
        self.button.setText('exportuj do txt')
        self.button.clicked.connect(self.export_data)
        #-----------------------------------------------------------
       # self.filename = self.line.text()
 
        #info Label
        self.infoLabel = QtWidgets.QLabel(TestQFileDialog)
        self.infoLabel.setWordWrap(True)
        self.infoLabel.setText(self.raport.GetOpis() + self.raport.GetInfo())
        self.infoLabel.setStyleSheet("font-size:14px;background:#14220a;color:#fff;padding:5px;""QListWidget QScrollBar")
        self.infoLabel.setGeometry(QtCore.QRect(10,180,480,180))
        self.infoLabel.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        #SCROLL
        self.scroll = QtWidgets.QScrollArea(TestQFileDialog)
        self.scroll.setWidget(self.infoLabel)
        self.scroll.setGeometry(QtCore.QRect(10,180,480,180))
        self.scroll.setWidgetResizable(True)
             
        #about butt
        self.about_button = QtWidgets.QPushButton(TestQFileDialog)
        self.about_button.setGeometry(10,380,100,25)
        self.about_button.setStyleSheet("color: #c9d1d9; background-color:#21262d;border-radius: 6px;border-width: 1px;border-style: solid;border-color: rgba(240, 246, 252, 0.1); text-decoration: none;padding: 0px 12px;")
        self.about_button.setText('o autorze')
        self.about_button.clicked.connect(self.about)

        #exit butt
        self.exit_button = QtWidgets.QPushButton(TestQFileDialog)
        self.exit_button.setGeometry(390,380,100,25)
        self.exit_button.setText('exit')
        self.exit_button.clicked.connect(self.quit)

        self.retranslateUi(TestQFileDialog)
        QtCore.QMetaObject.connectSlotsByName(TestQFileDialog)
        
#ustawienia okna
    def retranslateUi(self, TestQFileDialog):
        _translate = QtCore.QCoreApplication.translate
        TestQFileDialog.setWindowTitle(_translate("TestQFileDialog", "BadanioZliczatoInator"))
        TestQFileDialog.setWindowIcon(QtGui.QIcon("croupier2.ico"))
        self.toolButtonOpenDialog.setText(_translate("TestQFileDialog", "..."))
        

    def export_data(self):
        
        if not self.badania:
            self.infoLabel.setText('Nie można odczytać danych z pliku exela.\nPrawdopodobnie zły format arkusza lub nieporawne nazwy kolumn.\nDane pobrane z arkusza muszą zgadzać się z opisem\n\r' + self.raport.GetOpis())
            return
        else:
            self.infoLabel.setText('mn.\nDane pobrane z arkusza muszą zgadzać się z opisem\n\r' + self.raport.GetOpis())
            
            try:
                path = os.getcwd() + "/raporty"
                isExist = os.path.exists(path)
                if not isExist:
                   os.makedirs(path)
                				
                _date = datetime.datetime.now().strftime('%Y-%m-%d')
                f_name = "raporty/"+str(self.line.text())+"-"+self.choiceContry.currentText()+"-"+str(_date)+".txt"
                self.infoLabel.setText(f_name)
                _data = "Raport z dnia: " + str(_date)
                self._raport = self.makeRaport()
                #self._raport = raport.MakeRaport(self.badania.CountPCRinPinkAreas(),self.badania.CountPCRinBlueAreas(),self.badania.CountElisa(),self.badania.CountBonesData(),self.choiceContry.currentText() + "ego")
                #save to txt
                with open(f_name,'w') as fw:
                   fw.write(self._raport)
                   self.infoLabel.setText("Dane wyeksportowano do pliku: " + str(f_name) +"\n" + self._raport)


            except Exception as e:
                print(e)
                self.infoLabel.setText("Ups. coś poszło nie tak.")

    def quit(self):
        print("exit")
        sys.exit()


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    TestQFileDialog = QtWidgets.QDialog()
    ui = Ui_TestQFileDialog()
    ui.setupUi(TestQFileDialog)
    TestQFileDialog.show()
    sys.exit(app.exec_())