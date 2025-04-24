import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog
import qrcode
from PIL import Image
import ctypes

myappid = 'lxix.genqr.0.1'  # Уникальный идентификатор
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

class QRCodeGenerator(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.qr_generated = False
        self.initUI()
    
    def initUI(self):
        # Установка иконки для окна (должно работать и для панели задач)
        self.setWindowIcon(QtGui.QIcon('icon.png'))  # <- Важно! Должно быть перед setWindowTitle
        
        self.setWindowTitle('Генератор QR-Кодов By LXIX')
        self.setStyleSheet("background-color: #2b2b2b; color: #ffffff;")
        
        # Основной макет
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)
        
        # Макет для ввода URL и кнопки выбора логотипа
        input_layout = QtWidgets.QHBoxLayout()
        
        self.url_label = QtWidgets.QLabel('Вставьте текст или ссылку:', self)
        self.url_label.setStyleSheet("color: #ffffff; font-size: 16px;")  # Установка размера текста
        input_layout.addWidget(self.url_label)
        
        self.url_input = QtWidgets.QLineEdit(self)
        self.url_input.setStyleSheet("background-color: #3c3f41; color: #ffffff; border: 1px solid #5a5a5a;")
        input_layout.addWidget(self.url_input)
        
        main_layout.addLayout(input_layout)
        
        logo_layout = QtWidgets.QHBoxLayout()
        
        self.logo_label = QtWidgets.QLabel('Выберите логотип (если нужно):', self)
        self.logo_label.setStyleSheet("color: #ffffff; font-size: 16px;")  # Установка размера текста
        logo_layout.addWidget(self.logo_label)
        
        self.logo_button = QtWidgets.QPushButton('Выбрать', self)
        self.logo_button.clicked.connect(self.browseLogo)
        self.logo_button.setStyleSheet("background-color: #5a5a5a; color: #ffffff; font-size: 14px;")  # Установка размера текста
        logo_layout.addWidget(self.logo_button)
        
        main_layout.addLayout(logo_layout)
        
        # Макет для кнопок генерации и сохранения QR-кода
        button_layout = QtWidgets.QHBoxLayout()
        
        self.generate_button = QtWidgets.QPushButton('Сгенерировать QR-Code', self)
        self.generate_button.clicked.connect(self.generateQRCode)
        self.generate_button.setStyleSheet("background-color: #5a5a5a; color: #ffffff; font-size: 16px;")  # Установка размера текста
        button_layout.addWidget(self.generate_button)
        
        self.save_button = QtWidgets.QPushButton('Сохранить QR-Code', self)
        self.save_button.clicked.connect(self.saveQRCode)
        self.save_button.setStyleSheet("background-color: #5a5a5a; color: #ffffff; font-size: 16px;")  # Установка размера текста
        self.save_button.setEnabled(False)  # Кнопка отключена по умолчанию
        button_layout.addWidget(self.save_button)
        
        main_layout.addLayout(button_layout)
        
        self.qr_code_label = QtWidgets.QLabel(self)
        self.qr_code_label.setAlignment(QtCore.Qt.AlignCenter)
        self.qr_code_label.setFixedSize(400, 400)
        main_layout.addWidget(self.qr_code_label, alignment=QtCore.Qt.AlignCenter)
        
        self.setFixedSize(600, 600)  # Фиксированный размер окна
        
    def browseLogo(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, 'Выбор Логотипа', '', 'Image Files (*.png *.jpg *.bmp)', options=options)
        if file_name:
            self.logo_path = file_name
    
    def generateQRCode(self):
        url = self.url_input.text()
        if not url:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Please enter a URL or text.')
            return
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
        
        if hasattr(self, 'logo_path'):
            logo = Image.open(self.logo_path)
            qr_img = self.addLogo(qr_img, logo)
        
        qr_img.save('autosave_qr.png')
        
        pixmap = QtGui.QPixmap('autosave_qr.png')
        self.qr_code_label.setPixmap(pixmap)
        
        self.qr_generated = True
        self.save_button.setEnabled(True)  # Включаем кнопку сохранения
    
    def saveQRCode(self):
        if not self.qr_generated:
            QtWidgets.QMessageBox.warning(self, 'Ошибка', 'Please generate the QR code first.')
            return
        
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, 'Сохранение QR-Code', '', 'Image Files (*.png *.jpg *.bmp)', options=options)
        if file_name:
            qr_img = Image.open('autosave_qr.png')
            qr_img.save(file_name)
    
    def addLogo(self, qr_img, logo):
        qr_width, qr_height = qr_img.size
        logo_size = min(qr_width, qr_height) // 4
        logo = logo.resize((logo_size, logo_size))
        
        pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
        qr_img.paste(logo, pos)
        
        return qr_img

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    
    # Установка иконки для приложения (глобально)
    app.setWindowIcon(QtGui.QIcon('icon.png'))  # Это дублирование, но иногда помогает
    
    ex = QRCodeGenerator()
    ex.show()
    sys.exit(app.exec_())