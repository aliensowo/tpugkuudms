from gui.E_winner_page import Ui_MainWindow as EPage
from PyQt5 import QtWidgets
import docx
import os


class ELogicPage(QtWidgets.QMainWindow):

    def __init__(self, winner: dict, compare_id: int, username: str):
        super(ELogicPage, self).__init__()
        self.ui = EPage()
        self.ui.setupUi(self)
        self.winner = winner
        self.compare_id = compare_id
        self.username = username
        # button logic
        self.ui.buttonBox.accepted.connect(self.button_logic)
        self.ui.buttonBox.rejected.connect(self.close)

        # label logic
        self.ui.label_2.setText(self.winner["contractor_name"])

    def button_logic(self):
        doc = docx.Document('raport.docx')
        par_index = 0
        for paragraph in doc.paragraphs:
            style = paragraph.style
            if "{contractor_name}" in paragraph.text:
                paragraph.text = paragraph.text.format(
                    contractor_name=self.winner["contractor_name"].replace("\n", "").strip())
                doc.paragraphs[par_index].style = style
            par_index += 1
        doc.tables[0].columns[2].cells[1].text = self.winner["work_cost"].replace(
            "\n", "").strip()
        doc.tables[0].columns[2].cells[2].text = self.winner["availability_of_technology"].replace(
            "\n", "").strip()
        doc.tables[0].columns[2].cells[3].text = self.winner["tech_equipment"].replace(
            "\n", "").strip()
        doc.tables[0].columns[2].cells[4].text = self.winner["availability_of_production_facilities"].replace(
            "\n", "").strip()
        doc.tables[0].columns[2].cells[5].text = self.winner["qualified_human_resources_personnel"].replace(
            "\n", "").strip()
        doc.save(
            os.path.join(os.path.join(
                os.getenv("USERPROFILE")),
                "Desktop",
                f"report_{self.username}_{self.compare_id}.docx"
            )
        )
        self.close()
