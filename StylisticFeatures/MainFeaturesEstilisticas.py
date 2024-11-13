import csv
import sys
import os
from os import listdir
import nltk
import re

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

# buscar o caminho da pasta
script_dir = os.path.dirname(os.path.abspath(__file__))
# receber o caminho do projeto
project_dir = os.path.dirname(script_dir)
slang_File = os.path.join(project_dir, "src", "auxiliarFiles", "slang.txt")

def obter_string_salva():
    with open("caminho_pasta.txt", "r") as arquivo:
        pasta_salva = arquivo.read()
        return pasta_salva

pasta_salva = obter_string_salva()
base_dir = pasta_salva + "/"

class FeaturesEstatisticas(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Features Stylistics")
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
        acl = QPushButton("ACL Features", self)
        featuresSlang = QPushButton("Features Slang", self)
        featCapitalLetters = QPushButton("Features CapitalLetters", self)
        back = QPushButton("Back", self)

        # setting geometry of button
        acl.setGeometry(80, 80, 300, 50)
        featuresSlang.setGeometry(80, 160, 300, 50)
        featCapitalLetters.setGeometry(460, 80, 300, 50)
        back.setGeometry(460, 160, 300, 50)

        back.clicked.connect(self.back)
        acl.clicked.connect(self.ACL)
        featuresSlang.clicked.connect(self.slangWords)
        featCapitalLetters.clicked.connect(self.capitalLetters)

    def centerWindow(self):
        # Get the screen's geometry and center the window on it
        screenGeometry = QDesktopWidget().screenGeometry()
        x = (screenGeometry.width() - self.width()) // 2
        y = (screenGeometry.height() - self.height()) // 2
        self.move(x, y)

    def back(self):
        from MainWindow import MainWindow
        self.w = MainWindow()
        self.w.show()
        self.close()



    def capitalLetters(self):
        try:
            csv_filename = os.path.join(project_dir, "Output", "CapitalLetters.csv") #criar o ficheiro csv
            files_in_dir = listdir(base_dir) #listar todos os ficheiros na pasta
            capital_Letteres_counts = {} #criar um dicionario para guardar o nome do ficheiro e o numero de capital letters
            for file in files_in_dir: #percorrer todos os ficheiros
                filepath = nltk.data.find(base_dir + file) #encontrar o caminho do ficheiro
                textfile = open(filepath, 'r').read() #abrir o ficheiro
                count = sum(1 for c in textfile if c.isupper()) #contar o numero de capital letters
                capital_Letteres_counts[file] = count #guardar o nome do ficheiro e o numero de capital letters
                with open(csv_filename, 'w') as f: #guardar no ficheiro csv
                    f.write("%s,%s \n" % ("File", "Capital Letters")) #escrever o header do ficheiro csv
                    for key in capital_Letteres_counts.keys(): #percorrer o dicionario
                        f.write("%s,%s\n" % (key, capital_Letteres_counts[key])) #escrever no ficheiro csv
                print("File: ", file, " has ", count, " capital letters") #print o numero de capital letters
            QMessageBox.information(self, "Success", "CapitalLetters.csv successfully created in the Output folder.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def ACL(self):
        try:
            csv_filename = os.path.join(project_dir, "Output", "ACL.csv") # criar o ficheiro csv
            files_in_dir = listdir(base_dir) # listar todos os ficheiros na pasta
            ACL_counts = {} # criar um dicionario para guardar o nome do ficheiro e o numero de capital letters
            words_acl = [] # criar uma lista para guardar as palavras em maiusculas

            for file in files_in_dir: # percorrer todos os ficheiros
                filepath = nltk.data.find(base_dir + file) # encontrar o caminho do ficheiro
                textfile = open(filepath, 'r').read() # abrir o ficheiro
                words = re.findall(r'\b[A-Z]+\b', textfile)
                words_acl.append(words) # guardar as palavras em maiusculas
                count = len(words) # contar o numero de palavras em maiusculas
                ACL_counts[file] = count # guardar o nome do ficheiro e o numero de palavras em maiusculas
                with open(csv_filename, 'w') as f:
                    f.write("%s,%s \n" % ("File", "All Capital Letters")) # escrever o header do ficheiro csv
                    for key in ACL_counts.keys(): # percorrer o dicionario
                        f.write("%s,%s\n" % (key, ACL_counts[key])) # escrever no ficheiro csv
                print("File:", file, "has", count, "words entirely in uppercase") # print o numero de palavras em maiusculas
            QMessageBox.information(self, "Success", "ACL.csv successfully created in the Output folder.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def slangWords(self):
        try:
            slang_File = os.path.join(project_dir, "src", "auxiliarFiles", "slang.txt")
            csv_filename = os.path.join(project_dir, "Output", "SlangWords.csv") #criar o ficheiro csv
            files_in_dir = listdir(base_dir) #listar todos os ficheiros na pasta
            slangWords = [] #criar uma lista para guardar as palavras em gíria
            with open(slang_File, 'r') as slangFile: #abrir o ficheiro com as palavras em gíria
                for line in slangFile: #percorrer o ficheiro
                    slangWords.append(line.strip()) #guardar as palavras em gíria na lista
            with open(csv_filename, 'w', newline='') as csvfile: #criar o ficheiro csv
                csvwriter = csv.writer(csvfile)  # criar o writer
                csvwriter.writerow(['File', 'Slang Words'])

                for file in files_in_dir:   #percorrer todos os ficheiros
                    filepath = nltk.data.find(base_dir + file) #encontrar o caminho do ficheiro
                    textfile = open(filepath, 'r').read() #abrir o ficheiro
                    count = 0 #inicializar o contador

                    for word in textfile.split(): #percorrer todas as palavras do ficheiro
                        if word in slangWords: #verificar se a palavra está na lista de palavras em gíria
                            count += 1 #incrementar o contador

                    csvwriter.writerow([file, count]) #escrever no ficheiro csv
            QMessageBox.information(self, "Success", "SlangWords.csv successfully created in the Output folder.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FeaturesEstatisticas()
    window.show()
    sys.exit(app.exec_())