from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
import sys
import liwc
import os
sys.path.insert(0, os.path.abspath(".."))
parse, category_names = liwc.load_token_parser('LIWC2007_English100131.dic')

pasta_selecionada = None

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LMER-FE - Main Window")
        # Create a QGridLayout instance
        layout = QGridLayout()
        window = QWidget()
        self.setWindowIcon(QIcon('Music.ico'))

        self.UiComponents()

        self.show()

        # Set the layout on the application's window

        self.setLayout(layout)

    def UiComponents(self):
        self.resize(850, 350)  # Set the initial size of the window
        self.centerWindow()
        # creating a push button
        featSemanticas = QPushButton("Features Semantics", self)
        contBasedFeatures = QPushButton("Content-Based Features", self)
        structBased = QPushButton("Structural Based Features", self)
        featureEst = QPushButton("Features Stylistics", self)
        allFeatures = QPushButton("All Features", self)
        EscolherPasta = QPushButton("Choose a folder", self)
        label = QLabel("Before starting the Project, choose the folder", self)




        # setting geometry of button
        featSemanticas.setGeometry(80, 30, 300, 50)
        contBasedFeatures.setGeometry(80, 110, 300, 50)
        allFeatures.setGeometry(80, 190, 300, 50)
        featureEst.setGeometry(460, 30, 300, 50)
        structBased.setGeometry(460, 110, 300, 50)
        EscolherPasta.setGeometry(460, 190, 300, 50)
        label.move(270, 300)

        # adding action to a button
        featSemanticas.clicked.connect(self.openFeatSemanticas)
        contBasedFeatures.clicked.connect(self.openContBasedFeatures)
        structBased.clicked.connect(self.openStructBased)
        featureEst.clicked.connect(self.openFeatureEst)
        allFeatures.clicked.connect(self.allFeatures)
        EscolherPasta.clicked.connect(self.escolher_pasta)

        # action method

    def centerWindow(self):
        # Get the screen's geometry and center the window on it
        screenGeometry = QDesktopWidget().screenGeometry()
        x = (screenGeometry.width() - self.width()) // 2
        y = (screenGeometry.height() - self.height()) // 2
        self.move(x, y)
    def escolher_pasta(self):
        pasta_selecionada = QFileDialog.getExistingDirectory(None, "Select the folder")
        if pasta_selecionada:
            self.salvar_string(pasta_selecionada)

    def salvar_string(self, string):
        with open("caminho_pasta.txt", "w") as arquivo:
            arquivo.write(string)


    def allFeatures(self):
        try:
            from StructuralBasedFeatures.MainStructuralBasedFeatures import extract_chorus_from_song
            return extract_chorus_from_song
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")


    def openFeatSemanticas(self):
        from SemanticsFeatures.MainFeaturesSemanticas import FeaturesSemanticas
        self.w = FeaturesSemanticas()
        self.w.show()
        self.close()


    def openContBasedFeatures(self):
        from ContentBaseFeatures.MainContentBasedFeatures import ContentBasedFeatures
        self.w = ContentBasedFeatures()
        self.w.show()
        self.close()

    def openStructBased(self):
        from StructuralBasedFeatures.MainStructuralBasedFeatures import StructuralBasedFeatures
        self.w = StructuralBasedFeatures()
        self.w.show()
        self.close()

    def openFeatureEst(self):
        from StylisticFeatures.MainFeaturesEstilisticas import FeaturesEstatisticas
        self.w = FeaturesEstatisticas()
        self.w.show()
        self.close()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())