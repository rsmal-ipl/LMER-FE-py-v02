import csv
import os

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
import sys
from os import listdir
import nltk
import liwc
import numpy as np

from nltk.corpus import words
from nltk.sentiment import SentimentIntensityAnalyzer
from nrclex import NRCLex
parse, category_names = liwc.load_token_parser('LIWC2007_English100131.dic')
import re
from collections import Counter

# buscar o caminho da pasta
script_dir = os.path.dirname(os.path.abspath(__file__))
# receber o caminho do projeto
project_dir = os.path.dirname(script_dir)
gazetteers_file = os.path.join(project_dir, "src", "auxiliarFiles", "Gazetteers.txt")
dal_anew_file = os.path.join(project_dir, "src", "auxiliarFiles", "DAL_ANEW.txt")
gi_file = os.path.join(project_dir, "src", "auxiliarFiles", "gi-11788.csv")
warriner_file = os.path.join(project_dir, "src", "auxiliarFiles", "Warriner.txt")

def obter_string_salva():
    with open("caminho_pasta.txt", "r") as arquivo:
        pasta_salva = arquivo.read()
        return pasta_salva

pasta_salva = obter_string_salva()
base_dir = pasta_salva + "/"
def tokenize(text):
    # you may want to use a smarter tokenizer
    for match in re.finditer(r'\w+', text, re.UNICODE):
        yield match.group(0)

