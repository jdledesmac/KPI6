import pandas as pd
from PyQt5 import uic, sip
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
import TableModelWidget


class Window(QMainWindow):
    '''Window is the main class to show de window aplication and all its components'''
    def __init__(self):
        super().__init__()
        uic.loadUi("interface.ui", self)

        #variables
        self.files=[]
        self.data_umts=[]
        self.unuse_colums=['PLMN name', 'MRBTS/SBTS name', 'LNBTS type', 'RNC name', 'WBTS ID', 'WCEL ID']

        self.loadButton.clicked.connect(self.get_file)
        self.showDataButton.clicked.connect(self.show_data_table)

    
    def get_file(self):
        """ This function will get the address of the file location"""
        file_type=''
        try:
            file_name = QFileDialog.getOpenFileName(filter = "xlsx/csv (*.xlsx *.csv)")[0]
            if file_name not in self.files:
                self.files.append(file_name)
                file_type=file_name[-4:]
                if file_type=='xlsx':
                    self.read_xlsx(file_name)
            #elif file_type=='.csv':
            #TODO
            #self.read_csv_data()
            else:
                self.textBrowser.append("File ommited, previously loaded")
        except AssertionError:
            self.textBrowser.append("No file loaded")    
    
    def read_xlsx(self, file):
        """This function will read the data using pandas"""
        try:
            excel_data = pd.read_excel(file, index_col=0)
            if (pd.isnull(excel_data.index[0])):
                excel_data.drop(excel_data.index[0], inplace=True)
        except ValueError as _e:
            return _e
        
        # Delete unuseful columns
        for column in self.unuse_colums:
            if column in excel_data.columns:
                excel_data.drop([column], axis=1, inplace=True)
        excel_data = excel_data.infer_objects()
        if 'WCEL name' in excel_data.columns:
            self.data_umts.append(excel_data)
    
    def show_data_table(self):
        model=TableModelWidget.TableModel(self.data_umts[0])
        self.tableView.setModel(model)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.resizeColumnsToContents()
        self.tableView.resizeRowsToContents()
        
        


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = Window()
    ui.show()
    sys.exit(app.exec_())