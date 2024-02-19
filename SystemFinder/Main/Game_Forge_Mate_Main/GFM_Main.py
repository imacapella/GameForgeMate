import sys
import csv
import subprocess
import pandas as pd
import sys
import subprocess
import os
import signal
import time
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QCompleter, QHBoxLayout, QPushButton, QListWidget, QListWidgetItem
from PyQt5.QtGui import QPainter, QLinearGradient, QFont, QPixmap, QDesktopServices, QIcon
from PyQt5.QtCore import Qt, QStringListModel, QTimer, QUrl, QFileSystemWatcher

class GradualGradientBackground(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Game Forge Mate')
        self.setGeometry(100, 100, 800, 600)
        self.setFixedSize(800, 600)

        icon_path = 'SystemFinder/Main/Game_Forge_Mate_Main/logo.png'

        # window icon
        self.setWindowIcon(QIcon(icon_path))

        self.gradient = QLinearGradient(0, 0, 0, self.height())
        self.gradient.setColorAt(0.0, Qt.blue)
        self.gradient.setColorAt(1.0, Qt.magenta)

        # Logo görüntü
        self.logo_label = QLabel(self)
        self.logo_label.setGeometry(40, 0, 100, 100)

        # Logo görüntü boyutu
        logo_pixmap = QPixmap('SystemFinder/Main/Game_Forge_Mate_Main/logo.png')
        logo_pixmap = logo_pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo_label.setPixmap(logo_pixmap)

        # Sol üst köşede metin eklemek için QLabel kullanımı
        self.text_label = QLabel(self)
        self.text_label.setGeometry(100, 25, 300, 50)
        self.text_label.setText('Game Forge Mate')

        # Metin fontunu değiştirmek için QFont kullanımı
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.text_label.setFont(font)
        self.text_label.setStyleSheet('color: white;')

        # Arama çubuğu
        self.search_bar = QLineEdit(self)
        self.search_bar.setGeometry(500, 50, 200, 20)

        # Arama tahminleri için bir QCompleter oluşturdum
        self.completer = QCompleter()
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setFilterMode(Qt.MatchContains)

        #3
        # CSV dosyasından tahmin verilerini aldım ve QCompleter'a ekledim
        suggestions = self.load_suggestions_from_csv('SystemFinder/Main/Game_Forge_Mate_Main/3_searchbar.csv')
        self.completer.setModel(QStringListModel(suggestions))
        self.search_bar.setCompleter(self.completer)

        # Listeyi ve düğme
        self.word_list = QListWidget(self)
        self.word_list.setGeometry(50, 100, 200, 300)

        self.add_button = QPushButton('Ekle', self)
        self.add_button.setGeometry(700, 50, 75, 20)
        self.add_button.clicked.connect(self.add_word)

        self.remove_button = QPushButton('Sil', self)
        self.remove_button.setGeometry(50, 410, 75, 30)
        self.remove_button.clicked.connect(self.remove_word)

        # kaydet ve çalıştır
        self.save_button = QPushButton('Kaydet ve Çalıştır', self)
        self.save_button.setGeometry(130, 410, 120, 30)
        self.save_button.clicked.connect(self.save_and_run)

        # urllerin  bölmesi
        self.left_panel = QWidget(self)
        self.left_panel.setGeometry(400, 70, 250, 500)

        # Linkler bölmesi
        self.link_label = QLabel(self.left_panel)
        self.link_label.setGeometry(0, 0, 250, 30)
        self.link_label.setText("Linkler:")
        self.link_label.setAlignment(Qt.AlignCenter)

        # Linklerin bulunduğu liste
        self.link_list = QListWidget(self.left_panel)
        self.link_list.setGeometry(0, 30, 250, 470)

        # Linkleri yükleme işlemi
        self.update_links()  # Uygulama başlatıldığında veya CSV dosyası değiştiğinde otomatik olarak yükle
        #2
        # CSV dosyasını izlemek için bir QFileSystemWatcher oluşturduk
        self.csv_watcher = QFileSystemWatcher()
        self.csv_watcher.addPath('SystemFinder/Main/Game_Forge_Mate_Main/2_product_links.csv')
        self.csv_watcher.fileChanged.connect(self.update_links)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), self.gradient)

    def load_suggestions_from_csv(self, filename):
        suggestions = []
        try:
            with open(filename, 'r', newline='',encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    suggestions.extend(row)
        except Exception as e:
            print(f"Error loading CSV file: {str(e)}")
        return suggestions

    def add_word(self):
        word = self.search_bar.text()
        if word:
            item = QListWidgetItem(word)
            self.word_list.addItem(item)
            self.search_bar.clear()

    def remove_word(self):
        selected_item = self.word_list.currentItem()
        if selected_item:
            row = self.word_list.row(selected_item)
            self.word_list.takeItem(row)

    def save_and_run(self):
        # CSV dosyasını Pandas ile kaydetme işlemi
        csv_filename = 'SystemFinder/Main/Game_Forge_Mate_Main/1_games_list.csv'
        data = {'GameName': []}

        for row in range(self.word_list.count()):
            item = self.word_list.item(row)
            data['GameName'].append(item.text())

        df = pd.DataFrame(data)
        df.to_csv(csv_filename, index=False)
#Service
        python_filename = 'SystemFinder/Main/Game_Forge_Mate_Main/GFM Firebase Bridge Service.py'
        subprocess.Popen(['python', python_filename])
#Scraping
        time.sleep(0.2)
        # Belirttiğiniz Python dosyasını çalıştırın
        python_filename = 'SystemFinder/Main/Game_Forge_Mate_Main/GFM_WebScraping.py'
        subprocess.Popen(['python', python_filename])

    def update_links(self):
        self.link_list.clear()  # Mevcut linkleri temizle

        # CSV dosyasındaki linkleri okuyup listeleme
        csv_filename = 'SystemFinder/Main/Game_Forge_Mate_Main/2_product_links.csv'
        #Links
        links = []

        try:
            with open(csv_filename, 'r', newline='') as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    links.extend(row)
        except Exception as e:
            print(f"Error loading CSV file: {str(e)}")

        # Linkleri listeye ekliyoruz
        for i, link in enumerate(links, start=1):
            if link:
                item = QListWidgetItem(f"URL {i}")
                item.setData(Qt.UserRole, link)  
                self.link_list.addItem(item)

        # Linkler tıklanabilir olsun ve tarayıcıda açılsın
        self.link_list.itemClicked.connect(self.open_link)

    def open_link(self, item):
        link = item.data(Qt.UserRole)
        if link:
            QDesktopServices.openUrl(QUrl(link))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GradualGradientBackground()
    window.show()
    sys.exit(app.exec_())