class FeaturesSemanticas(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Features Semantics")
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
        allFeatures = QPushButton("All features", self)
        featuresNRCLex = QPushButton("Features NRCLex", self)
        featuresGI = QPushButton("Features GI", self)
        featureDAL_NEW = QPushButton("Featurs DAL_ANEW", self)
        featuresGazeteers = QPushButton("Features Gazetteers", self)
        featuresLIWC = QPushButton("Features LIWC", self)
        featuresWarriner = QPushButton("Features Warriner", self)
        back = QPushButton("Back", self)

        # setting geometry of button
        allFeatures.setGeometry(80, 20, 300, 50)
        featuresNRCLex.setGeometry(80, 100, 300, 50)
        featuresGI.setGeometry(460, 100, 300, 50)
        featureDAL_NEW.setGeometry(460, 20, 300, 50)
        featuresGazeteers.setGeometry(80, 180, 300, 50)
        featuresLIWC.setGeometry(460, 180, 300, 50)
        featuresWarriner.setGeometry(80, 260, 300, 50)
        back.setGeometry(460, 260, 300, 50)

        # adding action to a button
        allFeatures.clicked.connect(self.allFeatures)
        featuresNRCLex.clicked.connect(self.featuresNRCLex)
        featuresGI.clicked.connect(self.featuresGI)
        featureDAL_NEW.clicked.connect(self.featuresDAL_ANEW)
        featuresGazeteers.clicked.connect(self.Gazetteers)
        featuresLIWC.clicked.connect(self.featuresLIWC)
        featuresWarriner.clicked.connect(self.featuresWarriner)
        back.clicked.connect(self.backToMain)


    def centerWindow(self):
        # Get the screen's geometry and center the window on it
        screenGeometry = QDesktopWidget().screenGeometry()
        x = (screenGeometry.width() - self.width()) // 2
        y = (screenGeometry.height() - self.height()) // 2
        self.move(x, y)

    def allFeatures(self):
        try:
            print("All Features")
            self.featuresNRCLex()
            self.featuresGI()
            self.featuresDAL_ANEW()
            self.Gazetteers()
            self.featuresWarriner()
            self.featuresLIWC()
            QMessageBox.information(self, "Success", "All features .csv successfully created in the Output folder.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")



    def Gazetteers(self):
        try:
            gazetteer_files = ["Gazetteers.txt","GazQ1-dal.txt", "GazQ2-dal.txt", "GazQ3-dal.txt", "GazQ4-dal.txt"]
            for gazetteer_file in gazetteer_files:
                print(f"Processing {gazetteer_file}")
                gazetteers_file = os.path.join(project_dir, "src", "auxiliarFiles", gazetteer_file)
                files_in_dir = listdir(base_dir)
                csv_filename = os.path.join(project_dir, "Output", f"{gazetteer_file.split('.')[0]}.csv")

                with open(gazetteers_file, 'r') as f:
                    wordslist_gazetteers = []
                    valence = []
                    arousal = []
                    for line in f:
                        words = line.split()
                        if len(words) >= 3:
                            wordslist_gazetteers.append(words[0])
                            valence.append(float(words[1]))
                            arousal.append(float(words[2]))

                with open(csv_filename, 'w', newline='') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(['File', 'AvgValence', 'AvgArousal'])

                    for file in files_in_dir:
                        word_music_list = []
                        filepath = os.path.join(base_dir, file)
                        with open(filepath, 'r') as f:
                            for line in f:
                                wordlist = line.split()
                                if wordlist:
                                    word_music_list.extend(wordlist)

                        common_words_count = 0
                        valenciatotal = 0
                        arousaltotal = 0

                        for word in word_music_list:
                            if word in wordslist_gazetteers:
                                index = wordslist_gazetteers.index(word)
                                valenciatotal += valence[index]
                                arousaltotal += arousal[index]
                                common_words_count += 1

                        if common_words_count > 0:
                            valenciatotal /= common_words_count
                            arousaltotal /= common_words_count
                        else:
                            # If there are no common words, set both averages to NaN
                            valenciatotal = np.nan
                            arousaltotal = np.nan

                        row_data = [file, valenciatotal, arousaltotal]
                        csvwriter.writerow(row_data)

            QMessageBox.information(self, "Success", "Gazetteer.csv, GazQ1-dal.csv, GazQ2-dal.csv, GazQ3-dal.csv and GazQ4-dal.csv successfully created in the Output folder.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def featuresWarriner(self):
        try:
            csv_filename = os.path.join(project_dir, "Output", "Warriner.csv") # Nome do arquivo CSV
            warriner_ratings = {}  # Dicionário que armazenará os dados
            word_emotion_data = {}  # Dicionário para armazenar as emoções das palavras no arquivo a ser testado

            # Lendo o arquivo Warriner e preenchendo o dicionário
            with open(warriner_file, 'r', encoding='utf-8') as txtfile:
                for line in txtfile:
                    row = line.strip().split('\t')
                    if len(row) == 4:
                        word, valence, arousal, dominance = row
                        warriner_ratings[word.lower()] = {
                            'valence': float(valence),
                            'arousal': float(arousal),
                            'dominance': float(dominance)
                        }

            for file in os.listdir(base_dir):  # Iterar sobre cada arquivo no diretório
                filepath = os.path.join(base_dir, file)  # Obter o caminho completo do arquivo
                lyric_text = open(filepath, 'r').read()  # Ler o arquivo

                lyric_words = lyric_text.lower().split()  # Separar as palavras do texto

                # Inicializar contadores para as emoções
                total_valence = 0
                total_arousal = 0
                total_dominance = 0
                total_matches = 0

                for word in lyric_words:
                    if word in warriner_ratings:
                        total_matches += 1
                        word_data = warriner_ratings[word]
                        total_valence += word_data['valence']
                        total_arousal += word_data['arousal']
                        total_dominance += word_data['dominance']

                if total_matches > 0:
                    average_valence = total_valence / total_matches
                    average_arousal = total_arousal / total_matches
                    average_dominance = total_dominance / total_matches
                else:
                    average_valence = 0
                    average_arousal = 0
                    average_dominance = 0

                word_emotion_data[file] = {
                    'average_valence': average_valence,
                    'average_arousal': average_arousal,
                    'average_dominance': average_dominance
                }

            with open(csv_filename, 'w', newline='') as csvfile:  # Abrir o arquivo CSV para escrita
                csvwriter = csv.writer(csvfile)  # Criar um objeto para escrever no arquivo CSV
                csvwriter.writerow(['File', 'Average Valence', 'Average Arousal',
                                    'Average Dominance'])  # Escrever o cabeçalho do arquivo CSV

                for file, emotion_data in word_emotion_data.items():
                    csvwriter.writerow([file, emotion_data['average_valence'], emotion_data['average_arousal'],
                                        emotion_data['average_dominance']])  # Escrever os dados no arquivo CSV

            print(f"Emotion scores saved to '{csv_filename}'")  # Imprimir mensagem de sucesso
            QMessageBox.information(self, "Success",
                                    "Emotion scores successfully saved to Warriner.csv in the Output folder.")

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def backToMain(self):
        from MainWindow import MainWindow
        self.w = MainWindow()
        self.w.show()
        self.close()

    def featuresNRCLex(self):
        try:
            print("Features NRCLex")
            files_in_dir = listdir(base_dir) # Lista de arquivos no diretório
            csv_filename = os.path.join(project_dir, "Output", "NRCLex.csv") # Nome do arquivo .csv
            with open(csv_filename, 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile) # Cria um objeto csvwriter
                csvwriter.writerow(['Ficheiro', 'Fear', 'Anger', 'Anticip', 'Trust', 'Surprise', 'Positive', 'Negative', 'Sadness', 'Disgust', 'Joy']) # Escreve o cabeçalho do arquivo .csv
                for file in files_in_dir:  # Percorre todos os arquivos no diretório
                    filepath = os.path.join(base_dir, file) # Caminho do arquivo
                    textfile = open(filepath, 'r').read() # Lê o arquivo

                    # Criar um objeto NRCLex para analisar o texto
                    sentiment_obj = NRCLex(textfile) # Cria um objeto NRCLex

                    emotions = sentiment_obj.affect_frequencies # Obter as emoções
                    # Aceder diretamente aos valores das emoções
                    fear_value = emotions['fear']
                    anger_value = emotions['anger']
                    anticip_value = emotions['anticip']
                    trust_value = emotions['trust']
                    surprise_value = emotions['surprise']
                    positive_value = emotions['positive']
                    negative_value = emotions['negative']
                    sadness_value = emotions['sadness']
                    disgust_value = emotions['disgust']
                    joy_value = emotions['joy']

                    # Escrever no arquivo CSV
                    csvwriter.writerow(
                        [file, fear_value, anger_value, anticip_value, trust_value, surprise_value, positive_value,
                         negative_value, sadness_value, disgust_value, joy_value])
            QMessageBox.information(self, "Success", "NRCLex.csv successfully created in the Output folder.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def featuresGI(self):
        try:
            print("Features GI") # Imprime no terminal
            files_in_dir = listdir(base_dir) # Lista de arquivos no diretório
            csv_filename = os.path.join(project_dir, "Output", "GI.csv") # Nome do arquivo .csv
            gi_matrix = [] # Matriz para guardar os valores

            with open(gi_file, 'r') as csvfile:
                csvreader = csv.reader(csvfile)
                next(csvreader)  # Ignora a primeira linha
                for row in csvreader:
                    gi_matrix.append(row)  # Adiciona a linha completa

            # Cabeçalho das colunas
            header =  ['Entry', 'Positiv', 'Negativ', 'Pstv', 'Affil', 'Ngtv', 'Hostile', 'Strong', 'Power', 'Weak',
                      'Submit', 'Active', 'Passive', 'Pleasur', 'Pain', 'Feel', 'Arousal', 'EMOT', 'Virtue', 'Vice',
                      'Ovrst', 'Undrst', 'Academ', 'Doctrin', 'Econ@', 'Exch', 'ECON', 'Exprsv', 'Legal', 'Milit', 'Polit@',
                      'POLIT', 'Relig', 'Role', 'COLL', 'Work', 'Ritual', 'SocRel', 'Race', 'Kin@', 'MALE', 'Female',
                      'Nonadlt', 'HU', 'ANI', 'PLACE', 'Social', 'Region', 'Route', 'Aquatic', 'Land', 'Sky', 'Object',
                      'Tool', 'Food', 'Vehicle', 'BldgPt', 'ComnObj', 'NatObj', 'BodyPt', 'ComForm', 'COM', 'Say', 'Need',
                      'Goal', 'Try', 'Means', 'Persist', 'Complet', 'Fail', 'NatrPro', 'Begin', 'Vary', 'Increas',
                      'Decreas', 'Finish', 'Stay', 'Rise', 'Exert', 'Fetch', 'Travel', 'Fall', 'Think', 'Know', 'Causal',
                      'Ought', 'Perceiv', 'Compare', 'Eval@', 'EVAL', 'Solve', 'Abs@', 'ABS', 'Quality', 'Quan', 'NUMB',
                      'ORD', 'CARD', 'FREQ', 'DIST', 'Time@', 'TIME', 'Space', 'POS', 'DIM', 'Rel', 'COLOR', 'Self', 'Our',
                      'You', 'Name', 'Yes', 'No', 'Negate', 'Intrj', 'IAV', 'DAV', 'SV', 'IPadj', 'IndAdj', 'PowGain',
                      'PowLoss', 'PowEnds', 'PowAren', 'PowCon', 'PowCoop', 'PowAuPt', 'PowPt', 'PowDoct', 'PowAuth',
                      'PowOth', 'PowTot', 'RcEthic', 'RcRelig', 'RcGain', 'RcLoss', 'RcEnds', 'RcTot', 'RspGain', 'RspLoss',
                      'RspOth', 'RspTot', 'AffGain', 'AffLoss', 'AffPt', 'AffOth', 'AffTot', 'WltPt', 'WltTran', 'WltOth',
                      'WltTot', 'WlbGain', 'WlbLoss', 'WlbPhys', 'WlbPsyc', 'WlbPt', 'WlbTot', 'EnlGain', 'EnlLoss',
                      'EnlEnds', 'EnlPt', 'EnlOth', 'EnlTot', 'SklAsth', 'SklPt', 'SklOth', 'SklTOT', 'TrnGain', 'TrnLoss',
                      'TranLw', 'MeansLw', 'EndsLw', 'ArenaLw', 'PtLw', 'Nation', 'Anomie', 'NegAff', 'PosAff', 'SureLw',
                      'If', 'NotLw', 'TimeSpc', 'FormLw'] # Cabeçalho das colunas

            # Abre o arquivo CSV para escrita
            with open(csv_filename, 'w', newline='') as csvfile: # newline='' para evitar linhas em branco
                csvwriter = csv.writer(csvfile) # Cria um objeto csv.writer
                csvwriter.writerow(header) # Escreve o cabeçalho no arquivo CSV

                for file in files_in_dir: # Percorre todos os arquivos do diretório
                    storedMatches = {} # Dicionário para guardar as palavras já encontradas
                    matches = 0 # Contagem de palavras encontradas
                    word_counts = {}  # Contagem de ocorrências de cada palavra do arquivo de texto
                    attribute_counts = {} # Contagem de ocorrências de cada atributo do GI

                    filepath = nltk.data.find(base_dir + file) # Caminho do arquivo
                    textfile = open(filepath, 'r').read() # Lê o arquivo
                    textfile = textfile.lower() # Converte para minúsculo

                    words = textfile.split() # Separa as palavras do arquivo

                    for word in words: # Percorre todas as palavras do arquivo
                        if word not in storedMatches: # Se a palavra não foi encontrada ainda
                            storedMatches[word] = 1 # Adiciona a palavra ao dicionário
                            matches += 1 # Incrementa o contador de palavras encontradas
                        else:
                            storedMatches[word] += 1 # Incrementa o contador de palavras encontradas

                        if word not in word_counts: # Se a palavra não foi contada ainda
                            word_counts[word] = 1 # Adiciona a palavra ao dicionário
                        else:
                            word_counts[word] += 1 # Incrementa o contador de ocorrências da palavra

                    for row in gi_matrix: # Percorre todas as linhas da matriz
                        gi_word = row[0].lower().split("#")[0] # Pega a palavra da linha e converte para minúsculo
                        if gi_word in word_counts: # Se a palavra está no arquivo de texto
                            count = word_counts[gi_word] # Pega a contagem de ocorrências da palavra
                            attributes = row[1:] # Pega os atributos da palavra
                            for attribute, attribute_value in zip(header[1:], attributes): # Percorre os atributos e seus valores
                                if attribute_value != '0': # Se o valor do atributo for diferente de zero
                                    if attribute not in attribute_counts: # Se o atributo não foi contado ainda
                                        attribute_counts[attribute] = 0 # Adiciona o atributo ao dicionário
                                    attribute_counts[
                                        attribute] += count  # Conta o número de vezes que o atributo diferente de zero aparece em todas as palavras do arquivo

                    # Escreve os resultados no arquivo CSV
                    row_data = [file] + [attribute_counts.get(attr, 0) for attr in header[1:]] # Cria uma lista com os valores de cada atributo
                    csvwriter.writerow(row_data) # Escreve a lista no arquivo CSV
            QMessageBox.information(self, "Success", "GI.csv successfully created in the Output folder.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def featuresDAL_ANEW(self):
        try:
            print("Features DAL_ANEW") # Mensagem no console
            files_in_dir = listdir(base_dir) # Lista os arquivos do diretório
            csv_filename = os.path.join(project_dir, "Output", "DAL_ANEW.csv") # Caminho do arquivo CSV

            with open(csv_filename, 'w', newline='') as csvfile: # newline='' para evitar linhas em branco
                csvwriter = csv.writer(csvfile) # Cria um objeto csv.writer
                csvwriter.writerow(['File', 'AvgValence', 'AvgArousal', 'AvgDominance']) # Escreve o cabeçalho no arquivo CSV

                for file in files_in_dir: # Percorre todos os arquivos do diretório
                    storedMatches = [] # Lista para guardar as palavras já encontradas
                    valenciatotal = 0 # Contagem de valência
                    arousaltotal = 0 # Contagem de arousal
                    dominanceTotal = 0 # Contagem de dominance

                    word_music_list = [] # Lista para guardar as palavras do arquivo de texto
                    filepath = nltk.data.find(base_dir + file) # Caminho do arquivo

                    with open(filepath, 'r') as f: # Abre o arquivo
                        for line in f: # Percorre todas as linhas do arquivo
                            wordlist = line.split() # Separa as palavras da linha
                            if wordlist: # Se a lista não estiver vazia
                                word_music_list.extend(wordlist) # Adiciona as palavras à lista

                    with open(dal_anew_file, 'r') as f: # Abre o arquivo DAL_ANEW
                        wordslist_dal_anew = [] # Lista para guardar as palavras do arquivo
                        valence = [] # Lista para guardar os valores de valência
                        arousal = [] # Lista para guardar os valores de arousal
                        dominance = [] # Lista para guardar os valores de dominance
                        for line in f: # Percorre todas as linhas do arquivo
                            words = line.split() # Separa as palavras da linha
                            if words: # Se a lista não estiver vazia
                                wordslist_dal_anew.append(words[0]) # Adiciona as palavras à lista
                                valence.append(words[1]) # Adiciona os valores de valência à lista
                                arousal.append(words[2]) # Adiciona os valores de arousal à lista
                                dominance.append(words[3]) # Adiciona os valores de dominance à lista

                    for words in word_music_list: # Percorre todas as palavras do arquivo de texto
                        if words in wordslist_dal_anew and words not in storedMatches: # Se a palavra está no arquivo DAL_ANEW e não foi encontrada ainda
                            storedMatches.append(words) # Adiciona a palavra à lista de palavras encontradas
                            matches = storedMatches.count(words) # Conta o número de vezes que a palavra aparece no arquivo de texto
                            valenciatotal += float(valence[wordslist_dal_anew.index(words)]) * matches # Soma os valores de valência
                            arousaltotal += float(arousal[wordslist_dal_anew.index(words)]) * matches # Soma os valores de arousal
                            dominanceTotal += float(dominance[wordslist_dal_anew.index(words)]) * matches # Soma os valores de dominance

                    meanValence = valenciatotal / len(storedMatches) # Calcula a média de valência
                    meanArousal = arousaltotal / len(storedMatches) # Calcula a média de arousal
                    meanDominance = dominanceTotal / len(storedMatches) # Calcula a média de dominance
                    csvwriter.writerow([file, meanValence, meanArousal, meanDominance]) # Escreve os resultados no arquivo CSV
            QMessageBox.information(self, "Success", "DAL_ANEW.csv successfully created in the Output folder.") # Mensagem de sucesso
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def featuresLIWC(self):
        try:
            print("Features LIWC") # Mensagem no console
            files_in_dir = listdir(base_dir) # Lista os arquivos do diretório
            csv_filename = os.path.join(project_dir, "Output", "LIWC.csv") # Caminho do arquivo CSV

            with open(csv_filename, 'w', newline='') as csvfile: # newline='' para evitar linhas em branco
                csvwriter = csv.writer(csvfile) # Cria um objeto csv.writer
                header = ['File', 'funct', 'pronoun', 'ppron', 'you', 'social', 'verb', 'auxverb', 'past', 'number', 'conj',
                          'cogmech', 'tentat', 'excl', 'affect', 'posemo', 'achieve', 'ipron', 'certain', 'adverb', 'time',
                          'relativ', 'discrep', 'bio', 'body', 'present', 'negemo', 'health', 'percept', 'feel', 'preps',
                          'space', 'shehe', 'family', 'anx', 'article', 'see', 'incl', 'inhib', 'quant', 'motion', 'hear',
                          'cause', 'leisure'] # Cabeçalho do arquivo CSV
                csvwriter.writerow(header) # Escreve o cabeçalho no arquivo CSV

                for file in files_in_dir: # Percorre todos os arquivos do diretório
                    filepath = nltk.data.find(base_dir + file) # Caminho do arquivo
                    textfile = open(filepath, 'r').read() # Abre o arquivo
                    tokens = tokenize(textfile) # Tokeniza o texto
                    liwc = Counter(category for token in tokens for category in parse(token)) # Conta as categorias LIWC
                    liwc_values = {} # Dicionário para guardar os valores de cada categoria
                    for category in header[1:]: # Percorre todas as categorias
                        liwc_values[category] = liwc[category] # Adiciona os valores ao dicionário
                    row_data = [file] + [liwc_values.get(category, 0) for category in header[1:]] # Lista com os valores de cada categoria
                    csvwriter.writerow(row_data) # Escreve os resultados no arquivo CSV
            QMessageBox.information(self, "Success", "LIWC.csv successfully created in the Output folder.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FeaturesSemanticas()
    window.show()
    sys.exit(app.exec_())