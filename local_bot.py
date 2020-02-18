#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime

import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
from PyQt5.QtGui import QColor, QTextCharFormat, QFont
from design import bar_design_progress

from PyQt5.QtCore import QBasicTimer, Qt

class ExampleApp(QtWidgets.QMainWindow, bar_design_progress.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.pushButton_2.released.connect(self.send_message)
        self.lineEdit.returnPressed.connect(self.pushButton_2.released) #отправка сообщений по <enter>
        self.toolButton.clicked.connect(self.call_recognize)
#        self.pushButton.released.connect(self.click_for_progressBar)
        self.step = 0
        self.timer = QBasicTimer()
        self.progressBar.setMaximum(5)
        self.opts = {
            "alias": ('помощник','сапр','бот','помощь','bot','helper',
                    'цифровой помощник'),
            "commands": {
                "ctime": ('час','текущее время','сейчас времени','который час', 'time'),
                "sapr": ('проасу','запусти САПР','запусти проасу','запусти proasu',
                            'включи сапр', 'включи проасу', 'включи proasu'),
                "ch_projnumber": ('измени шифр', 'измени номер', 'подготовь шифры', 
                                    'смени шифры', 'перебей номера комплектов')
            }
        }
        self.counter = 0
        self.list = []
        self.flag_req = 0
        self.flag_start_dll = 0
        self.questions = []

    def ch_projnumber(self):
        #выполнени опроса и формирование словаря для дальнейшей передачи в сапр
        if self.flag_req == 0:
            self.list = []
            self.counter = 0
            self.flag_req = 1
            return(self.questions[0])
        if self.flag_req == 1:
            self.list.append(self.typing)
            self.typing = ''
            self.counter += 1

            if self.questions[self.counter] == 'Укажите Тип комплекта':
                self.items = ['АК', 'АСУ ТП', 'АТХ', 'АТ', 'АСУЭ', 'АПТ']
                self.combobox(self.items)

            if self.questions[self.counter] == 'Выберите Заказчика':
                self.items = ['Заказчик1', 'Заказчик2']
                self.combobox(self.items)


            if self.questions[self.counter] == 'Должность разработчика':
                self.items = ['Инженер 2 категории', 'Инженер 1 категории', 'Инженер', 'Ведущий инженер']
                self.combobox(self.items)

            if self.questions[self.counter] == 'Выберите папку':
                self.plainTextEdit.appendHtml('BOT: <b><span style=color:#33CCCC;> Выберите папку </span></b><br>')
                folderpath = self.open_folder()
                self.list.append(folderpath)
                self.plainTextEdit.appendHtml('Я: <b><span style=color:#3399CC;>' + folderpath + '</span></b><br>')
                self.counter += 1

            if self.counter < len(self.questions):
                return(self.questions[self.counter])
            else:
                self.flag_req = 0
                self.flag_start_dll = 1
                return

    def recognize_cmd(self, cmd):
        #распознавание команды "нечеткой логикой"
        RC = {'cmd': '', 'percent': 35}
        for c,v in self.opts['commands'].items():
    
            for x in v:
                vrt = fuzz.ratio(self.cmd, x)
                if vrt > RC['percent']:
                    RC['cmd'] = c
                    RC['percent'] = vrt
        return RC

    def execute_cmd(self, cmd):
        if cmd == 'ctime':
            # сказать текущее время
            now = datetime.datetime.now()
            return('Сейчас ' + str(now.hour) + ":" + str(now.minute))
    
        elif cmd == 'sapr':
            # запуск сапр
            os.system('xdg-open //home//andreyk//Загрузки//List_only.csv')
    
        elif cmd == 'ch_projnumber':
            self.questions = ["Введите шифр формируемого комплекта", "Введите подшифр", "Укажите Тип комплекта",
                         "Выберите Заказчика", "Введите наименование объекта", "Введите И. О. Фамилия ГИП",
                         "Должность разработчика", "Введите Фамилия И.О. разработчика", "Выберите папку"]

            question = self.ch_projnumber()

            if self.flag_start_dll == 0:
                return(question)
            else:
                self.flag_start_dll = 0
                print(self.list)
                return('Процесс завершен!')

# вызов библиотеки проасу

        else:
            return('Команда не распознана, повторите!')



    def send_message(self):
        #передать значение обработчику команд (def recognize_cmd)
        editor = QtWidgets.QTextEdit()
        cursor = editor.textCursor()

        boldFormat = QTextCharFormat()
        boldFormat.setFontWeight(QFont.Bold)

        stringg = self.lineEdit.text()

        self.plainTextEdit.appendHtml('Я: <b><span style=color:#3399CC;>' + stringg + '</span></b><br>')

        if self.flag_req == 0:
            self.cmd = self.lineEdit.text()
        if self.flag_req != 0:
            self.typing = self.lineEdit.text()

        self.lineEdit.clear()

        #Обратная связь

        self.out = self.recognize_cmd(self.cmd)
        self.out = self.execute_cmd(self.out['cmd'])
        self.plainTextEdit.appendHtml('BOT: <b><span style=color:#33CCCC;>' + self.out + '</span></b><br>')


    def call_recognize(self, recognizer, audio):
        #при нажатии кнопки голосового управления - распознавание речи
        r = sr.Recognizer()
        m = sr.Microphone(device_index=1)
#        with m as source:
#            r.adjust_for_ambient_noise(source)
        self.plainTextEdit.appendHtml('BOT: <b><span style=color:#33CCCC;> Жду Вашу команду... </span></b><br>')
        if self.flag_req == 0:
            self.cmd = recognizer.recognize_google(audio, language = "ru-RU").lower()
        if self.flag_req != 0:
            self.typing = self.lineEdit.text()

        self.plainTextEdit.appendPlainText(self.cmd)

        print('Вы сказали: ' + self.cmd)

    def timerEvent(self, e):
        if self.step >= 100:
            self.timer.stop()
            return

        self.step = self.step + 1
        self.progressBar.setValue(self.step)

    def click_for_progressBar(self):
          
        if self.timer.isActive():
            self.timer.stop()
            self.progressBar.setValue(0)
            self.step = 0
        else:
            self.timer.start(100, self)    	

    def open_folder(self):
        foldername = QtWidgets.QFileDialog.getExistingDirectory(self, 'Укажите папку', '/home')
        return foldername

    def combobox(self, items):

        self.plainTextEdit.appendHtml('BOT: <b><span style=color:#33CCCC;>' + self.questions[self.counter] + '</span></b><br>')
        text, ok = QtWidgets.QInputDialog.getItem(self, self.questions[self.counter], '', items, 0, False)

        if ok:
            self.list.append(text)
            self.plainTextEdit.appendHtml('Я: <b><span style=color:#3399CC;>' + text + '</span></b><br>')
            self.counter += 1

#        typecompl, ok = QtWidgets.QInputDialog.getText(self, 'Укажите Тип комплекта')

#        if ok:
#            self.le.setText(str(typecompl))
#        return typecompl

if __name__ == '__main__':
    
    #Дизайн
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение