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
from design import bar_design

opts = {
    "alias": ('помощник','сапр','бот','помощь','bot','helper',
              'цифровой помощник'),
    "commands": {
        "ctime": ('текущее время','сейчас времени','который час', 'time'),
        "sapr": ('проасу','запусти САПР','запусти проасу','запусти proasu',
        			'включи сапр', 'включи проасу', 'включи proasu')
    }
}

#распознавание команды "нечеткой логикой"
def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 35}
    for c,v in opts['commands'].items():
 
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt
   
    return RC

def execute_cmd(cmd):
    if cmd == 'ctime':
        # сказать текущее время
        now = datetime.datetime.now()
        return('Сейчас ' + str(now.hour) + ":" + str(now.minute))
   
    elif cmd == 'sapr':
        # запуск сапр
        os.system('xdg-open //home//andreyk//Загрузки//List_only.csv')
   
    else:
        return('Команда не распознана, повторите!')

class ExampleApp(QtWidgets.QMainWindow, bar_design.Ui_MainWindow):
    cmd = ''
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.pushButton_2.released.connect(self.send_message)
        self.lineEdit.returnPressed.connect(self.pushButton_2.released) #отправка сообщений по <enter>

    def send_message(self):
        #передать значение обработчику команд (def recognize_cmd)
        self.plainTextEdit.appendPlainText(
            self.lineEdit.text()
           )
        global cmd
        cmd = self.lineEdit.text()
        self.lineEdit.clear()
    
    def bot_message(self):
        #Обратная связь        
        cmd = recognize_cmd(cmd)
        outt = execute_cmd(cmd['cmd'])
        self.plainTextEdit.appendPlainText(outt)



if __name__ == '__main__':
    
    #Дизайн
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение
    

