import os
import requests
import sys
import urllib.request
import shutil
import atexit

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

API_key = os.environ['GOOGLE_API_KEY']

# TODO: add refresh button
# TODO: get a better map style, google offers options
# TODO: style the app like: red dot in the middle, bigger map area, road names, etc
# TODO: Clean!


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.dir_name = 'temporal'
        self.setWindowTitle('Recent Earthquakes Chile')

        # get info from the most recent earthquakes from api and work with it as json
        earthquake_api = requests.get('https://api.gael.cl/general/public/sismos')
        self.eq_data = earthquake_api.json()

        # It goes:
        # central widget
        #     - main_widget
        #         - main_layout
        #             - photo
        #             - widget
        #                 -vbox <- layout
        #                     - scroll
        #                         -buttons
        #                             -info

        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout()

        self.scroll = QScrollArea()  # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()  # Widget that contains the collection of Vertical Box
        self.v_scroll_layout = QVBoxLayout()  # The Vertical Box that contains the Horizontal Boxes of  labels and buttons

        self.button_group = QButtonGroup()
        self.button_group.buttonClicked[int].connect(self.on_button_clicked)

        for index in range(15):
            data_dict = self.eq_data[index]
            btn_label = f'Fecha: {data_dict["Fecha"]} \nMagnitud: {data_dict["Magnitud"]}'
            button_object = QPushButton(btn_label)
            self.button_group.addButton(button_object, index)
            self.v_scroll_layout.addWidget(button_object)

        self.v_scroll_layout.setAlignment(Qt.AlignHCenter)
        self.widget.setLayout(self.v_scroll_layout)

        # Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.photo = QLabel()
        self.download_map_image(self.eq_data[0])
        self.photo.setPixmap(QPixmap('temporal/map-0.png'))

        self.main_layout.addWidget(self.photo)
        self.main_layout.addWidget(self.scroll)
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        self.setGeometry(600, 100, 600, 600)

    def on_button_clicked(self, id):
        for button in self.button_group.buttons():
            if button is self.button_group.button(id):
                print(f"Showing image {id}")
                self.download_map_image(self.eq_data[id])
                self.photo.setPixmap(QPixmap(f'temporal/map-{id}.png'))

    def download_map_image(self, single_eq):
        """Generate image from google maps static api using geo data from earthquake api"""
        lat = single_eq['Latitud']
        long = single_eq['Longitud']
        btn_index = self.eq_data.index(single_eq)  # gets index of button pressed
        try:
            os.mkdir(self.dir_name)
            print("Directory ", self.dir_name, " Created ")
        except FileExistsError:
            print("Directory ", self.dir_name, " already exists")
        if not os.path.isfile(f'temporal/map-{btn_index}.png'):
            gmaps_api_url = 'https://maps.googleapis.com/maps/api/staticmap?'
            url = f'{gmaps_api_url}center={lat},{long}&zoom=8&size=600x400&key={API_key}'
            urllib.request.urlretrieve(url, f'temporal/map-{btn_index}.png')
            print("file created")
        else:
            print('file already exists')

    # Examples on getting an image file to show on Mainwindow
    def test_map_1(self):
        self.photo.setPixmap(QPixmap('staticmap.png'))

    def test_map_2(self):
        self.photo.setPixmap(QPixmap('staticmap-1.png'))


app = QApplication(sys.argv)

window = MainWindow()
window.show()


def delete_temporal_dir():
    shutil.rmtree('temporal')


atexit.register(delete_temporal_dir)
app.exec_()
