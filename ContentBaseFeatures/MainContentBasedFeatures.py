from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
import sys
import csv
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
import nltk
nltk.download('averaged_perceptron_tagger')
from nltk import *
from nltk import word_tokenize, pos_tag

def obter_string_salva():
    with open("caminho_pasta.txt", "r") as arquivo:
        pasta_salva = arquivo.read()
        return pasta_salva

pasta_salva = obter_string_salva()

# buscar o caminho da pasta
script_dir = os.path.dirname(os.path.abspath(__file__))
# receber o caminho do projeto
project_dir = os.path.dirname(script_dir)


class ContentBasedFeatures(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Content-Based Features")
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
        standardPosTagger = QPushButton("StandardPosTagger", self)
        featuresCBF = QPushButton("CBF Features", self)
        back = QPushButton("Back", self)

        # setting geometry of button
        standardPosTagger.setGeometry(280, 50, 300, 50)
        featuresCBF.setGeometry(280, 140, 300, 50)
        back.setGeometry(280, 230, 300, 50)

        back.clicked.connect(self.back)
        featuresCBF.clicked.connect(self.featuresCBF)
        standardPosTagger.clicked.connect(self.standardPosTagger)

    def centerWindow(self):
        # Get the screen's geometry and center the window on it
        screenGeometry = QDesktopWidget().screenGeometry()
        x = (screenGeometry.width() - self.width()) // 2
        y = (screenGeometry.height() - self.height()) // 2
        self.move(x, y)

    def standardPosTagger(self):
        try:
            csv_filename = os.path.join(project_dir, "FeatureExtraction_Python-main", "../Output", "STP.csv") # nome do arquivo csv
            base_dir = pasta_salva + "/" # pasta onde estão os arquivos
            files_in_dir = os.listdir(base_dir) # lista de arquivos
            pos_counts = defaultdict(list) # dicionário
            header = ['Ficheiro', 'VB', 'CD', 'NN', 'RB', 'VBD', 'MD', 'NNP', 'VBZ', 'JJ', 'NNS', 'VBP', 'POS', 'VBG', 'RP',
                      'BR', 'JJR', 'IN', 'VBN', 'CC', 'TO', 'DT'] # cabeçalho do arquivo csv

            for file in files_in_dir:
                filepath = nltk.data.find(os.path.join(base_dir, file))  # Use os.path.join to construct file paths
                textfile = open(filepath, 'r').read() # abrir o arquivo
                words = word_tokenize(textfile) # tokenizar o arquivo
                pos_tags = pos_tag(words) # tagger
                counts = Counter(tag for word, tag in pos_tags) # contar as tags

                for tag, count in counts.items(): # para cada tag e contagem
                    pos_counts[tag].append(count) # adicionar as tags no dicionário

            # Fill in missing tags with 0
            for tag in header[1:]: # para cada tag
                while len(pos_counts[tag]) < len(files_in_dir): # enquanto o tamanho do dicionário for menor que o tamanho da lista de arquivos
                    pos_counts[tag].append(0) # adicionar 0

            # Write the results to CSV
            with open(csv_filename, 'w', newline='') as csvfile: # abrir o arquivo csv
                writer = csv.writer(csvfile) # escrever no arquivo
                writer.writerow(header)  # escrever o cabeçalho
                for i, file in enumerate(files_in_dir): # para cada arquivo
                    row_values = [file] + [pos_counts[tag][i] for tag in header[1:]] # adicionar o nome do arquivo e as tags
                    writer.writerow(row_values) # escrever no arquivo
            QMessageBox.information(self, "Success", "STP.csv successfully created in the Output folder.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")



    def featuresCBF(self):
        from ContentBaseFeatures.MainOpenCBF import OpenCBF
        self.w = OpenCBF()
        self.w.show()
        self.close()


    def back(self):
        from MainWindow import MainWindow
        self.w = MainWindow()
        self.w.show()
        self.close()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ContentBasedFeatures()
    window.show()
    sys.exit(app.exec_())