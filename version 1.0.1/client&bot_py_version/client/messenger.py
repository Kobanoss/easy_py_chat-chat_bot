import time
from datetime import datetime

import requests
import threading

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer

from clientui import Ui_MainWindow


class ExampleApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, url):
        super().__init__()
        self.setupUi(self)

        self.url = url

        self.pushButton.pressed.connect(self.send_message)
        self.after = time.time() - 24 * 60 * 60
        self.timer = QTimer()
        threading.Thread(target=self.updater()).start()

    def format_message(self, message):
        name = message['name']
        text = message['text']
        dt = datetime.fromtimestamp(message['time'])
        dt_beauty = dt.strftime('%Y/%m/%d %H:%M:%S')
        return f'{name} {dt_beauty}\n{text}\n'

    def add_text(self, text):
        self.textBrowser.append(text)
        self.textBrowser.repaint()

    def updater(self):
        self.timer.timeout.connect(self.update_messages)
        self.timer.start(1000)

    def update_messages(self):
        try:
            response = requests.get(f'{self.url}messages', params={'after': self.after})
        except:
            return
        messages = response.json()['messages']
        for message_in in messages:
            self.add_text(self.format_message(message_in))
            self.after = message_in['time']

    def send_message(self):
        name = self.lineEditName.text()
        password = self.lineEditPassword.text()
        text = self.textEdit.toPlainText()
        print(name, password, text)
        if not name or not password or not text:
            self.add_text('No input text\n')
            return
        message = {'name': name,
                   'password': password,
                   'text': text}
        try:
            response = requests.post(
                f'{self.url}send',
                json=message
            )
        except:
            self.add_text('No server connection\n')
            return

        if response.status_code == 200:
            self.textEdit.setText('')
        elif response.status_code == 401:
            self.add_text('Invalid name + password\n')
        else:
            self.add_text('Extreme error\n')


app = QtWidgets.QApplication([])
window = ExampleApp('http://127.0.0.1:5000/')
window.show()
app.exec_()
