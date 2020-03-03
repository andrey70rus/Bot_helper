#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime
import threading

import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
from PyQt5.QtGui import QColor, QTextCharFormat, QFont
from design import bar_design_progress
import win32com.client as wincl

from PyQt5.QtCore import QBasicTimer, Qt


class ExampleApp(QtWidgets.QMainWindow, bar_design_progress.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.speak = wincl.Dispatch("SAPI.SpVoice")
        #self.engine = pyttsx3.init()
        #self.voices = self.engine.getProperty('voices')
        #self.engine.setProperty('voice', self.voices[0].id)
        #self.engine.setProperty('rate', 70)
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
                "ctime": ('Сколько время', 'час','текущее время','сейчас времени','который час', 'time'),
                "sapr": ('проасу','запусти САПР','запусти проасу','запусти proasu',
                            'включи сапр', 'включи проасу', 'включи proasu'),
                "ch_projnumber": ('Смени шифр в комплекте', 'измени шифр', 'измени номер', 'подготовь шифры', 
                                    'смени шифры', 'перебей номера комплектов'),
                "Kust": ('Сформируй ПД на кустовую площадку', 'сделай куст', 'сделай ПД', 'куст', 'кустовая площадка')
            }
        }
        self.counter = 0
        self.list = []
        self.flag_req = 0
        self.flag_start_dll = 0
        self.questions = []
        self.questions_voice = []

    def ch_projnumber(self):
        #выполнени опроса и формирование словаря для дальнейшей передачи в сапр
        if self.flag_req == 0:
            self.list = []
            self.counter = 0
            self.flag_req = 1
            self.start_voice(self.questions_voice[0])
            return(self.questions[0])
        if self.flag_req == 1:
            self.list.append(self.typing)
            self.typing = ''
            self.counter += 1
            self.start_voice(self.questions_voice[self.counter])
            
            if self.questions[self.counter] == 'Введите подшифр (шаблон: -Р-000.000.000-АК-01-)':
               self.lineEdit.setText('-Р-000.000.000-АК-01-')
				
            if self.questions[self.counter] == 'Укажите Тип комплекта':
                self.items = ['АК', 'АСУ ТП', 'АТХ', 'АТ', 'АСУЭ', 'АПТ']
                self.combobox(self.items)

            if self.questions[self.counter] == 'Выберите Заказчика':
                self.items = ['Заказчик #1', 'Заказчик #2', 'Заказчик #3', 'Заказчик #4', 'Заказчик #5']
                self.combobox(self.items)

            if self.questions[self.counter] == 'Выберите должность разработчика':
                self.items = ['Ведущий инженер', 'Инженер 1 категории', 'Инженер 2 категории', 'Инженер', 'Техник']
                self.combobox(self.items)

            if self.questions[self.counter] == 'Выберите папку с документацией':
                self.plainTextEdit.appendHtml('Бот: <b><span style=color:#1976D2;> Выберите папку </span></b><br>')
                folderpath = self.open_folder()
                self.list.append(folderpath)
                self.plainTextEdit.appendHtml('Я: <b><span style=color:#404040;>' + folderpath + '</span></b><br>')
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

    def voice(self, question_voice):
        self.speak.Speak(question_voice)

    def start_voice(self, question_voice):
        my_thread = threading.Thread(target=self.voice, args=(question_voice,))
        my_thread.start()

    def execute_cmd(self, cmd):
        if cmd == 'ctime':
            # сказать текущее время
            now = datetime.datetime.now()
            self.start_voice('Сейчас ' + str(now.hour) + ":" + str(now.minute))
            return('Сейчас ' + str(now.hour) + ":" + str(now.minute))

        elif cmd == 'ch_projnumber':
            self.questions = ["Введите шифр формируемого комплекта", "Введите подшифр (шаблон: -Р-000.000.000-АК-01-)", "Укажите Тип комплекта",
                         "Выберите Заказчика", "Введите наименование объекта", "Введите [И. О. Фамилия] ГИП",
                         "Выберите должность разработчика", "Введите [Фамилия И.О.] разработчика", "Выберите папку с документацией"]
            self.questions_voice = ["Введите шифр формируемого комплекта", "Введите подшифр", "Укажите тип комплекта",
                         "Выберите Заказчика", "Введите наименование объекта", "Введите Фамилию и инициалы ГИПа",
                         "Выберите должность разработчика", "Введите фамилию и инициалы разработчика", "Выберите папку с документацией"]

            question = self.ch_projnumber()

            if self.flag_start_dll == 0:
                return(question)
            else:
                self.flag_start_dll = 0
                print(self.list)
                #Передача во внешний САПР значений, полученных от пользователя
                self.start_voice('Процесс начат')
                return('Процесс начат')
        elif cmd == 'Kust':
            form = FormKPPD()
            form.pathTemplates = 'C:\\Bot\\FinalBot\\Templates\\'
            form.Show()
            self.start_voice('Заполните форму')
            return('Заполните форму')

