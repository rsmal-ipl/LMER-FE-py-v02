import csv
import sys
import os
import lyricsgenius
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from os import listdir

from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton
from lyricsgenius import genius
genius = lyricsgenius.Genius("vOLG7Pt7qqPgOgVOMqqJnu5jzR-JB8Abe_dv86DMmvLncIN6-LfFRrC_HbwpBkmb", timeout=10)

# buscar o caminho da pasta
script_dir = os.path.dirname(os.path.abspath(__file__))
# receber o caminho do projeto
project_dir = os.path.dirname(script_dir)
titulos = os.path.join(project_dir, "StructuralBasedFeatures", "titulos.txt")
refrao = os.path.join(project_dir, "StructuralBasedFeatures", "refrao.txt")

def obter_string_salva():
    with open("caminho_pasta.txt", "r") as arquivo:
        pasta_salva = arquivo.read()
        return pasta_salva

pasta_salva = obter_string_salva()
base_dir = pasta_salva + "/"

class StructuralBasedFeatures(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Structural Based Features")
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
        repTitulo = QPushButton("Number of title repetitions", self)
        detRefrao = QPushButton("Chorus detection", self)
        back = QPushButton("Back", self)

        # setting geometry of button
        repTitulo.setGeometry(280, 50, 300, 50)
        detRefrao.setGeometry(280, 140, 300, 50)
        back.setGeometry(280, 230, 300, 50)

        back.clicked.connect(self.back)
        repTitulo.clicked.connect(self.contarRepeticoesDoTitulo)
        detRefrao.clicked.connect(self.extract_chorus_from_song)

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

    def contarRepeticoesDoTitulo(self):
        try:
            files_in_dir = listdir(base_dir)  # listar os ficheiros da pasta
            csv_filename = os.path.join(project_dir, "Output", "RepTitles.csv")  # criar o ficheiro csv
            with open(csv_filename, 'w', newline='') as csvfile:  # abrir o ficheiro csv
                csvwriter = csv.writer(csvfile)  # criar o writer
                csvwriter.writerow(["Name of file", "Number of repetitions"])  # escrever o cabeçalho
                for file in files_in_dir:  # percorrer os ficheiros da pasta
                    titulo_encontrado = False  # inicializar a variável
                    counter = 0  # inicializar o contador
                    with open(base_dir + file, "r") as arquivo_musica:  # abrir o ficheiro de música
                        for linha_musica in arquivo_musica:  # percorrer as linhas do ficheiro de música
                            for linha in open(titulos, "r"):  # percorrer as linhas do ficheiro de títulos
                                titulo_partes = linha.strip().split("--")  # separar o título do artista
                                tituloficheiro = titulo_partes[0].strip()  # obter o título do ficheiro
                                tituloMusica = titulo_partes[1].strip()  # obter o título da música

                                if file.strip().lower() == tituloficheiro.strip().lower():  # comparar o título do ficheiro com o título do ficheiro de títulos
                                    if tituloMusica in linha_musica.strip():  # verificar se o título da música está na linha da música
                                        counter += 1  # incrementar o contador
                                        titulo_encontrado = True  # atualizar a variável
                                        break  # sair do ciclo

                    # Criar uma lista com os valores a serem escritos na linha do ficheiro CSV
                    row_data = [file, counter]

                    csvwriter.writerow(row_data)  # escrever a lista no ficheiro CSV

            QMessageBox.information(self, "Success", "RepTitles.csv successfully created in the Output folder.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")


    def extract_chorus(self, lyrics):
        if isinstance(lyrics, str): # verificar se o parâmetro é uma string
            lines = lyrics.split("\n") # separar as linhas da letra
            chorus_lines = [] # inicializar a lista
            in_chorus = False # inicializar a variável

            for line in lines: # percorrer as linhas da letra
                line = line.strip() # remover espaços em branco do início e fim da linha

                if line.startswith("[Chorus"): # verificar se a linha começa com [Chorus
                    in_chorus = True # atualizar a variável
                    continue
                elif line.startswith("["): # verificar se a linha começa com [
                    in_chorus = False # atualizar a variável
                    continue  # passar para a próxima linha

                if in_chorus and line: # verificar se a variável é verdadeira e se a linha não está vazia
                    chorus_lines.append(line) # adicionar a linha à lista

            chorus = "\n".join(chorus_lines) # juntar as linhas da lista numa string
            return chorus # retornar a string
        else:
            return None

    def extract_chorus_from_song(self):
        try:
            csv_filename = os.path.join(project_dir, "Output", "Chorus.csv")  # criar o ficheiro csv
            with open(refrao, "r") as arquivo, open(csv_filename, 'w',
                                                    newline='') as csvfile:  # abrir o ficheiro de títulos e o ficheiro csv
                csvwriter = csv.writer(csvfile)  # criar o writer
                csvwriter.writerow(['Nome ficheiro', 'artista', 'nome'])  # escrever o cabeçalho

                for linha in arquivo:  # percorrer as linhas do ficheiro de títulos
                    titulo_original = linha.strip()  # Remove espaços em branco do início e fim da linha
                    titulo_partes = linha.split("-")  # separar o título do artista
                    if len(titulo_partes) >= 4:  # verificar se o título tem 4 partes
                        lyrics_depois_do_hifen2 = titulo_partes[2]  # obter o artista
                        lyrics_depois_do_hifen3 = titulo_partes[3]  # obter o nome da música
                        artista = lyrics_depois_do_hifen2.strip().lower()  # remover espaços em branco do início e fim da linha e converter para minúsculas
                        nome_musica = lyrics_depois_do_hifen3.strip().lower()  # remover espaços em branco do início e fim da linha e converter para minúsculas
                        nomeFicheiro = titulo_partes[0] + "-" + titulo_partes[1]  # obter o nome do ficheiro
                        song = genius.search_song(artista, nome_musica)  # pesquisar a música no Genius

                        if song is not None:  # verificar se a música foi encontrada
                            lyrics = song.lyrics  # obter a letra da música
                            if lyrics:  # verificar se a letra da música foi encontrada
                                chorus = self.extract_chorus(lyrics)  # obter o refrão da música
                                csvwriter.writerow([nomeFicheiro, artista, nome_musica,
                                                    ""])  # escrever o nome do ficheiro, o artista e o nome da música no ficheiro csv
                                csvwriter.writerow(['Chorus'])  # escrever o cabeçalho do refrão
                                for line in chorus.split('\n'):  # Escrever cada linha do refrão separadamente
                                    csvwriter.writerow([line.strip()])
                                print("Chorus extracted for", nomeFicheiro)
                            else:
                                print("Lyrics not found for the song.")
                        else:
                            print("Song not found.")
                    else:
                        print("Song not found.")
            QMessageBox.information(self, "Success", "Chorus.csv successfully created in the Output folder.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StructuralBasedFeatures()
    window.show()
    sys.exit(app.exec_())