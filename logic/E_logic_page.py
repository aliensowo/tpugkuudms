from gui.E_winner_page import Ui_MainWindow as EPage
from PyQt5 import QtWidgets
import docx
import os


class ELogicPage(QtWidgets.QMainWindow):

    def __init__(self, winner: dict):
        super(ELogicPage, self).__init__()
        self.ui = EPage()
        self.ui.setupUi(self)
        self.winner = winner
        # button logic
        self.ui.buttonBox.accepted.connect(self.button_logic)
        self.ui.buttonBox.rejected.connect(self.close)

        # label logic
        self.ui.label_2.setText(self.winner["contractor_name"])

    def button_logic(self):
        try:
            doc = docx.Document('raport.docx')
            par_index = 0
            for paragraph in doc.paragraphs:
                style = paragraph.style
                if "{contractor_name}" in paragraph.text:
                    paragraph.text = paragraph.text.format(ctc_name=self.winner["contractor_name"])
                    doc.paragraphs[par_index].style = style
                par_index += 1
            doc.tables[0].columns[2].cells[2].text = self.winner["work_cost"]
            doc.tables[0].columns[2].cells[2].text = self.winner["availability_of_technology"]
            doc.tables[0].columns[2].cells[2].text = self.winner["tech_equipment"]
            doc.tables[0].columns[2].cells[2].text = self.winner["availability_of_production_facilities"]
            doc.tables[0].columns[2].cells[2].text = self.winner["qualified_human_resources_personnel"]
            doc.save("result.docx")
        except Exception as e:
            print(e)