# вызов библиотеки внешнего САПР

        else:
            self.start_voice('Команда не распознана, повторите!')
            return('Команда не распознана, повторите!')



    def send_message(self):
        #передать значение обработчику команд (def recognize_cmd)
        editor = QtWidgets.QTextEdit()
        cursor = editor.textCursor()

        boldFormat = QTextCharFormat()
        boldFormat.setFontWeight(QFont.Bold)

        stringg = self.lineEdit.text()

        self.plainTextEdit.appendHtml('Я: <b><span style=color:#404040;>' + stringg + '</span></b><br>')

        if self.flag_req == 0:
            self.cmd = self.lineEdit.text()
        if self.flag_req != 0:
            self.typing = self.lineEdit.text()

        self.lineEdit.clear()

        #Обратная связь

        self.out = self.recognize_cmd(self.cmd)
        self.out = self.execute_cmd(self.out['cmd'])
        self.plainTextEdit.appendHtml('Бот: <b><span style=color:#1976D2;>' + self.out + '</span></b><br>')


    def call_recognize(self):
        #при нажатии кнопки голосового управления - распознавание речи
        r = sr.Recognizer()
        m = sr.Microphone(device_index=0)
#        with m as source:
#            r.adjust_for_ambient_noise(source)
        with sr.Microphone(device_index=0) as source:
            audio = r.listen(source)
	
        recogn = r.recognize_google(audio, language="ru-RU")
        if self.flag_req == 0:
            self.cmd = recogn
			
        if self.flag_req != 0:
            self.typing = recogn

        print('Вы сказали: ' + recogn)
        self.out = self.recognize_cmd(self.cmd)
        self.plainTextEdit.appendHtml('Я: <b><span style=color:#404040;>' + self.opts['commands'][self.out['cmd']][0] + '</span></b><br>')
        self.out = self.execute_cmd(self.out['cmd'])
        self.plainTextEdit.appendHtml('Бот: <b><span style=color:#1976D2;>' + self.out + '</span></b><br>')

    def timerEvent(self, e):
        self.progressBar.setValue(AnalogShifr.Progress)
        if AnalogShifr.Progress >= self.maxPB:
            self.plainTextEdit.appendHtml('Бот: <b><span style=color:#1976D2;>' + 'Процесс завершен' + '</span></b><br>')
            self.progressBar.setValue(0)
            self.timer.stop()
            self.start_voice('Процесс завершен')
            return

    def click_for_progressBar(self):
          
        if self.timer.isActive():
            self.timer.stop()
            self.progressBar.setValue(0)
            self.step = 0
        else:
            self.timer.start(100, self)    	

    def open_folder(self):
        foldername = QtWidgets.QFileDialog.getExistingDirectory(self,"Укажите путь к папке", "C:\\", QtWidgets.QFileDialog.DontUseNativeDialog)
        #foldername = QtWidgets.QFileDialog.getExistingDirectory(self, 'Укажите папку', 'C:\\')
        return foldername

    def combobox(self, items):

        self.plainTextEdit.appendHtml('Бот: <b><span style=color:#1976D2;>' + self.questions[self.counter] + '</span></b><br>')
        text, ok = QtWidgets.QInputDialog.getItem(self, self.questions[self.counter], '', items, 0, False)

        if ok:
            self.list.append(text)
            self.plainTextEdit.appendHtml('Я: <b><span style=color:#404040;>' + text + '</span></b><br>')
            self.counter += 1
            self.start_voice(self.questions_voice[self.counter])


if __name__ == '__main__':
    
    #Дизайн
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение