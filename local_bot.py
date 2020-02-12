#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime
# import clr
# clr.AddReference('AnalogShifr')
# from AnalogShifr import *

import sys  # для передачи argv в QApplication
from PyQt5 import QtWidgets
from design import bar_design_progress

from PyQt5.QtCore import QBasicTimer

class ExampleApp(QtWidgets.QMainWindow, bar_design_progress.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.pushButton_2.released.connect(self.send_message)
        self.lineEdit.returnPressed.connect(self.pushButton_2.released) #отправка сообщений по <enter>
        self.toolButton.clicked.connect(self.call_recognize)
        self.pushButton.released.connect(self.click_for_progressBar)
        self.step = 0
        self.timer = QBasicTimer()
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

    def ch_projnumber(self, questions):
        #выполнени опроса и формирование словаря для дальнейшей передачи в сапр
        if self.flag_req == 0:
            self.list = []
            self.counter = 0
            self.flag_req = 1
            return(questions[0])
        if self.flag_req == 1:
            self.list.append(self.typing)
            self.typing = ''
            self.counter += 1
            if self.counter < len(questions):
                return(questions[self.counter])
            else:
                self.flag_req = 0
                self.flag_start_dll = 1
                return('')



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
            questions = ["Введите шифр формируемого комплекта", "Введите подшифр", "Укажите Тип комплекта", "Выберите Заказчика", "Введите наименование объекта", "Введите И. О. Фамилия ГИП", "Должность разработчика", "Введите Фамилия И.О. разработчика", "Введите папку"]

            question = self.ch_projnumber(questions)

            if self.flag_start_dll == 0:
                return(question)
            else:
                # self.flag_start_dll = 0
                # AnalogShifr.Init(self.list[0], self.list[1], self.list[2], self.list[3], self.list[4], self.list[5], self.list[6], self.list[7])
                # InitData.DocASU[4].Datai = "235263"
                # InitData.DocASU[8].Datai = "235268"
                # InitData.DocASU[16].Datai = "235275"
                # AnalogShifr.path = self.list[8]
                # AnalogShifr.pathToTemplates = "C:\\Bot\\testShifr\\Templates"
                # self.maxPB = AnalogShifr.MaximumProgressBar(AnalogShifr.path)
                # self.progressBar.setMaximum(self.maxPB)
                # self.timer.start(100, self)  
                # AnalogShifr.StartCreateDoc()
                return('Процесс начат')
# вызов формирующей комплект документации библиотеки .dll C#

        else:
            return('Команда не распознана, повторите!')

    def send_message(self):
        #передать значение обработчику команд (def recognize_cmd)
        self.plainTextEdit.appendPlainText(self.lineEdit.text())

        if self.flag_req == 0:
            self.cmd = self.lineEdit.text()
        if self.flag_req != 0:
            self.typing = self.lineEdit.text()

        self.lineEdit.clear()

        #Обратная связь

        self.out = self.recognize_cmd(self.cmd)
        self.out = self.execute_cmd(self.out['cmd'])
        self.plainTextEdit.appendPlainText(self.out)

    def call_recognize(self):
        #при нажатии кнопки голосового управления - распознавание речи
        r = sr.Recognizer()
        m = sr.Microphone(device_index=0)
#        with m as source:
#            r.adjust_for_ambient_noise(source)
        with sr.Microphone(device_index=0) as source:
            audio = r.listen(source)
	
        recogn = r.recognize_google(audio, language="ru-RU")
        self.plainTextEdit.appendPlainText(recogn)
        if self.flag_req == 0:
            self.cmd = recogn
			
        if self.flag_req != 0:
            self.typing = recogn

        print('Вы сказали: ' + recogn)
        self.out = self.recognize_cmd(self.cmd)
        self.out = self.execute_cmd(self.out['cmd'])
        self.plainTextEdit.appendPlainText(self.out)
		
    def timerEvent(self, e):
        self.progressBar.setValue(AnalogShifr.Progress)
        if AnalogShifr.Progress >= self.maxPB:
            self.plainTextEdit.appendPlainText('Процесс завершен')
            self.progressBar.setValue(0)
            self.timer.stop()
            return

    def click_for_progressBar(self):
          
        if self.timer.isActive():
            self.timer.stop()
            self.progressBar.setValue(0)
            self.step = 0
        else:
            self.timer.start(100, self)    	


if __name__ == '__main__':
    
    #Дизайн
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()