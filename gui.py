import os
import requests
import sys
import urllib.request

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from cred import API_key

# TODO: delete temporal folder when closing app
# TODO: add refresh button
# TODO: get a better map style, google offers options
# TODO: style the app e.g.
# TODO: Clean!


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle('Recent Earthquakes Chile')

        earthquaque_api = requests.get('https://api.gael.cl/general/public/sismos')
        self.eq_data = earthquaque_api.json()

        self.main_layout = QVBoxLayout()
        self.main_widget = QWidget()

        self.scroll = QScrollArea()  # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()  # Widget that contains the collection of Vertical Box
        self.vbox = QVBoxLayout()  # The Vertical Box that contains the Horizontal Boxes of  labels and buttons

        self.info_buttons = []
        for index in range(15):
            data_dict = self.eq_data[index]
            btn_label = f'Fecha: {data_dict["Fecha"]} \nMagnitud: {data_dict["Magnitud"]}'
            self.info_buttons.append(QPushButton(btn_label))

        # Same process as lines 36-39
        # for w in self.info_buttons:
        #     w.setFixedWidth(350)
        #     w.clicked.connect(lambda: self.get_map_image(self.info_buttons.index(w)))
        #     self.vbox.addWidget(w)

        for i in range(len(self.info_buttons)):
            self.info_buttons[i].setFixedWidth(350)
            # self.info_buttons[i].clicked.connect(lambda: self.get_map_image(i)) TODO: maybe figure out why this doesn't work
            self.vbox.addWidget(self.info_buttons[i])

        self.vbox.setAlignment(Qt.AlignHCenter)
        self.widget.setLayout(self.vbox)

        # Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)


        self.photo = QLabel()
        self.generate_map_image(self.eq_data[0])
        self.photo.setPixmap(QPixmap('temporal/map-0.png'))



        self.main_layout.addWidget(self.photo)
        self.main_layout.addWidget(self.scroll)
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        self.setGeometry(600, 100, 600, 600)

        self.info_buttons[0].clicked.connect(lambda: self.get_map_image(0))
        self.info_buttons[1].clicked.connect(lambda: self.get_map_image(1))
        self.info_buttons[2].clicked.connect(lambda: self.get_map_image(2))
        self.info_buttons[3].clicked.connect(lambda: self.get_map_image(3))
        self.info_buttons[4].clicked.connect(lambda: self.get_map_image(4))
        self.info_buttons[5].clicked.connect(lambda: self.get_map_image(5))
        self.info_buttons[6].clicked.connect(lambda: self.get_map_image(6))
        self.info_buttons[7].clicked.connect(lambda: self.get_map_image(7))
        self.info_buttons[8].clicked.connect(lambda: self.get_map_image(8))
        self.info_buttons[9].clicked.connect(lambda: self.get_map_image(9))
        self.info_buttons[10].clicked.connect(lambda: self.get_map_image(10))
        self.info_buttons[11].clicked.connect(lambda: self.get_map_image(11))
        self.info_buttons[12].clicked.connect(lambda: self.get_map_image(12))
        self.info_buttons[13].clicked.connect(lambda: self.get_map_image(13))
        self.info_buttons[14].clicked.connect(lambda: self.get_map_image(14))




    def get_map_image(self, btn_index):
        print(str(self.sender))
        self.generate_map_image(self.eq_data[btn_index])
        self.photo.setPixmap(QPixmap(f'temporal/map-{btn_index}.png'))

    def generate_map_image(self, single_eq):
        lat = single_eq['Latitud']
        long = single_eq['Longitud']
        btn_index = self.eq_data.index(single_eq)
        self.dir_name = 'temporal'
        try:
            # Create target Directory
            os.mkdir(self.dir_name)
            print("Directory ", self.dir_name, " Created ")
        except FileExistsError:
            print("Directory ", self.dir_name, " already exists")
        if not os.path.isfile(f'temporal/map.png-{btn_index}'):
            gmaps_api_url = 'https://maps.googleapis.com/maps/api/staticmap?'
            url = f'{gmaps_api_url}center={lat},{long}&zoom=10&size=600x400&key={API_key}'
            urllib.request.urlretrieve(url, f'temporal/map-{btn_index}.png')
        else:
            print('file already exists')

    def test_map_1(self):
        self.photo.setPixmap(QPixmap('staticmap.png'))

    def test_map_2(self):
        self.photo.setPixmap(QPixmap('staticmap-1.png'))


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()