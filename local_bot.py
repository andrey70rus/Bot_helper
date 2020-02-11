#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime
import clr
clr.AddReference('AnalogShifr')
from AnalogShifr import *

import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
from design import bar_design

class ExampleApp(QtWidgets.QMainWindow, bar_design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.pushButton_2.released.connect(self.send_message)
        self.lineEdit.returnPressed.connect(self.pushButton_2.released) #отправка сообщений по <enter>
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
                self.flag_start_dll = 0
                AnalogShifr.Init(self.list[0], self.list[1], self.list[2], self.list[3], self.list[4], self.list[5], self.list[6], self.list[7])
                InitData.DocASU[4].Datai = "235263"
                InitData.DocASU[8].Datai = "235268"
                InitData.DocASU[16].Datai = "235275"
                AnalogShifr.path = self.list[8]
                AnalogShifr.pathToTemplates = "C:\\Bot\\testShifr\\Templates"
                AnalogShifr.StartCreateDoc()
                return('Процесс завершен!')
# вызов библиотеки проасу

        else:
            return('Команда не распознана, повторите!')

    def send_message(self):
        #передать значение обработчику команд (def recognize_cmd)
        self.plainTextEdit.appendPlainText(
            self.lineEdit.text()
           )

        if self.flag_req == 0:
            self.cmd = self.lineEdit.text()
        if self.flag_req != 0:
            self.typing = self.lineEdit.text()

#        if self.cmd.startswith(self.opts["alias"]):

#            for x in opts['alias']:
#                self.cmd = cmd.replace(x, "").strip()

        self.lineEdit.clear()

        #Обратная связь

        self.out = self.recognize_cmd(self.cmd)
        self.out = self.execute_cmd(self.out['cmd'])
        self.plainTextEdit.appendPlainText(self.out)

if __name__ == '__main__':
    
    #Дизайн
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение
    

