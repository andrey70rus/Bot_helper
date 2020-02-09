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
import bar_design

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
        print('Сейчас ' + str(now.hour) + ":" + str(now.minute))
   
    elif cmd == 'sapr':
        # запуск сапр
        os.system('xdg-open //home//andreyk//Загрузки//List_only.csv')
   
    else:
        print('Команда не распознана, повторите!')

class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна



if __name__ == '__main__':
    
    #Дизайн
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

    cmd = str(input())
    cmd = recognize_cmd(cmd)
    execute_cmd(cmd['cmd'])