import sys
from nltk.tokenize import word_tokenize
import string
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer

import ngrams as ngrams
import nltk
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
import os

nltk.download("stopwords")

import csv
from PyQt5.QtWidgets import QDesktopWidget, QMessageBox
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QRadioButton, QPushButton, QButtonGroup
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

from nltk.util import ngrams

# buscar o caminho da pasta
script_dir = os.path.dirname(os.path.abspath(__file__))
# receber o caminho do projeto
project_dir = os.path.dirname(script_dir)


def obter_string_salva():
    with open("caminho_pasta.txt", "r") as arquivo:
        pasta_salva = arquivo.read()
        return pasta_salva

def ngrams(word_list, n):
    ngrams_list = zip(*[word_list[i:] for i in range(n)])
    return [" ".join(ngram) for ngram in ngrams_list]

csv_filename = os.path.join(project_dir, "Output", "CBF.csv")
csv_boolean = os.path.join(project_dir, "Output", "CBF_Boolean.csv")
csv_tfidf = os.path.join(project_dir, "Output", "CBF_TFIDF.csv")
origem = obter_string_salva()
base_dir = origem + "/"


class OpenCBF(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Open CBF Features")
        # Create a QGridLayout instance
        layout = QGridLayout()
        window = QWidget()
        self.UiComponents()
        self.setWindowIcon(QIcon('Music.ico'))
        self.show()
        # Set the layout on the application's window
        self.setLayout(layout)

    def UiComponents(self):
        self.resize(850, 350)  # Set the initial size of the window
        self.centerWindow()

        # creating a push button
        self.label = QLabel("N-Gramas", self)
        uni = QRadioButton("Unigramas", self)
        bi = QRadioButton("Bigramas", self)
        tri = QRadioButton("Trigramas", self)

        self.label1 = QLabel("StopWords", self)
        nada = QRadioButton("nada", self)
        st = QRadioButton("st", self)
        sw = QRadioButton("sw", self)
        st_sw = QRadioButton("st_sw", self)

        self.label2 = QLabel("TF", self)
        freq = QRadioButton("freq", self)
        bool = QRadioButton("bool", self)
        tfdif = QRadioButton("tfdif", self)

        confirm = QPushButton("Confirm", self)
        back = QPushButton("Back", self)

        uni.setProperty("value", "1")
        bi.setProperty("value", "2")
        tri.setProperty("value", "3")

        nada.setProperty("value", "nada")
        st.setProperty("value", "st")
        sw.setProperty("value", "sw")
        st_sw.setProperty("value", "st_sw")

        freq.setProperty("value", "freq")
        bool.setProperty("value", "bool")
        tfdif.setProperty("value", "tfidf")

        # setting geometry of button
        self.label.setGeometry(160, 40, 300, 50)
        uni.setGeometry(160, 70, 300, 50)
        bi.setGeometry(160, 100, 300, 50)
        tri.setGeometry(160, 130, 300, 50)
        self.group1 = QButtonGroup()

        self.label1.setGeometry(400, 40, 300, 50)
        nada.setGeometry(400, 70, 300, 50)
        st.setGeometry(400, 100, 300, 50)
        sw.setGeometry(400, 130, 300, 50)
        st_sw.setGeometry(400, 160, 300, 50)
        self.group2 = QButtonGroup()

        self.label2.setGeometry(640, 40, 300, 50)
        freq.setGeometry(640, 70, 300, 50)
        bool.setGeometry(640, 100, 300, 50)
        tfdif.setGeometry(640, 130, 300, 50)
        self.group3 = QButtonGroup()

        self.group1.addButton(uni)
        self.group1.addButton(bi)
        self.group1.addButton(tri)
        self.group2.addButton(nada)
        self.group2.addButton(st)
        self.group2.addButton(sw)
        self.group2.addButton(st_sw)
        self.group3.addButton(freq)
        self.group3.addButton(bool)
        self.group3.addButton(tfdif)

        self.group1.setExclusive(True)
        self.group2.setExclusive(True)
        self.group3.setExclusive(True)

        confirm.setGeometry(160, 250, 250, 50)
        back.setGeometry(450, 250, 250, 50)

        confirm.clicked.connect(self.confirm)
        back.clicked.connect(self.back)

    def centerWindow(self):
        # Get the screen's geometry and center the window on it
        screenGeometry = QDesktopWidget().screenGeometry()
        x = (screenGeometry.width() - self.width()) // 2
        y = (screenGeometry.height() - self.height()) // 2
        self.move(x, y)

    def create_csv_filename(self, ngram_option, processing_option, count_option):
        # Create a unique name for the CSV file based on the user's choices
        csv_filename = f"{ngram_option}_{processing_option}_{count_option}_.csv"  # {term_frequency_option}

        return os.path.join(project_dir, "Output", csv_filename)



    def confirm(self):
        try:
            all_words = []
            files_processed_words = []  # Armazena as palavras processadas de cada arquivo

            n_gram_option = self.group1.checkedButton().property("value")
            count_option = self.group3.checkedButton().property("value")
            processing_option = self.group2.checkedButton().property("value")

            csv_filename = self.create_csv_filename(n_gram_option, processing_option, count_option)


            print(csv_filename)
            print(n_gram_option)
            print(count_option)
            print(processing_option)

            for filename in os.listdir(origem):
                with open(os.path.join(origem, filename), 'r') as f: # abre o ficheiro
                    alltext = f.read() # le o ficheiro
                    wordFiletoFile = word_tokenize(alltext) # tokeniza o ficheiro
                    wordsAllFile = word_tokenize(alltext) # tokeniza o ficheiro
                    #convert to lower case
                    wordsAllFile = [word.lower() for word in wordsAllFile]
                    wordFiletoFile = [word.lower() for word in wordFiletoFile]

                    # Processamento das palavras
                    processed_words_AllFiles = self.process_words(wordsAllFile, processing_option)
                    processed_words_FiletoFile = self.process_words(wordFiletoFile, processing_option)

                    files_processed_words.append(processed_words_FiletoFile)  # Armazena palavras processadas do arquivo
                    all_words.extend(processed_words_AllFiles)  # Adiciona palavras processadas à lista consolidada

            if n_gram_option == "1":
                ngramsAllFiles = list(ngrams(all_words, 1)) # Cria os n-grams
                ngram_docs = [" ".join(file_words) for file_words in files_processed_words] # Cria os n-grams
                print(ngramsAllFiles)

            elif n_gram_option == "2":
                ngramsAllFiles = list(ngrams(all_words, 2)) # Cria os n-grams
                ngram_docs = [" ".join(file_words) for file_words in files_processed_words] # Cria os n-grams

                print(ngramsAllFiles)

            elif n_gram_option == "3": # Se a opção for 3-gram
                ngramsAllFiles = list(ngrams(all_words, 3)) # Cria os 3-gramas
                ngram_docs = [" ".join(file_words) for file_words in files_processed_words] # Cria os n-grams

                print(ngramsAllFiles)

            else:
                print("Invalid Option")

            if count_option == "freq":
                with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile: # Cria o ficheiro CSV
                    csvwriter = csv.writer(csvfile) # Cria o escritor CSV
                    header = ['File'] + ngramsAllFiles # Cria o cabeçalho do CSV
                    csvwriter.writerow(header) # Escreve o cabeçalho no CSV

                    for filename, file_words in zip(os.listdir(origem), files_processed_words): # Percorre os ficheiros
                        if n_gram_option == "1": # Se a opção for 1-gram
                            ngramsFileToFile = list(ngrams(file_words, 1)) # Cria os 1-gramas
                        elif n_gram_option == "2": # Se a opção for 2-gram
                            ngramsFileToFile = list(ngrams(file_words, 2)) # Cria os 2-gramas
                        elif n_gram_option == "3": # Se a opção for 3-gram
                            ngramsFileToFile = list(ngrams(file_words, 3)) # Cria os 3-gramas
                        else:
                            continue

                        ngram_counts = Counter(ngramsFileToFile) # Conta os n-gramas
                        row_values = [filename] + [ngram_counts[ngram] if ngram in ngram_counts else 0 for ngram in
                                                   ngramsAllFiles] # Cria a linha do CSV
                        csvwriter.writerow(row_values) # Escreve a linha no CSV

            elif count_option == "tfidf": # Se a opção for TF-IDF
                tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, int(n_gram_option))) # Cria o vetorizador TF-IDF
                tfidf_matrix = tfidf_vectorizer.fit_transform(ngram_docs) # Cria a matriz TF-IDF
                feature_names = tfidf_vectorizer.get_feature_names_out() # Obtém os nomes das features

                with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile: # Cria o ficheiro CSV
                    csvwriter = csv.writer(csvfile) # Cria o escritor CSV
                    header = ['File'] + ngramsAllFiles # Cria o cabeçalho do CSV
                    csvwriter.writerow(header) # Escreve o cabeçalho no CSV

                    for filename, tfidf_row in zip(os.listdir(origem), tfidf_matrix.toarray()): # Percorre os ficheiros
                        row_values = [filename] + list(tfidf_row) # Cria a linha do CSV
                        csvwriter.writerow(row_values) # Escreve a linha no CSV

            elif count_option == "bool": # Se a opção for booleana
                ngram_presence_data = [] # Armazena a presença dos n-gramas

                for filename, file_words in zip(os.listdir(origem), files_processed_words): # Percorre os ficheiros
                    if n_gram_option == "1": # Se a opção for 1-gram
                        ngramsFileToFile = list(ngrams(file_words, 1)) # Cria os 1-gramas
                    elif n_gram_option == "2": # Se a opção for 2-gram
                        ngramsFileToFile = list(ngrams(file_words, 2)) # Cria os 2-gramas
                    elif n_gram_option == "3": # Se a opção for 3-gram
                        ngramsFileToFile = list(ngrams(file_words, 3)) # Cria os 3-gramas
                    else:
                        continue

                    ngram_presence = [1 if ngram in ngramsFileToFile else 0 for ngram in ngramsAllFiles] # Verifica a presença dos n-gramas
                    ngram_presence_data.append([filename] + ngram_presence) # Adiciona a presença dos n-gramas à lista

                with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile: # Cria o ficheiro CSV
                    csvwriter = csv.writer(csvfile) # Cria o escritor CSV
                    header = ['File'] + ngramsAllFiles # Cria o cabeçalho do CSV
                    csvwriter.writerow(header) # Escreve o cabeçalho no CSV

                    for row in ngram_presence_data: # Percorre as linhas
                        csvwriter.writerow(row) # Escreve a linha no CSV
            else:
                print("Invalid Option")
            QMessageBox.information(self, "Success",  n_gram_option + '_' + processing_option + '_'+count_option + '_.csv successfully created in the Output folder.')
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")


    def process_words(self, words, processing_option):
        processed_words = words

        if processing_option == "st": # Se a opção for stemming
            processed_words = self.removeStemming(words) # Remove o stemming
        elif processing_option == "sw": # Se a opção for stop words
            processed_words = self.removeStopWords(words) # Remove as stop words
        elif processing_option == "st_sw":  # Se a opção for stemming e stop words
            stemmed_words = self.removeStemming(words) # Remove o stemming
            processed_words = self.removeStopWords(stemmed_words) # Remove as stop words

        # Remove pontuação
        processed_words = [word for word in processed_words if word not in string.punctuation] # Remove a pontuação

        return processed_words

    def removeStemming(self, word_list):
        stemmer = PorterStemmer() # Cria o stemmer
        stemmed_words = [stemmer.stem(word) for word in word_list] # Remove o stemming
        return stemmed_words # Retorna as palavras sem stemming

    def removeStopWords(self, word_list): # Remove as stop words
        stop_words = set(stopwords.words('english')) # Obtém as stop words
        filtered_words = [word for word in word_list if word.lower() not in stop_words] # Remove as stop words
        return filtered_words # Retorna as palavras sem stop words





    def back(self):
        from ContentBaseFeatures.MainContentBasedFeatures import ContentBasedFeatures
        self.w = ContentBasedFeatures()
        self.w.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OpenCBF()
    window.show()
    sys.exit(app.exec_())
